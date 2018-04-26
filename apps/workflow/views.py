from django.views import View
from service.format_response import api_response
from service.workflow.workflow_state_service import WorkflowStateService


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
        username = request_data.get('username', '')
        result, msg = WorkflowStateService.get_restful_state_info_by_id(state_id)
        if result is not False:
            code, data = 0, result
        else:
            code, data = -1, ''
        return api_response(code, msg, data)