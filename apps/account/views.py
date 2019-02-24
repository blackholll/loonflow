from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from service.account.account_base_service import AccountBaseService
from service.format_response import api_response


@method_decorator(login_required, name='dispatch')
class LoonUserView(View):
    def get(self, request, *args, **kwargs):
        """
        获取用户列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        user_result_object_list, msg = AccountBaseService().get_user_list(search_value, page, per_page)
        if user_result_object_list is not False:
            data = dict(value=user_result_object_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonRoleView(View):
    def get(self, request, *args, **kwargs):
        """
        用户角色列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        role_result_object_list, msg = AccountBaseService().get_role_list(search_value, page, per_page)
        if role_result_object_list is not False:
            data = dict(value=role_result_object_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonDeptView(View):
    def get(self, request, *args, **kwargs):
        """
        用户角色列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        dept_result_object_list, msg = AccountBaseService().get_dept_list(search_value, page, per_page)
        if dept_result_object_list is not False:
            data = dict(value=dept_result_object_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)
