from django.views import View
from service.format_response import api_response
from service.workflow.workflow_base_service import WorkflowBaseService
from service.workflow.workflow_state_service import WorkflowStateService


class WorkflowView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        name = request_data.get('name', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制

        workflow_result_restful_list, msg = WorkflowBaseService.get_workflow_list(name, page, per_page)
        if workflow_result_restful_list is not False:
            data = dict(value=workflow_result_restful_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowInitView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流初始状态信息，包括状态详情以及允许的transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制

        if not (workflow_id and username):
            return api_response(-1, '请提供username', '')
        state_result, msg = WorkflowStateService.get_workflow_init_state(workflow_id)
        if state_result is not False:
            code, msg, data = 0, '', state_result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class StateView(View):
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
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        if not username:
            return api_response(-1, '请提供username', '')

        result, msg = WorkflowStateService.get_restful_state_info_by_id(state_id)
        if result is not False:
            code, data = 0, result
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowStateView(View):
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
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        if not username:
            return api_response(-1, '请提供username', '')
        result, msg = WorkflowStateService.get_workflow_states_serialize(workflow_id, per_page, page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)
