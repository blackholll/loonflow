import json
import logging
import traceback

from django.views import View
from schema import Schema, Regex, And, Or, Use, Optional
from urllib3 import request

from apps.loon_base_view import BaseView
from service.account.account_base_service import account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from service.permission.user_permission import user_permission_check
from service.workflow.workflow_base_service import workflow_base_service_ins
from service.workflow.workflow_component_service import workflow_component_service_ins
from service.workflow.workflow_permission_service import workflow_permission_service_ins

logger = logging.getLogger("django")


class WorkflowView(BaseView):
    @user_permission_check("admin, workflow_admin")
    def get(self, request, *args, **kwargs):
        """
        get workflow list api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = workflow_base_service_ins.get_workflow_list(tenant_id, operator_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(workflow_info_list=result.get("workflow_info_list"), page=
                                        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))

    @user_permission_check('workflow_admin,admin')
    def post(self, request, *args, **kwargs):
        """
        new workflow. include all workflow info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            workflow_id = workflow_base_service_ins.add_workflow(operator_id, tenant_id, request_data_dict)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(workflow_id=workflow_id))

class WorkflowSimpleView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get simple workflow list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = workflow_base_service_ins.get_workflow_list(tenant_id, operator_id, search_value, page, per_page, simple=True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(workflow_info_list=result.get("workflow_info_list"), page=
        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))


class WorkflowInitNodeView(BaseView):
    """
    workflow's init node info
    """
    def get(self, request, *args, **kwargs):
        """
        get workflow's init node info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get("workflow_id")
        try:
            result = workflow_base_service_ins.get_workflow_init_node_rest(workflow_id=workflow_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)




class WorkflowVersionsView(BaseView):
    @user_permission_check("admin, workflow_admin")
    def get(self, request, *args, **kwargs):
        workflow_id = kwargs.get("workflow_id")
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        search_value = request.GET.get('search_value', '')
        per_page = int(request.GET.get('per_page', 10)) if request.GET.get('per_page', 10) else 10
        page = int(request.GET.get('page', 1)) if request.GET.get('page', 1) else 1
        try:
            result = workflow_base_service_ins.get_workflow_version_list(workflow_id, tenant_id, operator_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(version_info_list=result.get("version_info_list"), page=
                                        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))




class WorkflowDetailView(BaseView):
    @user_permission_check('workflow_admin,admin', workflow_id_source='url')
    def get(self, request, *args, **kwargs):
        """
        获取工作流详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        version_name = request.GET.get('version_name', '')
        
        try:
            workflow_result = workflow_base_service_ins.get_full_definition_info_by_id(tenant_id, workflow_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        
        return api_response(0, '', {'workflow_full_defination':  workflow_result})

    @user_permission_check('workflow_admin,admin', workflow_id_source='url')
    def patch(self, request, *args, **kwargs):
        """
        修改工作流
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_id = kwargs.get('workflow_id')
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')

        try:
            workflow_base_service_ins.update_workflow(operator_id, tenant_id, workflow_id, request_data_dict)
            return api_response(0, "", dict(workflow_id=workflow_id))
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")


        

    @user_permission_check('workflow_admin')
    def delete(self, request, *args, **kwargs):
        """
        删除工作流
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_name = request.META.get('HTTP_APPNAME')
        workflow_id = kwargs.get('workflow_id')
        # 判断是否有工作流的权限
        app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        flag, result = workflow_base_service_ins.delete_workflow(workflow_id)
        if flag is False:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {}
        return api_response(code, msg, data)
    

class WorkflowTicketCreationFormView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket creation form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        version_name = request.GET.get('version_name', '')
        try:
            result = workflow_base_service_ins.get_ticket_creation_form(workflow_id, tenant_id, operator_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, '', dict(form_schema={'component_info_list': result}))
    

class WorkflowTicketCreationActionsView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket creation actions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        version_name = request.GET.get('version_name', '')
        try:
            result = workflow_base_service_ins.get_ticket_creation_actions(workflow_id, tenant_id, operator_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, '', dict(actions=result))


##################  below ar waiting for update




class WorkflowUserAdminView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        获取用户管理的工作流信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.META.get('HTTP_USERNAME')
        flag, result = workflow_base_service_ins.get_workflow_manage_list(username)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', result.get('workflow_list'))


class WorkflowInitView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        获取工作流初始状态信息，包括状态详情以及允许的transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        # 判断是否有工作流的权限
        app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')

        if not (workflow_id and username):
            return api_response(-1, '请提供username或workflow_id', '')
        flag, state_result = workflow_state_service_ins.get_workflow_init_state(workflow_id)
        if flag is not False:
            code, msg, data = 0, '', state_result
        else:
            code, msg, data = -1, state_result, ''
        return api_response(code, msg, data)





class WorkflowTransitionView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        'source_state_id': And(int, lambda n: n != 0, error='source_state_id is needed and should be an integer'),
        'attribute_type_id': And(int, lambda n: n != 0, error='attribute_type_id is needed and should be an integer'),

        Optional('alert_enable'): int,
        Optional('field_require_check'): int,
        Optional('alert_text'): str,
        Optional('destination_state_id'): int,
        Optional('timer'): int,
        Optional('condition_expression'): str,
        Optional('transition_type_id'): int,

    })

    @user_permission_check('workflow_admin')
    def get(self, request, *args, **kwargs):
        """
        获取流转
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        query_value = request_data.get('search_value', '')
        # if not username:
        #     return api_response(-1, '请提供username', '')
        flag, result = workflow_transition_service_ins.get_transitions_serialize_by_workflow_id(workflow_id, per_page, page, query_value)

        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('workflow_transitions_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)

    @user_permission_check('workflow_admin')
    def post(self, request, *args, **kwargs):
        """
        新增流转
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_id = kwargs.get('workflow_id')
        username = request.user.username
        name = request_data_dict.get('name', '')
        transition_type_id = int(request_data_dict.get('transition_type_id', 0))
        timer = int(request_data_dict.get('timer', 0))
        source_state_id = int(request_data_dict.get('source_state_id', 0))
        destination_state_id = int(request_data_dict.get('destination_state_id', 0))
        condition_expression = request_data_dict.get('condition_expression', '')
        attribute_type_id = int(request_data_dict.get('attribute_type_id', 0))
        field_require_check = int(request_data_dict.get('field_require_check', 0))
        alert_enable = int(request_data_dict.get('alert_enable', 0))
        alert_text = request_data_dict.get('alert_text', '')
        flag, result = workflow_transition_service_ins.add_workflow_transition(workflow_id, name, transition_type_id, timer, source_state_id,
                                               destination_state_id, condition_expression, attribute_type_id,
                                               field_require_check, alert_enable, alert_text, username)
        if flag is not False:
            data = dict(value=dict(transition_id=result.get('transition_id')))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)


class WorkflowTransitionDetailView(BaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        'source_state_id': And(int, lambda n: n != 0, error='source_state_id is needed'),
        'attribute_type_id': And(int, lambda n: n != 0, error='attribute_type_id is needed'),
        Optional('transition_type_id'): int,
        Optional('alert_enable'): int,
        Optional('field_require_check'): int,
        Optional('alert_text'): str,
        Optional('destination_state_id'): int,
        Optional('timer'): int,
        Optional('condition_expression'): str,
    })

    @user_permission_check('workflow_admin')
    def patch(self, request, *args, **kwargs):
        """
        编辑
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_id = kwargs.get('workflow_id')
        app_name = request.META.get('HTTP_APPNAME')
        username = request.user.username
        name = request_data_dict.get('name', '')
        transition_type_id = int(request_data_dict.get('transition_type_id', 0))
        timer = int(request_data_dict.get('timer', 0))
        source_state_id = int(request_data_dict.get('source_state_id', 0))
        destination_state_id = int(request_data_dict.get('destination_state_id', 0))
        condition_expression = request_data_dict.get('condition_expression', '')
        attribute_type_id = int(request_data_dict.get('attribute_type_id', 0))
        field_require_check = int(request_data_dict.get('field_require_check', 0))
        alert_enable = int(request_data_dict.get('alert_enable', 0))
        alert_text = request_data_dict.get('alert_text', '')
        transition_id = kwargs.get('transition_id')
        flag, result = workflow_transition_service_ins.edit_workflow_transition(transition_id, workflow_id, name,
                                                                          transition_type_id, timer, source_state_id,
                                                                          destination_state_id, condition_expression,
                                                                          attribute_type_id, field_require_check,
                                                                          alert_enable, alert_text)
        if flag is not False:
            data = {}
            code, msg, = 0, ''
        else:
            code, data, msg = -1, {}, ''
        return api_response(code, msg, data)

    @user_permission_check('workflow_admin')
    def delete(self, request, *args, **kwargs):
        """
        删除transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        transition_id = kwargs.get('transition_id')
        flag, result = workflow_transition_service_ins.del_workflow_transition(transition_id)
        if flag is not False:
            data = {}
            code, msg, = 0, ''
        else:
            code, data, msg = -1, {}, ''
        return api_response(code, msg, data)


class StateView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        获取状态详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        state_id = kwargs.get('state_id')
        request_data = request.GET
        username = request.META.get('HTTP_USERNAME')
        if not username:
            return api_response(-1, '请提供username', '')

        flag, state_info_dict = workflow_state_service_ins.get_restful_state_info_by_id(state_id)
        if flag is not False:
            code, data, msg = 0, state_info_dict, ''
        else:
            code, data, msg = -1, {}, state_info_dict
        return api_response(code, msg, data)


class WorkflowStateView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        'order_id': And(int, error='order_id is needed'),
        'type_id': And(int, error='type_id is needed'),
        'participant_type_id': int,
        'distribute_type_id': And(int, lambda n: n != 0, error='distribute_type_id is needed'),
        Optional('remember_last_man_enable'): int,
        Optional('state_field_str'): str,
        Optional('label'): str,
        Optional(str): object
    })

    def get(self, request, *args, **kwargs):
        """
        获取工作流拥有的state列表信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        # if not username:
        #     return api_response(-1, '请提供username', '')
        flag, result = workflow_state_service_ins.get_workflow_states_serialize(workflow_id, per_page, page, search_value)

        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('workflow_states_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg,  = 0, ''
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)

    @user_permission_check('workflow_admin')
    def post(self, request, *args, **kwargs):
        """
        新增状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_data = {}
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        is_hidden = request_data_dict.get('is_hidden', 0)
        order_id = int(request_data_dict.get('order_id', 0))
        type_id = int(request_data_dict.get('type_id', 0))
        remember_last_man_enable = int(request_data_dict.get('remember_last_man_enable', 0))
        enable_retreat = int(request_data_dict.get('enable_retreat', 0))
        participant_type_id = int(request_data_dict.get('participant_type_id', 0))

        participant = request_data_dict.get('participant', '')
        distribute_type_id = int(request_data_dict.get('distribute_type_id', 1))
        state_field_str = request_data_dict.get('state_field_str', '')
        label = request_data_dict.get('label', '')
        workflow_id = kwargs.get('workflow_id')

        flag, result = workflow_state_service_ins.add_workflow_state(
            workflow_id, name, is_hidden, order_id, type_id, remember_last_man_enable, participant_type_id,
            participant, distribute_type_id, state_field_str, label, username, enable_retreat)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', {'state_id': result.get('workflow_state_id')}
        return api_response(code, msg, data)


class WorkflowSimpleStateView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        获取工作流状态列表(简单信息)
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        flag, result = workflow_state_service_ins.get_workflow_states_serialize(workflow_id, per_page, page,
                                                                                search_value, simple=True)

        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('workflow_states_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)


class WorkflowStateDetailView(BaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        'order_id': And(int, error='order_id is needed'),
        'type_id': And(int, error='type_id is needed'),
        'participant_type_id': int,
        'distribute_type_id': And(int, lambda n: n != 0, error='distribute_type_id is needed'),
        Optional('remember_last_man_enable'): int,
        Optional('state_field_str'): str,
        Optional('label'): str,
        str: object
    })

    @user_permission_check('workflow_admin')
    def patch(self, request, *args, **kwargs):
        """
        编辑状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_data = {}
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        is_hidden = request_data_dict.get('is_hidden', 0)
        order_id = int(request_data_dict.get('order_id', 0))
        type_id = int(request_data_dict.get('type_id', 0))
        remember_last_man_enable = int(request_data_dict.get('remember_last_man_enable', 0))
        enable_retreat = int(request_data_dict.get('enable_retreat', 0))
        participant_type_id = int(request_data_dict.get('participant_type_id', 0))

        participant = request_data_dict.get('participant', '')
        distribute_type_id = int(request_data_dict.get('distribute_type_id', 1))
        state_field_str = request_data_dict.get('state_field_str', '')
        label = request_data_dict.get('label', '')
        workflow_id = kwargs.get('workflow_id')
        state_id = kwargs.get('state_id')

        flag, result = workflow_state_service_ins.edit_workflow_state(
            state_id, workflow_id, name, is_hidden, order_id, type_id, remember_last_man_enable, participant_type_id,
            participant, distribute_type_id, state_field_str, label, enable_retreat)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', {}
        return api_response(code, msg, data)

    @user_permission_check('workflow_admin')
    def delete(self, request, *args, **kwargs):
        """
        删除状态
        delete state
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_name = request.META.get('HTTP_APPNAME')
        state_id = kwargs.get('state_id')
        flag, result = workflow_state_service_ins.del_workflow_state(state_id)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', {}
        return api_response(code, msg, data)


# class WorkflowRunScriptView(BaseView):
#     @user_permission_check('workflow_admin')
#     def get(self, request, *args, **kwargs):
#         """
#         获取工作流执行脚本列表
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         request_data = request.GET
#         username = request.META.get('HTTP_USERNAME')
#         if not username:
#             username = request.user.username
#         search_value = request_data.get('search_value', '')
#         per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
#         page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
#         if not username:
#             return api_response(-1, '请提供username', '')
#         flag, result = workflow_run_script_service_ins.get_run_script_list(search_value, page, per_page)
#
#         if flag is not False:
#             paginator_info = result.get('paginator_info')
#             data = dict(value=result.get('run_script_result_restful_list'), per_page=paginator_info.get('per_page'), page=paginator_info.get('page'),
#                         total=paginator_info.get('total'))
#             code, msg, = 0, ''
#         else:
#             code, data = -1, ''
#         return api_response(code, msg, data)
#
#     @user_permission_check('workflow_admin')
#     def post(self, request, *args, **kwargs):
#         """
#         新增脚本
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         file_obj = request.FILES.get('file')
#         if file_obj:  # 处理附件上传到方法
#             import os
#             import uuid
#             from django.conf import settings
#             script_file_name = "workflow_script/{}.py".format(str(uuid.uuid1()))
#             upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
#             with open(upload_file, 'wb') as new_file:
#                 for chunk in file_obj.chunks():
#                     new_file.write(chunk)
#         script_name = request.POST.get('script_name', '')
#         script_desc = request.POST.get('script_desc', '')
#         is_active = request.POST.get('is_active', '0')
#         flag, result = workflow_run_script_service_ins.add_run_script(script_name, script_file_name, script_desc, is_active, request.user.username)
#         if flag is not False:
#             data, code, msg = dict(script_id=result.get('script_id')), 0, ''
#         else:
#             code, data, msg = -1, {}, result
#         return api_response(code, msg, data)
#
#
# class WorkflowRunScriptDetailView(BaseView):
#     @user_permission_check('workflow_admin')
#     def post(self, request, *args, **kwargs):
#         """
#         修改脚本,本来准备用patch的。但是发现非json提交过来获取不到数据(因为要传文件，所以不能用json)
#         update script
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         file_obj = request.FILES.get('file')
#         if file_obj:  # 处理附件上传到方法
#             import os
#             import uuid
#             from django.conf import settings
#             script_file_name = "workflow_script/{}.py".format(str(uuid.uuid1()))
#             upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
#             with open(upload_file, 'wb') as new_file:
#                 for chunk in file_obj.chunks():
#                     new_file.write(chunk)
#         else:
#             script_file_name = None
#         run_script_id = kwargs.get('run_script_id')
#         script_name = request.POST.get('script_name', '')
#         script_desc = request.POST.get('script_desc', '')
#         is_active = request.POST.get('is_active', '0')
#         flag, result = workflow_run_script_service_ins.edit_run_script(run_script_id, script_name, script_file_name, script_desc, is_active)
#         if flag is not False:
#             code, msg, data = 0, '', {}
#         else:
#             code, data, msg = -1, {}, result
#         return api_response(code, msg, data)
#
#     @user_permission_check('workflow_admin')
#     def delete(self, request, *args, **kwargs):
#         """
#         删除脚本，本操作不删除对应的脚本文件，只标记记录
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         run_script_id = kwargs.get('run_script_id')
#         result, msg = workflow_run_script_service_ins.del_run_script(run_script_id)
#         if result is not False:
#             code, msg, data = 0, '', {}
#         else:
#             code, data = -1, {}
#         return api_response(code, msg, data)
#
# class SimpleWorkflowCustomNoticeView(BaseView):
#     @user_permission_check('workflow_admin')
#     def get(self, request, *args, **kwargs):
#         """
#         获取通知列表(简单信息)
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         request_data = request.GET
#         search_value = request_data.get('search_value', '')
#         per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
#         page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
#         result, msg = workflow_custom_notice_service_ins.get_notice_list(search_value, page, per_page, simple=True)
#
#         if result is not False:
#             data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
#             code, msg, = 0, ''
#         else:
#             code, data = -1, ''
#         return api_response(code, msg, data)
#
#
# class WorkflowCustomNoticeView(BaseView):
#     post_schema = Schema({
#         'name': And(str, lambda n: n != '', error='name is needed'),
#         'type_id': And(int, error='type_id is needed'),
#         Optional('description'): str,
#         Optional('hook_url'): str,
#         Optional('hook_token'): str,
#         Optional('corpid'): str,
#         Optional('corpsecret'): str,
#         Optional('appkey'): str,
#         Optional('appsecret'): str,
#     })
#
#     @user_permission_check('admin')
#     def get(self, request, *args, **kwargs):
#         """
#         get worklfow custom notice list
#         获取工作流通知列表
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         request_data = request.GET
#         # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
#         username = request.META.get('HTTP_USERNAME')
#         if not username:
#             username = request.user.username
#         search_value = request_data.get('search_value', '')
#         per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
#         page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
#         if not username:
#             return api_response(-1, '请提供username', '')
#         result, msg = workflow_custom_notice_service_ins.get_notice_list(search_value, page, per_page)
#
#         if result is not False:
#             data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
#             code, msg, = 0, ''
#         else:
#             code, data = -1, ''
#         return api_response(code, msg, data)
#
#     @user_permission_check('admin')
#     def post(self, request, *args, **kwargs):
#         """
#         add notice record
#         新增通知记录
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#
#         json_str = request.body.decode('utf-8')
#         if not json_str:
#             return api_response(-1, 'post参数为空', {})
#         request_data_dict = json.loads(json_str)
#
#         creator = request.META.get('HTTP_USERNAME')
#         name = request_data_dict.get('name', '')
#         description = request_data_dict.get('description', '')
#         type_id = request_data_dict.get('type_id', 1)
#         hook_url = request_data_dict.get('hook_url', '')
#         hook_token = request_data_dict.get('hook_token', '')
#         corpid = request_data_dict.get('corpid', '')
#         corpsecret = request_data_dict.get('corpsecret', '')
#         appkey = request_data_dict.get('appkey', '')
#         appsecret = request_data_dict.get('appsecret', '')
#
#         flag, result = account_base_service_ins.admin_permission_check(creator)
#         if flag is False:
#             return api_response(-1, result, {})
#
#         result, msg = workflow_custom_notice_service_ins.add_custom_notice(
#             name, description, type_id, corpid, corpsecret, appkey, appsecret, hook_url, hook_token, creator)
#         if result is not False:
#             data = msg
#             code, msg,  = 0, ''
#         else:
#             code, data = -1, {}
#         return api_response(code, msg, data)
#
#
# class WorkflowCustomNoticeDetailView(BaseView):
#     patch_schema = Schema({
#         'name': And(str, lambda n: n != '', error='name is needed'),
#         'type_id': And(int, error='type_id is needed'),
#         Optional('description'): str,
#         Optional('hook_url'): str,
#         Optional('hook_token'): str,
#         Optional('corpid'): str,
#         Optional('corpsecret'): str,
#         Optional('appkey'): str,
#         Optional('appsecret'): str,
#     })
#
#     @user_permission_check('admin')
#     def patch(self, request, *args, **kwargs):
#         """
#         修改通知
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         notice_id = kwargs.get('notice_id')
#
#         json_str = request.body.decode('utf-8')
#         if not json_str:
#             return api_response(-1, 'post参数为空', {})
#         request_data_dict = json.loads(json_str)
#
#         name = request_data_dict.get('name', '')
#         description = request_data_dict.get('description', '')
#         type_id = request_data_dict.get('type_id', 1)
#         hook_url = request_data_dict.get('hook_url', '')
#         hook_token = request_data_dict.get('hook_token', '')
#         corpid = request_data_dict.get('corpid', '')
#         corpsecret = request_data_dict.get('corpsecret', '')
#         appkey = request_data_dict.get('appkey', '')
#         appsecret = request_data_dict.get('appsecret', '')
#
#         username = request.META.get('HTTP_USERNAME')
#
#
#         flag, result = account_base_service_ins.admin_permission_check(username)
#         if flag is False:
#             return api_response(-1, result, {})
#
#         result, msg = workflow_custom_notice_service_ins.update_custom_notice(
#             notice_id, name, description, type_id, corpid, corpsecret, appkey, appsecret, hook_url, hook_token)
#         if result is not False:
#             data = {}
#             code, msg, = 0, ''
#         else:
#             code, data = -1, {}
#         return api_response(code, msg, data)
#
#     @user_permission_check('admin')
#     def delete(self, request, *args, **kwargs):
#         """
#         删除自定义通知
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         notice_id = kwargs.get('notice_id')
#         result, msg = workflow_custom_notice_service_ins.del_custom_notice(notice_id)
#         if result is not False:
#             code, msg, data = 0, '', {}
#         else:
#             code, data = -1, {}
#         return api_response(code, msg, data)
#
#     @user_permission_check('admin')
#     def get(self, request, *args, **kwargs):
#         """
#         获取自定义通知详情
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         notice_id = kwargs.get('notice_id')
#         result, msg = workflow_custom_notice_service_ins.get_notice_detail(notice_id)
#         if result is not False:
#             code, msg, data = 0, '', dict(value=msg)
#         else:
#             code, data = -1, {}
#         return api_response(code, msg, data)
#
#
# class WorkflowCustomFieldView(BaseView):
#     post_schema = Schema({
#         'field_key': And(str, lambda n: n != '', error='field_key is needed'),
#         'field_name': And(str, lambda n: n != '', error='field_name is needed'),
#         'field_type_id': And(int, lambda n: n != 0, error='field_type_id is needed and should be a number'),
#         'order_id': And(int, error='order_id is needed and should be a number'),
#         Optional('description'): str,
#         Optional('label'): str,
#         Optional('field_template'): str,
#         Optional('default_value'): str,
#         Optional('boolean_field_display'): str,
#         Optional('field_choice'): str,
#     })
#
#     def get(self, request, *args, **kwargs):
#         """
#         获取工作流自定义字段列表
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         request_data = request.GET
#         # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
#         username = request.META.get('HTTP_USERNAME')
#         if not username:
#             username = request.user.username
#         search_value = request_data.get('search_value', '')
#         per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
#         page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
#         if not username:
#             return api_response(-1, '请提供username', '')
#         flag, result = workflow_custom_field_service_ins.get_workflow_custom_field_list(kwargs.get('workflow_id'), search_value, page, per_page)
#
#         if flag is not False:
#             paginator_info = result.get('paginator_info')
#             data = dict(value=result.get('workflow_custom_field_result_restful_list'),
#                         per_page=paginator_info.get('per_page'), page=paginator_info.get('page'),
#                         total=paginator_info.get('total'))
#             code, msg = 0, ''
#         else:
#             code, data, msg = -1, {}, ''
#         return api_response(code, msg, data)
#
#     @user_permission_check('workflow_admin')
#     def post(self, request, *args, **kwargs):
#         """
#         新增工作流自定义字段
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         app_name = request.META.get('HTTP_APPNAME')
#         username = request.META.get('HTTP_USERNAME')
#         workflow_id = kwargs.get('workflow_id')
#         # 判断是否有工作流的权限
#         app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
#         if not app_permission:
#             return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
#         json_str = request.body.decode('utf-8')
#         if not json_str:
#             return api_response(-1, 'post参数为空', {})
#         request_data_dict = json.loads(json_str)
#         field_key = request_data_dict.get('field_key', '')
#         field_name = request_data_dict.get('field_name', '')
#         field_type_id = request_data_dict.get('field_type_id', '')
#         order_id = int(request_data_dict.get('order_id', 0))
#         label = request_data_dict.get('label', '')
#         description = request_data_dict.get('description', '')
#         field_template = request_data_dict.get('field_template', '')
#         default_value = request_data_dict.get('default_value', '')
#         boolean_field_display = request_data_dict.get('boolean_field_display', '')
#         field_choice = request_data_dict.get('field_choice', '')
#         flag, result = workflow_custom_field_service_ins.add_record(workflow_id, field_type_id, field_key, field_name, order_id,
#                                                              default_value, description, field_template,
#                                                              boolean_field_display, field_choice, label, username)
#
#         if flag is not False:
#             data = dict(value={'custom_field_id': result.get('custom_field_id')})
#             code, msg, = 0, ''
#         else:
#             code, data, msg = -1, {}, result
#         return api_response(code, msg, data)
#
#
# class WorkflowCustomFieldDetailView(BaseView):
#     patch_schema = Schema({
#         'field_key': And(str, lambda n: n != '', error='field_key is needed'),
#         'field_name': And(str, lambda n: n != '', error='field_name is needed'),
#         'field_type_id': And(int, lambda n: n != 0, error='field_type_id is needed and should be a number'),
#         'order_id': And(int, error='order_id is needed and should be a number'),
#         Optional('description'): str,
#         Optional('label'): str,
#         Optional('field_template'): str,
#         Optional('default_value'): str,
#         Optional('boolean_field_display'): str,
#         Optional('field_choice'): str,
#     })
#
#     @user_permission_check('workflow_admin')
#     def patch(self, request, *args, **kwargs):
#         """
#         更新自定义字段
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         custom_field_id = kwargs.get('custom_field_id')
#         app_name = request.META.get('HTTP_APPNAME')
#         username = request.META.get('HTTP_USERNAME')
#         workflow_id = kwargs.get('workflow_id')
#         # 判断是否有工作流的权限
#         app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
#         if not app_permission:
#             return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
#         json_str = request.body.decode('utf-8')
#         if not json_str:
#             return api_response(-1, 'post参数为空', {})
#         request_data_dict = json.loads(json_str)
#         field_key = request_data_dict.get('field_key', '')
#         field_name = request_data_dict.get('field_name', '')
#         field_type_id = request_data_dict.get('field_type_id', '')
#         order_id = int(request_data_dict.get('order_id', 0))
#         label = request_data_dict.get('label', '')
#         description = request_data_dict.get('description', '')
#         field_template = request_data_dict.get('field_template', '')
#         default_value = request_data_dict.get('default_value', '')
#         boolean_field_display = request_data_dict.get('boolean_field_display', '')
#         field_choice = request_data_dict.get('field_choice', '')
#         result, msg = workflow_custom_field_service_ins.edit_record(custom_field_id, workflow_id, field_type_id, field_key, field_name, order_id,
#                                                             default_value, description, field_template,
#                                                             boolean_field_display, field_choice, label)
#
#         if result is not False:
#             code, msg, data = 0, '', {}
#         else:
#             code, data = -1, ''
#         return api_response(code, msg, data)
#
#     @user_permission_check('workflow_admin')
#     def delete(self, request, *args, **kwargs):
#         """删除记录"""
#         app_name = request.META.get('HTTP_APPNAME')
#         username = request.META.get('HTTP_USERNAME')
#         workflow_id = kwargs.get('workflow_id')
#         custom_field_id = kwargs.get('custom_field_id')
#         # 判断是否有工作流的权限
#         app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
#         if not app_permission:
#             return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
#         flag, result = workflow_custom_field_service_ins.delete_record(custom_field_id)
#         if flag is not False:
#             data = dict(value={'custom_field_id': result})
#             code, msg, = 0, ''
#         else:
#             code, data = -1, ''
#         return api_response(code, msg, data)
#
#
# class WorkflowSimpleDescriptionView(BaseView):
#     def get(self, request, *args, **kwargs):
#         """
#         简单描述，可用于生成流程图
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         workflow_id = kwargs.get('workflow_id')
#
#         flag, workflow_simple_description = workflow_base_service_ins.get_simple_description(workflow_id)
#         if flag is False:
#             code, data, msg = -1, {}, workflow_simple_description
#         else:
#             code, data, msg = 0, workflow_simple_description, ''
#         return api_response(code, msg, data)
#
#
# class WorkflowCanInterveneView(BaseView):
#     def get(self, request, *args, **kwargs):
#         """
#         是否有干预权限
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         workflow_id = kwargs.get('workflow_id')
#         username = request.META.get('HTTP_USERNAME')
#
#         flag, result = workflow_base_service_ins.can_intervene(workflow_id, username)
#         if flag is False:
#             code, data, msg = -1, {}, result
#         else:
#             code, data, msg = 0, {'can_intervene': result}, ''
#
#         return api_response(code, msg, data)
#
#
# class WorkflowStatisticsView(BaseView):
#     @user_permission_check('workflow_admin')
#     def get(self, request, *args, **kwargs):
#         """
#         工作流统计
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         workflow_id = kwargs.get('workflow_id')
#         request_data = request.GET
#         start_time = request_data.get('start_time', '')
#         end_time = request_data.get('end_time', '')
#
#
#         flag, workflow_statistics = workflow_base_service_ins.get_statistics(workflow_id, start_time, end_time)
#         if flag is False:
#             code, data, msg = -1, {}, workflow_statistics
#         else:
#             code, data, msg = 0, workflow_statistics, ''
#         return api_response(code, msg, data)
