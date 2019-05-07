import json

from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
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


@method_decorator(login_required, name='dispatch')
class LoonAppTokenView(View):
    def get(self, request, *args, **kwargs):
        """
        调用权限列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        token_result_object_list, msg = AccountBaseService().get_token_list(search_value, page, per_page)
        if token_result_object_list is not False:
            data = dict(value=token_result_object_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增调用权限记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        app_name = request_data_dict.get('app_name', '')
        ticket_sn_prefix = request_data_dict.get('ticket_sn_prefix', '')
        workflow_ids = request_data_dict.get('workflow_ids', '')
        # username = request.user.username
        username = request.META.get('HTTP_USERNAME')
        flag, msg = AccountBaseService().add_token_record(app_name, ticket_sn_prefix, workflow_ids, username)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {'id': msg}

        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonAppTokenDetailView(View):
    def get(self, request, *args, **kwargs):
        """
        获取token详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_token_id = kwargs.get('app_token_id')
        pass

    def patch(self, request, *args, **kwargs):
        """
        编辑token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_token_id = kwargs.get('app_token_id')
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'patch参数为空', {})
        request_data_dict = json.loads(json_str)
        app_name = request_data_dict.get('app_name', '')
        ticket_sn_prefix = request_data_dict.get('ticket_sn_prefix', '')
        workflow_ids = request_data_dict.get('workflow_ids', '')
        flag, msg = AccountBaseService.update_token_record(app_token_id, app_name, ticket_sn_prefix, workflow_ids)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {}

        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_token_id = kwargs.get('app_token_id')
        flag, msg = AccountBaseService.del_token_record(app_token_id)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {}
        return api_response(code, msg, data)


class LoonLoginView(View):
    def post(self, request, *args, **kwargs):
        """
        登录验证
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'patch参数为空', {})
        request_data_dict = json.loads(json_str)
        username = request_data_dict.get('username', '')
        password = request_data_dict.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return api_response(0, '', {})
        else:
            return api_response(-1, 'username or password is invalid', {})


class LoonLogoutView(View):
    def get(self, request, *args, **kwargs):
        """
        注销
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logout(request)
        return redirect('/manage')


class LoonUserRoleView(View):
    def get(self, request, *args, **kwargs):
        """
        用户角色信息
        """
        user_id = kwargs.get('user_id', 0)
        search_value = request.GET.get('search_value', '')
        role_info_list, msg = AccountBaseService.get_user_role_info_by_user_id(user_id, search_value)
        if role_info_list is not False:
            data = dict(value=role_info_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class LoonRoleUserView(View):
    def get(self, request, *args, **kwargs):
        """
        角色的用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id', 0)
        search_value = request.GET.get('search_value', '')
        user_info_list, msg = AccountBaseService.get_role_user_info_by_role_id(role_id, search_value)
        if user_info_list is not False:
            data = dict(value=user_info_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)
