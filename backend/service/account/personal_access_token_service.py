"""
Personal access tokens (PAT) for programmatic API/MCP access.

Plain token is shown only once at creation. Only an encrypted password-hash
of the secret segment is stored at rest (AES via encrypt_service wrapping
Django's password hasher output).
"""

from __future__ import annotations

import secrets
import uuid
from datetime import timedelta
from typing import Any

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone

from apps.account.models import PersonalAccessToken, User
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.encrypt_service import encrypt_service_ins


PAT_SCHEME = "lfpat"


class PersonalAccessTokenService(BaseService):
    """Create, list, revoke, and verify personal access tokens."""

    @staticmethod
    def _parse_token(raw: str) -> tuple[str, str]:
        token = (raw or "").strip()
        if token.startswith("Bearer "):
            token = token[7:].strip()
        parts = token.split(".", 2)
        if len(parts) != 3 or parts[0] != PAT_SCHEME:
            raise CustomCommonException("Invalid personal access token format")
        token_id, secret = parts[1], parts[2]
        if not token_id or not secret:
            raise CustomCommonException("Invalid personal access token format")
        return token_id, secret

    @classmethod
    def verify_token_string(cls, raw: str) -> User:
        """
        Validate a PAT string and return the owning User.
        Updates last_used_at on success.
        """
        token_id, secret = cls._parse_token(raw)
        try:
            token_uuid = uuid.UUID(str(token_id))
        except ValueError as exc:
            raise CustomCommonException("Invalid personal access token") from exc

        row = (
            PersonalAccessToken.objects.filter(id=token_uuid, revoked_at__isnull=True)
            .select_related("user")
            .first()
        )
        if not row:
            raise CustomCommonException("Invalid personal access token")
        if row.expires_at and row.expires_at < timezone.now():
            raise CustomCommonException("Personal access token expired")
        if not row.user or not row.user.is_active:
            raise CustomCommonException("User is inactive")

        try:
            pwd_hash = encrypt_service_ins.decrypt(row.secret_ciphertext)
        except Exception as exc:
            raise CustomCommonException("Invalid personal access token") from exc

        if not check_password(secret, pwd_hash):
            raise CustomCommonException("Invalid personal access token")

        PersonalAccessToken.objects.filter(id=row.id).update(last_used_at=timezone.now())
        return row.user

    @classmethod
    @transaction.atomic
    def create_token(
        cls,
        *,
        user_id: str,
        tenant_id: str,
        label: str = "",
        expires_in_days: int | None = None,
    ) -> dict[str, Any]:
        """
        Create a new PAT. Returns the full plaintext token once.

        expires_in_days: None or 0 means no expiry; otherwise 1..730.
        """
        user = User.objects.filter(id=user_id, tenant_id=tenant_id).first()
        if not user:
            raise CustomCommonException("User not found")

        if expires_in_days is not None:
            if expires_in_days < 0 or expires_in_days > 730:
                raise CustomCommonException("expires_in_days must be between 0 and 730")

        secret = secrets.token_urlsafe(48)
        row = PersonalAccessToken(
            tenant_id=tenant_id,
            creator_id=user_id,
            user=user,
            token_label=(label or "")[:200],
        )
        row.save()

        full_token = f"{PAT_SCHEME}.{row.id}.{secret}"
        pwd_hash = make_password(secret)
        row.secret_ciphertext = encrypt_service_ins.encrypt(pwd_hash)
        row.mask_prefix = full_token[:14]
        if expires_in_days:
            row.expires_at = timezone.now() + timedelta(days=int(expires_in_days))
        row.save(
            update_fields=[
                "secret_ciphertext",
                "mask_prefix",
                "expires_at",
                "updated_at",
            ]
        )

        return {
            "id": str(row.id),
            "token": full_token,
            "label": row.token_label,
            "expires_at": row.expires_at.strftime("%Y-%m-%d %H:%M:%S") if row.expires_at else "",
            "masked_hint": cls.mask_for_prefix(row.mask_prefix),
        }

    @staticmethod
    def mask_for_prefix(prefix: str) -> str:
        """Build a display-only masked token string."""
        p = prefix or ""
        if len(p) < 4:
            return "****"
        return p + ("*" * 32)

    @classmethod
    def list_tokens(cls, *, user_id: str, tenant_id: str) -> list[dict[str, Any]]:
        rows = (
            PersonalAccessToken.objects.filter(user_id=user_id, tenant_id=tenant_id)
            .order_by("-created_at")
            .all()
        )
        result = []
        for row in rows:
            revoked = row.revoked_at is not None
            result.append(
                {
                    "id": str(row.id),
                    "label": row.token_label or "",
                    "masked_token": cls.mask_for_prefix(row.mask_prefix),
                    "expires_at": row.expires_at.strftime("%Y-%m-%d %H:%M:%S") if row.expires_at else "",
                    "created_at": row.created_at.strftime("%Y-%m-%d %H:%M:%S") if row.created_at else "",
                    "last_used_at": row.last_used_at.strftime("%Y-%m-%d %H:%M:%S")
                    if row.last_used_at
                    else "",
                    "revoked": revoked,
                }
            )
        return result

    @classmethod
    @transaction.atomic
    def revoke_token(cls, *, token_id: str, user_id: str, tenant_id: str) -> bool:
        qs = PersonalAccessToken.objects.filter(
            id=token_id, user_id=user_id, tenant_id=tenant_id, revoked_at__isnull=True
        )
        if not qs.exists():
            raise CustomCommonException("Token not found or already revoked")
        qs.update(revoked_at=timezone.now())
        return True


personal_access_token_service_ins = PersonalAccessTokenService()
