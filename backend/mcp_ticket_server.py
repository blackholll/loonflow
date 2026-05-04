"""
MCP server for ticket querying and handling.

This server calls Django service-layer methods directly and performs
permission checks explicitly instead of relying on HTTP middleware.

Authentication: pass ``access_token`` (JWT or personal access token ``lfpat.*``) as
a tool argument, or set ``Authorization: Bearer <token>`` / ``X-Loonflow-Access-Token``
on the HTTP client, or set env ``LOONFLOW_MCP_ACCESS_TOKEN`` on the server process
(stdio or default token when the tool argument is empty).

Run (``python mcp_ticket_server.py`` from ``backend/``):
- Default: Streamable HTTP (remote-friendly). Listens on ``LOONFLOW_MCP_HOST`` (default
  ``127.0.0.1``) and ``LOONFLOW_MCP_PORT`` (default ``8000``). Client URL is
  ``http://<host>:<port>/mcp`` (see ``streamable_http_path`` in FastMCP, default ``/mcp``).
- Set ``LOONFLOW_MCP_TRANSPORT=stdio`` to use stdio (e.g. Cursor spawning the process).
- Bind on all interfaces: ``LOONFLOW_MCP_HOST=0.0.0.0``.
"""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

import jwt
from django.conf import settings
from django.utils import timezone

# Django bootstrap
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.config")
import django  # noqa: E402

django.setup()

from mcp.server.fastmcp import Context, FastMCP  # noqa: E402

from service.account.account_user_service import AccountUserService  # noqa: E402
from service.account.personal_access_token_service import personal_access_token_service_ins  # noqa: E402
from service.account.account_base_service import account_base_service_ins  # noqa: E402
from service.exception.custom_common_exception import CustomCommonException  # noqa: E402
from service.ticket.ticket_base_service import ticket_base_service_ins  # noqa: E402


def _mcp_listen_config() -> tuple[str, int]:
    host = (os.environ.get("LOONFLOW_MCP_HOST") or "127.0.0.1").strip() or "127.0.0.1"
    raw_port = (os.environ.get("LOONFLOW_MCP_PORT") or "8002").strip()
    try:
        port = int(raw_port)
    except ValueError:
        port = 8000
    return host, port


_mcp_host, _mcp_port = _mcp_listen_config()
mcp = FastMCP("loonflow-ticket", host=_mcp_host, port=_mcp_port)


def _stdout_log(event: str, **kwargs: Any) -> None:
    payload = {
        "event": event,
        "ts": timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S%z"),
        **kwargs,
    }
    print(json.dumps(payload, ensure_ascii=False, default=str), flush=True)


@dataclass
class TicketAuthContext:
    tenant_id: str
    user_id: str
    app_name: str


def _normalize_bearer(access_token: str) -> str:
    token = (access_token or "").strip()
    if token.startswith("Bearer "):
        token = token[7:].strip()
    if not token:
        raise CustomCommonException("access_token is required")
    return token


def _access_token_from_http_context(mcp_ctx: Context | None) -> str:
    if mcp_ctx is None:
        return ""
    try:
        req = mcp_ctx.request_context.request
        if req is None:
            return ""
        headers = req.headers
        auth = headers.get("authorization") or ""
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        custom = headers.get("x-loonflow-access-token")
        if custom:
            return custom.strip()
    except Exception:
        return ""
    return ""


def _resolve_access_token(access_token: str, mcp_ctx: Context | None = None) -> str:
    candidate = (access_token or "").strip()
    if candidate:
        return _normalize_bearer(candidate)
    candidate = _access_token_from_http_context(mcp_ctx).strip()
    if candidate:
        return _normalize_bearer(candidate)
    env_tok = (os.environ.get("LOONFLOW_MCP_ACCESS_TOKEN") or "").strip()
    if env_tok:
        return _normalize_bearer(env_tok)
    raise CustomCommonException(
        "access_token is required: pass the tool argument, send Authorization or "
        "X-Loonflow-Access-Token from the MCP HTTP client, or set LOONFLOW_MCP_ACCESS_TOKEN "
        "for the server process"
    )


def _resolve_user_from_access_token(access_token: str):
    token = _normalize_bearer(access_token)
    if token.startswith("lfpat."):
        return personal_access_token_service_ins.verify_token_string(token)
    jwt_salt = settings.JWT_SALT
    try:
        jwt_data = jwt.decode(token, jwt_salt, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise CustomCommonException("Token expired") from None
    except jwt.InvalidTokenError:
        raise CustomCommonException("Invalid token") from None
    except Exception as exc:
        raise CustomCommonException("Invalid token") from exc
    email = (jwt_data.get("data") or {}).get("email")
    if not email:
        raise CustomCommonException("Invalid token")
    return AccountUserService.get_user_by_email(email)


def _auth_context(
    access_token: str,
    app_name: str = "loonflow",
    mcp_ctx: Context | None = None,
) -> TicketAuthContext:
    user = _resolve_user_from_access_token(_resolve_access_token(access_token, mcp_ctx))
    app = str(app_name or "loonflow").strip() or "loonflow"
    return TicketAuthContext(
        tenant_id=str(user.tenant_id),
        user_id=str(user.id),
        app_name=app,
    )


def _build_default_time_window(create_start: str, create_end: str) -> tuple[str, str]:
    if create_start or create_end:
        return create_start, create_end
    now_local = timezone.localtime(timezone.now())
    end_time = now_local + timedelta(hours=1)
    start_time = now_local - timedelta(days=365 * 3)
    return (
        start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S"),
    )


def _extract_form_field_permissions(component_info_list: list[dict[str, Any]]) -> dict[str, str]:
    field_permissions: dict[str, str] = {}
    for component in component_info_list:
        if component.get("type") != "row":
            continue
        for child in component.get("children", []):
            field_key = str(child.get("component_key", "")).strip()
            if not field_key:
                continue
            permission = str(child.get("component_permission", "")).strip() or "readonly"
            field_permissions[field_key] = permission
    return field_permissions


def _build_handle_request_payload(
    action_type: str,
    action_id: str,
    action_props: dict[str, Any] | None,
    fields: dict[str, Any] | None,
) -> dict[str, Any]:
    payload = {
        "action_type": str(action_type or "").strip(),
        "action_id": str(action_id or "").strip(),
        "action_props": action_props or {},
        "fields": fields or {},
    }
    if not payload["action_type"]:
        raise CustomCommonException("action_type is required")
    if not payload["action_id"]:
        raise CustomCommonException("action_id is required")
    return payload


def _assert_ticket_access(ctx: TicketAuthContext, ticket_id: str) -> None:
    account_base_service_ins.app_ticket_permission_check(ctx.tenant_id, ctx.app_name, ticket_id)
    if not ticket_base_service_ins.ticket_view_permission_check(ctx.tenant_id, ticket_id, ctx.user_id):
        raise CustomCommonException("user has no view permission")


def _ticket_list_sync(
    access_token: str,
    app_name: str,
    category: str,
    search_value: str,
    create_start: str,
    create_end: str,
    workflow_ids: str,
    node_ids: str,
    ticket_ids: str,
    act_state: str,
    creator_id: str,
    parent_ticket_id: str,
    reverse: int,
    per_page: int,
    page: int,
    mcp_ctx: Context | None,
) -> dict[str, Any]:
    _stdout_log(
        "ticket_list.start",
        app_name=app_name,
        category=category,
        per_page=per_page,
        page=page,
        reverse=reverse,
    )
    ctx = _auth_context(access_token, app_name, mcp_ctx)
    allowed_categories = {"duty", "owner", "relation", "view", "worked", "intervene", "all"}
    if category not in allowed_categories:
        raise CustomCommonException("category is invalid")
    create_start_val, create_end_val = _build_default_time_window(create_start, create_end)
    result = ticket_base_service_ins.get_ticket_list(
        ctx.tenant_id,
        search_value,
        ctx.user_id,
        creator_id,
        create_start_val,
        create_end_val,
        workflow_ids,
        node_ids,
        ticket_ids,
        category,
        int(reverse),
        int(per_page),
        int(page),
        ctx.app_name,
        act_state=act_state,
        parent_ticket_id=parent_ticket_id,
    )
    paginator_info = result.get("paginator_info", {})
    response = {
        "ticket_list": result.get("ticket_result_restful_list", []),
        "per_page": paginator_info.get("per_page", per_page),
        "page": paginator_info.get("page", page),
        "total": paginator_info.get("total", 0),
    }
    _stdout_log(
        "ticket_list.done",
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
        app_name=ctx.app_name,
        category=category,
        page=response["page"],
        per_page=response["per_page"],
        total=response["total"],
        count=len(response["ticket_list"]),
    )
    return response


@mcp.tool()
async def ticket_list(
    access_token: str = "",
    app_name: str = "loonflow",
    category: str = "duty",
    search_value: str = "",
    create_start: str = "",
    create_end: str = "",
    workflow_ids: str = "",
    node_ids: str = "",
    ticket_ids: str = "",
    act_state: str = "",
    creator_id: str = "",
    parent_ticket_id: str = "",
    reverse: int = 1,
    per_page: int = 10,
    page: int = 1,
    mcp_ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Query ticket list using existing ticket service.

    Supported categories:
    - duty: my todo
    - owner: created by me
    - relation: related to me
    - view: I can view
    - worked: tickets I processed
    - intervene: I can intervene
    - all: all tickets (admin only)
    """
    return await asyncio.to_thread(
        _ticket_list_sync,
        access_token,
        app_name,
        category,
        search_value,
        create_start,
        create_end,
        workflow_ids,
        node_ids,
        ticket_ids,
        act_state,
        creator_id,
        parent_ticket_id,
        reverse,
        per_page,
        page,
        mcp_ctx,
    )


def _ticket_detail_sync(
    ticket_id: str,
    access_token: str,
    app_name: str,
    mcp_ctx: Context | None,
) -> dict[str, Any]:
    _stdout_log("ticket_detail.start", ticket_id=ticket_id, app_name=app_name)
    ctx = _auth_context(access_token, app_name, mcp_ctx)
    _assert_ticket_access(ctx, ticket_id)
    component_info_list, workflow_metadata = ticket_base_service_ins.get_ticket_detail_form(
        ctx.tenant_id, ctx.user_id, ticket_id
    )
    actions, action_base_node_id = ticket_base_service_ins.get_ticket_detail_actions(
        ctx.tenant_id, ticket_id, ctx.user_id
    )
    admin_actions, admin_action_base_node_id = ticket_base_service_ins.get_ticket_detail_admin_actions(
        ctx.tenant_id, ticket_id, ctx.user_id
    )
    field_permissions = _extract_form_field_permissions(component_info_list)
    required_fields = [k for k, v in field_permissions.items() if v == "required"]
    optional_fields = [k for k, v in field_permissions.items() if v == "optional"]
    readonly_fields = [k for k, v in field_permissions.items() if v not in {"required", "optional"}]
    response = {
        "form_schema": {
            "component_info_list": component_info_list,
            "workflow_metadata": workflow_metadata,
        },
        "field_permissions": field_permissions,
        "required_fields": required_fields,
        "optional_fields": optional_fields,
        "readonly_fields": readonly_fields,
        "actions": actions,
        "action_base_node_id": action_base_node_id,
        "admin_actions": admin_actions,
        "admin_action_base_node_id": admin_action_base_node_id,
    }
    _stdout_log(
        "ticket_detail.done",
        ticket_id=ticket_id,
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
        action_count=len(actions),
        admin_action_count=len(admin_actions),
    )
    return response


@mcp.tool()
async def ticket_detail(
    ticket_id: str,
    access_token: str = "",
    app_name: str = "loonflow",
    mcp_ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Query ticket detail form and available actions.
    """
    return await asyncio.to_thread(_ticket_detail_sync, ticket_id, access_token, app_name, mcp_ctx)


@mcp.tool()
async def ticket_prepare_handle(
    ticket_id: str,
    access_token: str = "",
    app_name: str = "loonflow",
    mcp_ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Prepare ticket handling context:
    - form and required fields
    - user actions
    - admin actions
    """
    return await asyncio.to_thread(_ticket_detail_sync, ticket_id, access_token, app_name, mcp_ctx)


def _ticket_handle_sync(
    ticket_id: str,
    action_type: str,
    action_id: str,
    access_token: str,
    action_props: dict[str, Any] | None,
    fields: dict[str, Any] | None,
    app_name: str,
    dry_run: bool,
    mcp_ctx: Context | None,
) -> dict[str, Any]:
    _stdout_log(
        "ticket_handle.start",
        ticket_id=ticket_id,
        action_type=action_type,
        action_id=action_id,
        app_name=app_name,
        dry_run=dry_run,
    )
    ctx = _auth_context(access_token, app_name, mcp_ctx)
    _assert_ticket_access(ctx, ticket_id)
    payload = _build_handle_request_payload(action_type, action_id, action_props, fields)
    if not ticket_base_service_ins.ticket_action_permission_check(
        ctx.tenant_id, ticket_id, ctx.user_id, payload["action_type"], payload["action_id"]
    ):
        raise CustomCommonException("user has no permission to handle this ticket")

    component_info_list, _ = ticket_base_service_ins.get_ticket_detail_form(ctx.tenant_id, ctx.user_id, ticket_id)
    field_permissions = _extract_form_field_permissions(component_info_list)
    required_fields = [k for k, v in field_permissions.items() if v == "required"]
    missing_required_fields = [
        field_key for field_key in required_fields if field_key not in payload.get("fields", {}).keys()
    ]
    if missing_required_fields:
        raise CustomCommonException(f"missing required fields: {', '.join(missing_required_fields)}")

    actions, action_base_node_id = ticket_base_service_ins.get_ticket_detail_actions(
        ctx.tenant_id, ticket_id, ctx.user_id
    )
    admin_actions, admin_action_base_node_id = ticket_base_service_ins.get_ticket_detail_admin_actions(
        ctx.tenant_id, ticket_id, ctx.user_id
    )
    allowed_action_pairs = {
        (str(action.get("type", "")), str(action.get("id", "")))
        for action in (actions + admin_actions)
    }
    if (payload["action_type"], payload["action_id"]) not in allowed_action_pairs:
        raise CustomCommonException("action_type/action_id is not available for current user")

    if payload["action_type"] == "add_comment":
        action_props_payload = payload.setdefault("action_props", {})
        if not action_props_payload.get("node_id"):
            fallback_node_id = action_base_node_id or admin_action_base_node_id or ""
            if fallback_node_id:
                action_props_payload["node_id"] = fallback_node_id
                _stdout_log(
                    "ticket_handle.add_comment.auto_node_id",
                    ticket_id=ticket_id,
                    node_id=fallback_node_id,
                )

    if dry_run:
        response = {
            "dry_run": True,
            "ticket_id": ticket_id,
            "validated_action": {
                "action_type": payload["action_type"],
                "action_id": payload["action_id"],
                "action_props": payload.get("action_props", {}),
            },
            "provided_fields": list(payload.get("fields", {}).keys()),
            "required_fields": required_fields,
            "missing_required_fields": [],
            "status": "validated",
        }
        _stdout_log(
            "ticket_handle.dry_run_done",
            ticket_id=ticket_id,
            action_type=payload["action_type"],
            action_id=payload["action_id"],
            user_id=ctx.user_id,
        )
        return response

    ticket_base_service_ins.handle_ticket(
        ctx.tenant_id,
        ctx.app_name,
        ticket_id,
        ctx.user_id,
        payload,
    )
    response = {
        "dry_run": False,
        "ticket_id": ticket_id,
        "status": "handled",
        "action_type": payload["action_type"],
        "action_id": payload["action_id"],
    }
    _stdout_log(
        "ticket_handle.done",
        ticket_id=ticket_id,
        action_type=payload["action_type"],
        action_id=payload["action_id"],
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
    )
    return response


@mcp.tool()
async def ticket_handle(
    ticket_id: str,
    action_type: str,
    action_id: str,
    access_token: str = "",
    action_props: dict[str, Any] | None = None,
    fields: dict[str, Any] | None = None,
    app_name: str = "loonflow",
    dry_run: bool = False,
    mcp_ctx: Context | None = None,
) -> dict[str, Any]:
    """
    Handle a ticket after checking permissions and required fields.
    """
    return await asyncio.to_thread(
        _ticket_handle_sync,
        ticket_id,
        action_type,
        action_id,
        access_token,
        action_props,
        fields,
        app_name,
        dry_run,
        mcp_ctx,
    )


if __name__ == "__main__":
    transport = (os.environ.get("LOONFLOW_MCP_TRANSPORT") or "streamable-http").strip().lower()
    if transport in ("stdio",):
        mcp.run(transport="stdio")
    elif transport in ("streamable-http", "streamable_http", "http"):
        mcp.run(transport="streamable-http")
    elif transport in ("sse",):
        mcp.run(transport="sse")
    else:
        raise SystemExit(
            f"Unknown LOONFLOW_MCP_TRANSPORT={transport!r}; "
            "use stdio, sse, or streamable-http"
        )
