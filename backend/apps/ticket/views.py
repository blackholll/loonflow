import json
import logging
import os
import traceback
import uuid
from django.conf import settings
from django.http import FileResponse, Http404
from schema import Schema, And, Or, Use, Optional
from apps.loon_base_view import BaseView
from service.format_response import api_response
from service.ticket.ticket_flow_history_service import ticket_flow_history_service_ins
from service.account.account_base_service import account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.ticket.ticket_base_service import ticket_base_service_ins
from service.ticket.ticket_node_service import ticket_node_service_ins
from service.common.common_service import common_service_ins

logger = logging.getLogger("django")


class TicketListView(BaseView):
    get_schema = Schema({
        'category': And(str, Or('all', 'duty', 'owner', 'relation', 'worked', 'intervene', 'view')),
        Optional('search_value'): str,
        Optional('username'): str,
        Optional('create_start'): str,
        Optional('create_end'): str,
        Optional('workflow_ids'): str,
        Optional('stage_ids'): str,
        Optional('ticket_ids'): str,
        Optional('node_ids'): str,
        Optional('act_state'): And(str, Or('in_draft', 'on_going', 'rejected', 'withdrawn', 'finished', 'closed')),
        Optional('reverse', default=1): And(Use(int), lambda n: n in [0, 1]),
        Optional('creator_id'): str,
        Optional('parent_ticket_id'): str,
        Optional('parent_ticket_node_id'): str,
        Optional('page', default=1): And(Use(int), lambda n: n > 0, error='page should be int and greater than 0'),
        Optional('per_page', default=10): And(Use(int), lambda n: n > 0, error='per_page should be int and greater than 0'),
    })

    post_schema = Schema({
        'workflow_id': str,
        'action_id': str,
        Optional('parent_ticket_id'): str,
        Optional('parent_ticket_node_id'): str,
        Optional('fields'): object,
    })

    def get(self, request, *args, **kwargs):
        """
        get ticket list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = request.META.get('HTTP_TENANTID')

        request_data = request.GET
        search_value = request_data.get('search_value', '')
        user_id = str(request.META.get('HTTP_USERID'))
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        node_ids = request_data.get('node_ids', '')
        ticket_ids = request_data.get('ticket_ids', '')
        reverse = int(request_data.get('reverse', 1)) if request_data.get('reverse', 1) else 1
        per_page = int(request_data.get('per_page')) if request_data.get('per_page') else 10
        page = int(request_data.get('page', 1))
        act_state_id = request_data.get('act_state_id', '')
        from_admin = request_data.get('from_admin', '')
        creator_id = request_data.get('creator_id', '')
        parent_ticket_id = request_data.get('parent_ticket_id', '')
        parent_ticket_node_id = request_data.get('parent_ticket_node_id', '')

        # duty, owner, relation, view, intervene
        category = request_data.get('category')
        # app_name
        app_name = request.META.get('HTTP_APPNAME')

        # Default list window: last three years (use aware local time for consistent filtering with USE_TZ)
        if not(create_start or create_end):
            from datetime import timedelta
            from django.utils import timezone
            now_local = timezone.localtime(timezone.now())
            end_time = now_local + timedelta(hours=1)
            last_year_time = now_local - timedelta(days=365 * 3)
            create_start = last_year_time.strftime('%Y-%m-%d %H:%M:%S')
            create_end = end_time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            result = ticket_base_service_ins.get_ticket_list(
                tenant_id, search_value, user_id, creator_id, create_start, create_end,
                workflow_ids, node_ids, ticket_ids, category, reverse,
                per_page, page, app_name, act_state_id=act_state_id, from_admin=from_admin,
                parent_ticket_id=parent_ticket_id, parent_ticket_node_id=parent_ticket_node_id)
            paginator_info = result.get('paginator_info')
            data = dict(ticket_list=result.get('ticket_result_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg,  = 0, ''
        except CustomCommonException as e:
            code, data, msg = -1, {}, e.message
        except Exception as e:
            logger.error(traceback.format_exc())
            code, data, msg = -1, {}, "Internal Server Error"
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        new ticket, should submit different args for different workflow
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        app_name = request.META.get('HTTP_APPNAME')

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)

        try:
            result = ticket_base_service_ins.new_ticket(tenant_id, app_name, operator_id, request_data_dict)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error",{})
        return api_response(0, "", dict(ticket_id=result))

class TicketDetailFormView(BaseView):

    def get(self, request, *args, **kwargs):
        """
        get ticket detail form, include form design and field value
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')
        
        # check whether user has view permission
        try:
            user_view_permission = ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        if not user_view_permission:
            return api_response(-1, "user has no view permission", '')

        try:
            component_result_list, workflow_metadata = ticket_base_service_ins.get_ticket_detail_form(tenant_id, operator_id, ticket_id)
            return api_response(0, '', dict(form_schema={'component_info_list':component_result_list, 'workflow_metadata':workflow_metadata}))
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')

class TicketDetailActionsView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket detail actions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        user_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')
        
        try:
            actions, action_base_node_id = ticket_base_service_ins.get_ticket_detail_actions(tenant_id, ticket_id, user_id)
            return api_response(0, '', dict(actions=actions, action_base_node_id=action_base_node_id))
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')

class TicketDetailAdminActionsView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket detail admin actions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        user_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')
        
        try:
            actions, action_base_node_id = ticket_base_service_ins.get_ticket_detail_admin_actions(tenant_id, ticket_id, user_id)
            return api_response(0, '', dict(actions=actions, action_base_node_id=action_base_node_id))
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')
        
class TicketHandleView(BaseView):
    def post(self, request, *args, **kwargs):
        """
        handle ticket
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        user_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')
        
        try:
            json_str = request.body.decode('utf-8')
            request_data_dict = json.loads(json_str)
            if not ticket_base_service_ins.ticket_action_permission_check(tenant_id, ticket_id, user_id, request_data_dict.get('action_type'), request_data_dict.get('action_id')):
                return api_response(-1, "user has no permission to handle this ticket", '')

            result = ticket_base_service_ins.handle_ticket(tenant_id, app_name, ticket_id, user_id, request_data_dict)
            return api_response(0, '', dict())
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')

class TicketFlowHistoryView(BaseView):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        operator_id = request.META.get('HTTP_USERID')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        desc = int(request_data.get('desc', 1))

        account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        try:
            user_view_permission = ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        if not user_view_permission:
            return api_response(-1, "user has no view permission", {})

        try:
            result = ticket_flow_history_service_ins.get_ticket_flow_history(tenant_id, ticket_id, per_page, page, desc)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, '', dict(ticket_flow_history_list = result['ticket_flow_history_object_format_list'], 
        total=result['paginator_info']['total'], page=result['paginator_info']['page'], per_page=result['paginator_info']['per_page']))


class TicketDraftFileUploadView(BaseView):
    """
    Draft file upload for new ticket: save to {upload_dir}/{tenant_id}/draft/{upload_id}/, return draft URL; migrate to ticket directory when creating ticket
    """
    def post(self, request, *args, **kwargs):
        tenant_id = request.META.get('HTTP_TENANTID')
        if not tenant_id:
            return api_response(-1, "tenant required", '')

        loonflow_data_dir = getattr(settings, 'LOONFLOW_DATA_DIR', None)
        if not loonflow_data_dir:
            return api_response(-1, "LOONFLOW_DATA_DIR not configured", '')
        upload_dir = os.path.join(loonflow_data_dir, tenant_id, 'ticket_uploads')

        if 'file' not in request.FILES:
            return api_response(-1, "no file in request", '')

        uploaded = request.FILES['file']
        ext = os.path.splitext(uploaded.name)[1] or ''
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        safe_name = str(uuid.uuid4()) + ext
        dir_path = os.path.join(upload_dir, 'draft')
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to create upload directory", '')

        file_path = os.path.join(dir_path, safe_name)
        try:
            with open(file_path, 'wb') as f:
                for chunk in uploaded.chunks():
                    f.write(chunk)
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to save file", '')

        draft_url = f"/api/v1.0/tickets/{tenant_id}/draft/files/{safe_name}"
        timestamp, token = common_service_ins.gen_file_temp_token(draft_url)
        draft_url = f"{draft_url}?token={token}&timestamp={timestamp}"
        return api_response(0, '', dict(url=draft_url, name=uploaded.name, size=uploaded.size))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class TicketDraftFileDownloadView(BaseView):
    """
    Draft file download for new ticket: download the file from {upload_dir}/{tenant_id}/ticket_uploads/draft/{safe_name}
    only support temp token validataion
    """
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', '')
        timestamp = request.GET.get('timestamp', '')
        if not (token and timestamp):
            return api_response(-1, "token and timestamp are required", '')
        
        # check token valudation
        tenant_id = kwargs.get('tenant_id', '')
        safe_name = kwargs.get('safe_name', '')
        file_uri = f"/api/v1.0/tickets/{tenant_id}/draft/files/{safe_name}?token={token}&timestamp={timestamp}"
        flag, msg = common_service_ins.check_file_temp_token(token, timestamp, file_uri)
        if not flag:
            return api_response(-1, msg, '')
        safe_name = kwargs.get('safe_name', '')
        tenant_id = kwargs.get('tenant_id', '')

        if not safe_name or '..' in safe_name or '/' in safe_name or '\\' in safe_name:
            return api_response(-1, "invalid path", '')

        loonflow_data_dir = getattr(settings, 'LOONFLOW_DATA_DIR', None)
        if not loonflow_data_dir:
            return api_response(-1, "LOONFLOW_DATA_DIR not configured", '')
        upload_dir = os.path.join(loonflow_data_dir, tenant_id, 'ticket_uploads')
        file_path = os.path.join(upload_dir, 'draft', safe_name)

        if not os.path.isfile(file_path):
            raise Http404("File not found")

        try:
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=safe_name)
            return response
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to read file", '')

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class TicketFileUploadView(BaseView):
    """ 
    Ticket file upload: save the file to {LOONFLOW_DATA_DIR}/{tenant_id}/ticket_uploads/{ticket_id}/ and return the access path
    """
    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')

        try:
            user_view_permission = ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        if not user_view_permission:
            return api_response(-1, "user has no view permission", '')

        loonflow_data_dir = getattr(settings, 'LOONFLOW_DATA_DIR', None)
        if not loonflow_data_dir:
            return api_response(-1, "LOONFLOW_DATA_DIR not configured", '')
        upload_dir = os.path.join(loonflow_data_dir, tenant_id, 'ticket_uploads')
        dir_path = os.path.join(upload_dir, str(ticket_id))

        if 'file' not in request.FILES:
            return api_response(-1, "no file in request", '')

        uploaded = request.FILES['file']
        ext = os.path.splitext(uploaded.name)[1] or ''
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        safe_name = str(uuid.uuid4()) + ext
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to create upload directory", '')

        file_path = os.path.join(dir_path, safe_name)
        try:
            with open(file_path, 'wb') as f:
                for chunk in uploaded.chunks():
                    f.write(chunk)
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to save file", '')

        file_url = f"/api/v1.0/tickets/{tenant_id}/{ticket_id}/files/{safe_name}"
        timestamp, token = common_service_ins.gen_file_temp_token(file_url)
        file_url = f"{file_url}?token={token}&timestamp={timestamp}"
        return api_response(0, '', dict(url=file_url, name=uploaded.name, size=uploaded.size))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class TicketFileDownloadView(BaseView):
    """
    Ticket file download: check the ticket view permission and return the file content, the path is the same as TicketFileUploadView, the URL is the safe_name
    """
    def get(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        safe_name = kwargs.get('safe_name', '')
        tenant_id = kwargs.get('tenant_id', '')
        operator_id = request.META.get('HTTP_USERID')
        token = request.GET.get('token', '')
        timestamp = request.GET.get('timestamp', '')

        if not safe_name or '..' in safe_name or '/' in safe_name or '\\' in safe_name:
            return api_response(-1, "invalid safe_name", '')

        
        if token:
            # token permission check
            file_uri = f"/api/v1.0/tickets/{tenant_id}/{ticket_id}/files/{safe_name}"
            flag, msg = common_service_ins.check_file_temp_token(token, timestamp, file_uri)
            if not flag:
                return api_response(-1, msg, '')
        else:
            try:
                account_base_service_ins.app_ticket_permission_check(tenant_id, 'loonflow', ticket_id)
            except CustomCommonException as e:
                return api_response(-1, str(e), '')
            except Exception:
                logger.error(traceback.format_exc())
                return api_response(-1, "Internal Server Error", '')

            try:
                user_view_permission = ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, operator_id)
            except CustomCommonException as e:
                return api_response(-1, str(e), '')
            if not user_view_permission:
                return api_response(-1, "user has no view permission", '')

        loonflow_data_dir = getattr(settings, 'LOONFLOW_DATA_DIR', None)
        if not loonflow_data_dir:
            return api_response(-1, "LOONFLOW_DATA_DIR not configured", '')

        upload_dir = os.path.join(loonflow_data_dir, tenant_id, 'ticket_uploads')
        file_path = os.path.join(upload_dir, str(ticket_id), safe_name)
        if not os.path.isfile(file_path):
            raise Http404("File not found")

        try:
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=safe_name)
            return response
        except OSError:
            logger.error(traceback.format_exc())
            return api_response(-1, "failed to read file", '')

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class TicketMockExternalAssigneeView(BaseView):
    def post(self, request, *args, **kwargs):
        """
        mock external assignee
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        # token = "" # should be the same as you configured in loonflow
        # if token and signature and timestamp:
        #     try:
        #         common_service_ins.signature_check(timestamp, signature, token)
        #     except CustomCommonException as e:
        #         return api_response(-1, str(e), {})

        # you can return the assignee email list base on ticket detail info from body
        # try:
        #     body = json.loads(request.body.decode('utf-8')) if request.body else {}
        # except (json.JSONDecodeError, UnicodeDecodeError):
        #     body = {}
        # if not isinstance(body, dict):
        #     body = {}
        return api_response(0, '', {'assignee_email_list': ["blackholll@loonapp.com"]})


class TicketMockExternalDataSourceView(BaseView):
    """
    Mock endpoint for external data source field testing.
    Expects the same headers as hook calls: signature + timestamp (md5(timestamp + token)).
    Request body is the ticket fields JSON object.
    Response shape matches fetch_external_data_source_value: code 0 and data.value.

    Query params:
    - style or displayStyle: json | key_value | text (same as form field displayStyle).
      Demo payload is shaped for that rendering mode.
    - token: optional, for signature_check when signature/timestamp are sent.
    """

    @staticmethod
    def _demo_value_for_style(style: str, _body: dict) -> object:
        """Minimal sample values for each displayStyle (_body is the ticket fields POST body, unused)."""
        if style == 'json':
            return [
                {'id': 1, 'name': 'demo_item_a', 'ok': True},
                {'id': 2, 'name': 'demo_item_b', 'ok': False},
            ]

        if style == 'key_value':
            return {'a': 1, 'b': 2, 'c': 3}

        return 'this is a sample text from external'

    def post(self, request, *args, **kwargs):
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        # token = "" # should be the same as you configured in loonflow
        # if token and signature and timestamp:
        #     try:
        #         common_service_ins.signature_check(timestamp, signature, token)
        #     except CustomCommonException as e:
        #         return api_response(-1, str(e), {})

        # you can return the result base on ticket detail info from body
        try:
            body = json.loads(request.body.decode('utf-8')) if request.body else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            body = {}
        if not isinstance(body, dict):
            body = {}

        raw_style = (
            request.GET.get('style')
            or request.GET.get('displayStyle')
            or 'text'
        )
        style = str(raw_style).strip().lower()
        if style in ('keyvalue', 'key-value'):
            style = 'key_value'
        if style not in ('json', 'key_value', 'text'):
            style = 'text'

        demo_value = self._demo_value_for_style(style, body)
        return api_response(0, '', {'value': demo_value})
class TicketCurrentNodeInfosView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket current node infos
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        user_id = request.META.get('HTTP_USERID')
        try:
            account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
            current_node_infos = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
            result_list = []
            for current_node_info in current_node_infos:
                result_list.append(dict(
                    id=current_node_info.node_id,
                    name=current_node_info.node.name,
                ))
            return api_response(0, '', dict(current_node_info_list=result_list))

        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')