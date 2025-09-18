import json
import logging
import traceback

from django.http import HttpResponse
from django.views import View
from schema import Schema, Regex, And, Or, Use, Optional

from apps.loon_base_view import BaseView
from service.ticket.ticket_flow_history_service import ticket_flow_history_service_ins
from service.account.account_base_service import account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from service.permission.user_permission import user_permission_check
from service.ticket.ticket_base_service import ticket_base_service_ins

logger = logging.getLogger("django")


class TicketListView(BaseView):
    get_schema = Schema({
        'category': And(str, Or('all', 'duty', 'owner', 'relation', 'worked', 'intervene', 'view')),
        Optional('sn'): str,
        Optional('title'): str,
        Optional('username'): str,
        Optional('create_start'): str,
        Optional('create_end'): str,
        Optional('workflow_ids'): str,
        Optional('stage_ids'): str,
        Optional('ticket_ids'): str,
        Optional('node_ids'): str,
        Optional('act_state'): And(str, Or('in_draft', 'on_going', 'rejected', 'withdrawn', 'finished', 'closed')),
        Optional('reverse', default=1): And(Use(int), lambda n: n in [0, 1]),
        Optional('creator_id'): And(Use(int), lambda n: n > 0, error='parent_ticket_id should be int and greater than 0'),
        Optional('parent_ticket_id'): And(Use(int), lambda n: n > 0, error='parent_ticket_id should be int and greater than 0'),
        Optional('parent_ticket_node_id'): And(Use(int), lambda n: n > 0, error='parent_ticket_node_id should be int and greater than 0'),
        Optional('page', default=1): And(Use(int), lambda n: n > 0, error='page should be int and greater than 0'),
        Optional('per_page', default=10): And(Use(int), lambda n: n > 0, error='per_page should be int and greater than 0'),
        Optional('act_state', default=10): And(Use(int), lambda n: n > 0, error='per_page should be int and greater than 0'),
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
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
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
        creator = request_data.get('creator', '')
        parent_ticket_id = int(request_data.get('parent_ticket_id', 0))
        parent_ticket_state_id = int(request_data.get('parent_ticket_state_id', 0))

        # 待办,关联的,创建
        category = request_data.get('category')
        # app_name
        app_name = request.META.get('HTTP_APPNAME')

        # 未指定创建起止时间则取最近三年的记录
        if not(create_start or create_end):
            import datetime
            end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            last_year_time = datetime.datetime.now() - datetime.timedelta(days=365*3)
            create_start = str(last_year_time)[:19]
            create_end = str(end_time)[:19]
        try:
            result = ticket_base_service_ins.get_ticket_list(
                tenant_id=tenant_id, title=title, user_id=user_id, create_start=create_start, create_end=create_end,
                workflow_ids=workflow_ids, node_ids=node_ids, ticket_ids=ticket_ids, category=category, reverse=reverse,
                per_page=per_page, page=page, app_name=app_name, act_state_id=act_state_id, from_admin=from_admin,
                creator=creator, parent_ticket_id=parent_ticket_id, parent_ticket_state_id=parent_ticket_state_id)
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
        user_view_permission = ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, operator_id)
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
            return api_response(0, '', dict(ticket_id=result))
        except CustomCommonException as e:
            return api_response(-1, str(e), '')
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", '')


# todo: update
class TicketView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        获取工单详情，根据用户返回不同的内容(是否有工单表单的编辑权限)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        # username = request_data.get('username', '')
        username = request.META.get('HTTP_USERNAME')
        if not username:
            return api_response(-1, '参数不全，请提供username', '')
        flag, result = ticket_base_service_ins.get_ticket_detail(ticket_id, username)
        if flag:
            code, data = 0, dict(value=result)
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)

    def patch(self, request, *args, **kwargs):
        """
        处理工单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'patch参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')

        app_name = request.META.get('HTTP_APPNAME')
        request_data_dict.update(dict(username=request.META.get('HTTP_USERNAME')))
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, {})

        result, msg = ticket_base_service_ins.handle_ticket(ticket_id, request_data_dict)
        if result or result is not False:
            code, data = 0, dict(value=result)
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除工单，仅用于管理员干预处理工单，loonflow管理后台的功能
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 校验工单权限
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        json_str = request.body.decode('utf-8')
        suggestion = ''
        if json_str:
            request_data_dict = json.loads(json_str)
            suggestion = request_data_dict.get('suggestion')

        flag, result = ticket_base_service_ins.ticket_admin_permission_check(ticket_id, username)
        if flag is False:
            return api_response(-1, result, {})
        flag, result = ticket_base_service_ins.delete_ticket(ticket_id, username, suggestion)
        if flag is False:
            return api_response(-1, result, {})
        else:
            return api_response(0, '', {})

class TicketFlowHistoryView(BaseView):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        app_name = request.META.get('HTTP_APPNAME')
        tenant_id = request.META.get('HTTP_TENANTID')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        desc = int(request_data.get('desc', 1))

        account_base_service_ins.app_ticket_permission_check(tenant_id, app_name, ticket_id)
        try:
            result = ticket_flow_history_service_ins.get_ticket_flow_history(tenant_id, ticket_id, per_page, page, desc)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, '', dict(ticket_flow_history_list = result['ticket_flow_history_object_format_list'], 
        total=result['paginator_info']['total'], page=result['paginator_info']['page'], per_page=result['paginator_info']['per_page']))

