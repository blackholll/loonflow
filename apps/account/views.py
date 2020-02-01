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

        flag, result = AccountBaseService().get_user_list(search_value, page, per_page)
        if flag is not False:
            data = dict(value=result.get('user_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        add user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        username = request_data_dict.get('username')
        alias = request_data_dict.get('alias')
        email = request_data_dict.get('email')
        password = request_data_dict.get('password')
        phone = request_data_dict.get('phone')
        dept_id = int(request_data_dict.get('dept_id')) if request_data_dict.get('dept_id') else 0
        is_active = request_data_dict.get('is_active')
        is_admin = request_data_dict.get('is_admin')
        is_workflow_admin = request_data_dict.get('is_workflow_admin')
        creator = request.user.username
        flag, result = AccountBaseService().add_user(username, alias, email, phone, dept_id, is_active, is_admin, is_workflow_admin,
                                      creator, password)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', result
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonUserDetailView(View):
    def patch(self, request, *args, **kwargs):
        """
        edit user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        user_id = kwargs.get('user_id')
        request_data_dict = json.loads(json_str)
        username = request_data_dict.get('username')
        alias = request_data_dict.get('alias')
        email = request_data_dict.get('email')
        phone = request_data_dict.get('phone')
        dept_id = int(request_data_dict.get('dept_id')) if request_data_dict.get('dept_id') else 0
        is_active = request_data_dict.get('is_active')
        is_admin = request_data_dict.get('is_admin')
        is_workflow_admin = request_data_dict.get('is_workflow_admin')
        flag, result = AccountBaseService().edit_user(user_id, username, alias, email, phone, dept_id, is_active,
                                                      is_admin, is_workflow_admin)
        if flag is not False:
            code, msg, data = 0, '', {}
        else:
            code, msg, data = -1, result, {}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        delete user record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        operator = request.user.username
        flag, result = AccountBaseService().admin_permission_check(username=operator)
        if flag:
            flag, result = AccountBaseService().delete_user(user_id)
            if flag:
                code, msg, data = 0, '', {}
                return api_response(code, msg, data)
        code, msg, data = -1, result, {}
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
        flag, result = AccountBaseService().get_role_list(search_value, page, per_page)
        if flag is not False:
            data = dict(value=result.get('role_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
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
        flag, result = AccountBaseService().get_dept_list(search_value, page, per_page)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('dept_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
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
        flag, result = AccountBaseService().get_token_list(search_value, page, per_page)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('token_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
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
        flag, result = AccountBaseService().add_token_record(app_name, ticket_sn_prefix, workflow_ids, username)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {'id': result.get('app_token_id')}

        return api_response(code, result, data)


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
        flag, result = AccountBaseService.get_user_role_info_by_user_id(user_id, search_value)
        if flag is not False:
            data = dict(value=result.get('role_result_format_list'), per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'), total=result.get('paginator_info').get('total'))
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
        # user_info_list, msg = AccountBaseService.get_role_user_info_by_role_id(role_id, search_value)
        flag, result = AccountBaseService.get_role_user_info_by_role_id(role_id, search_value)

        if flag is not False:
            data = dict(value=result.get('user_result_format_list'), per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'), total=result.get('paginator_info').get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class LoonUserResetPasswordView(View):
    def post(self, request, *args, **kwargs):
        """
        重置密码
        :param requesdt:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        operator = request.user.username
        # operator admin permission check
        flag, result = AccountBaseService().admin_permission_check(username=operator)
        if flag is False:
            return api_response(-1, result, {})
        flag, result = AccountBaseService().admin_or_workflow_admin_check(user_id=user_id)
        if flag is False:
            return api_response(-1, result, {})
        flag, result = AccountBaseService().reset_password(user_id=user_id)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, result, {})
