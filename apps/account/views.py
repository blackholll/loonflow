import json

import jwt
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from service.account.account_base_service import account_base_service_ins
from service.format_response import api_response
from apps.loon_base_view import LoonBaseView
from schema import Schema, Regex, And, Or, Use, Optional

from service.permission.manage_permission import manage_permission_check


@method_decorator(login_required, name='dispatch')
class LoonUserView(LoonBaseView):
    post_schema = Schema({
        'username': And(str, lambda n: n != '', error='username is needed'),
        'alias': And(str, lambda n: n != '', error='alias is needed'),
        'email': And(str, lambda n: n != '', error='alias is needed'),
        Optional('password'): str,
        'phone': str,
        'dept_ids': str,
        'type_id': int,
        'is_active': Use(bool),

    })

    @manage_permission_check('workflow_admin')
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

        flag, result = account_base_service_ins.get_user_list(search_value, page, per_page)
        if flag is not False:
            data = dict(value=result.get('user_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
            code, msg,  = 0, ''
        else:
            code, data, msg = -1, '', result
        return api_response(code, msg, data)

    @manage_permission_check('admin')
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
        dept_ids = request_data_dict.get('dept_ids')
        is_active = request_data_dict.get('is_active')
        type_id = request_data_dict.get('type_id')
        creator = request.user.username
        flag, result = account_base_service_ins.add_user(username, alias, email, phone, dept_ids, is_active, type_id, creator, password)
        if flag is False:
            code, msg, data = -1, result, {}
        else:
            code, msg, data = 0, '', result
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonUserDetailView(LoonBaseView):
    patch_schema = Schema({
        'username': And(str, lambda n: n != ''),
        'alias': And(str, lambda n: n != ''),
        'email': And(str, lambda n: n != ''),
        Optional('password'): str,
        'phone': str,
        'dept_ids': str,
        'is_active': Use(bool),
        'type_id': int
    })

    @manage_permission_check('admin')
    def patch(self, request, *args, **kwargs):
        """
        edit user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        user_id = kwargs.get('user_id')
        request_data_dict = json.loads(json_str)
        username = request_data_dict.get('username')
        alias = request_data_dict.get('alias')
        email = request_data_dict.get('email')
        phone = request_data_dict.get('phone')
        dept_ids = request_data_dict.get('dept_ids')
        type_id = request_data_dict.get('type_id')

        is_active = request_data_dict.get('is_active')
        flag, result = account_base_service_ins.edit_user(user_id, username, alias, email, phone, dept_ids, is_active,
                                                          type_id)
        if flag is not False:
            code, msg, data = 0, '', {}
        else:
            code, msg, data = -1, result, {}
        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete user record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        flag, result = account_base_service_ins.delete_user(user_id)
        if flag:
            code, msg, data = 0, '', {}
            return api_response(code, msg, data)
        code, msg, data = -1, result, {}
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonRoleView(LoonBaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != ''),
        Optional('description'): str,
        Optional('label'): str,
    })

    @manage_permission_check('admin')
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
        flag, result = account_base_service_ins.get_role_list(search_value, page, per_page)
        if flag is not False:
            data = dict(value=result.get('role_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        add role
        新增角色
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        description = request_data_dict.get('description', '')
        label = request_data_dict.get('label', '')
        creator = request.user.username

        flag, result = account_base_service_ins.add_role(name=name, description=description, label=label,
                                                         creator=creator)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, result, {})


@method_decorator(login_required, name='dispatch')
class LoonRoleDetailView(LoonBaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is need'),
        Optional('description'): str,
        Optional('label'): str,
    })

    @manage_permission_check('admin')
    def patch(self, request, *args, **kwargs):
        """
        update role
        更新角色信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        description = request_data_dict.get('description')
        label = request_data_dict.get('label')
        flag, result = account_base_service_ins.update_role(role_id, name, description, label)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})

    @manage_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete role
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id')
        flag, result = account_base_service_ins.delete_role(role_id)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})


@method_decorator(login_required, name='dispatch')
class LoonDeptView(LoonBaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != ''),
        Optional('parent_dept_id'): int,
        Optional('leader'): str,
        Optional('approver'): str,
        Optional('label'): str,
    })

    @manage_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        部门列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        flag, result = account_base_service_ins.get_dept_list(search_value, page, per_page)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('dept_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        新增部门
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        parent_dept_id = request_data_dict.get('parent_dept_id')
        leader = request_data_dict.get('leader')
        approver = request_data_dict.get('approver')

        label = request_data_dict.get('label')
        creator = request.user.username
        flag, result = account_base_service_ins.add_dept(name, parent_dept_id, leader, approver, label, creator)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, result, {})


@method_decorator(login_required, name='dispatch')
class LoonDeptDetailView(LoonBaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is need'),
        Optional('parent_dept_id'): int,
        Optional('leader'): str,
        Optional('approver'): str,
        Optional('label'): str,
    })

    @manage_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete dept
        删除部门
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator = request.user.username
        dept_id = kwargs.get('dept_id')
        flag, result = account_base_service_ins.delete_dept(dept_id)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})

    @manage_permission_check('admin')
    def patch(self, request, *args, **kwargs):
        """
        更新部门
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_id = kwargs.get('dept_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        parent_dept_id = request_data_dict.get('parent_dept_id')
        leader = request_data_dict.get('leader')
        approver = request_data_dict.get('approver')
        label = request_data_dict.get('label')

        flag, result = account_base_service_ins.update_dept(dept_id,name, parent_dept_id, leader,
                                                            approver, label)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})


class LoonSimpleDeptView(LoonBaseView):
    def get(self, request, *args, **kwargs):
        """
        部门列表，简单信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        flag, result = account_base_service_ins.get_dept_list(search_value, page, per_page, simple=True)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('dept_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonAppTokenView(LoonBaseView):
    post_schema = Schema({
        'app_name': And(str, lambda n: n != '', error='app_name is needed'),
        Optional('ticket_sn_prefix'): str,
        Optional('workflow_ids'): str,
    })

    @manage_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        call api permission
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
        flag, result = account_base_service_ins.get_token_list(search_value, page, per_page)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('token_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, '', result
        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        add call api permission
        新增调用权限记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        app_name = request_data_dict.get('app_name', '')
        ticket_sn_prefix = request_data_dict.get('ticket_sn_prefix', '')
        workflow_ids = request_data_dict.get('workflow_ids', '')
        username = request.user.username
        flag, result = account_base_service_ins.add_token_record(app_name, ticket_sn_prefix, workflow_ids, username)

        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {'id': result.get('app_token_id')}

        return api_response(code, result, data)


@method_decorator(login_required, name='dispatch')
class LoonSimpleAppTokenView(LoonBaseView):
    @manage_permission_check('workflow_admin')
    def get(self, request, *args, **kwargs):
        """
        call api permission
        调用权限列表（返回简单数据）
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        flag, result = account_base_service_ins.get_token_list(search_value, page, per_page, simple=True)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('token_result_object_format_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, '', result
        return api_response(code, msg, data)



@method_decorator(login_required, name='dispatch')
class LoonAppTokenDetailView(LoonBaseView):
    patch_schema = Schema({
        Optional('ticket_sn_prefix'): str,
        Optional('workflow_ids'): str,
    })

    @manage_permission_check('admin')
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
        request_data_dict = json.loads(json_str)
        ticket_sn_prefix = request_data_dict.get('ticket_sn_prefix', '')
        workflow_ids = request_data_dict.get('workflow_ids', '')
        flag, msg = account_base_service_ins.update_token_record(app_token_id, ticket_sn_prefix, workflow_ids)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {}

        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        删除记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_token_id = kwargs.get('app_token_id')
        flag, msg = account_base_service_ins.del_token_record(app_token_id)
        if flag is False:
            code, data = -1, {}
        else:
            code, data = 0, {}
        return api_response(code, msg, data)


class LoonLoginView(LoonBaseView):
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
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return api_response(-1, e.__str__(), {})

        if user is not None:
            login(request, user)
            return api_response(0, '', {})
        else:
            return api_response(-1, 'username or password is invalid', {})


class LoonLogoutView(LoonBaseView):
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


class LoonJwtLoginView(LoonBaseView):
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'invalid args', {})
        request_data_dict = json.loads(json_str)
        username = request_data_dict.get('username', '')
        password = request_data_dict.get('password', '')
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return api_response(-1, e.__str__(), {})
        if user is not None:
            # todo: get jwt
            flag, jwt_info = account_base_service_ins.get_user_jwt(username)
            if flag is False:
                return api_response(-1, '', {})
            else:
                login(request, user)
                return api_response(0, '', {'jwt': jwt_info})
        else:
            return api_response(-1, 'username or password is invalid', {})


@method_decorator(login_required, name='dispatch')
class LoonUserRoleView(LoonBaseView):
    @manage_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        用户角色信息
        """
        user_id = kwargs.get('user_id', 0)
        search_value = request.GET.get('search_value', '')
        flag, result = account_base_service_ins.get_user_role_info_by_user_id(user_id, search_value)
        if flag is not False:
            data = dict(value=result.get('role_result_format_list'), per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'), total=result.get('paginator_info').get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


@method_decorator(login_required, name='dispatch')
class LoonRoleUserView(LoonBaseView):
    post_schema = Schema({
        'user_id': And(int, error='user_id is needed and should be int')
    })

    @manage_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        角色的用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id', 0)
        request_data = request.GET
        page = int(request_data.get('page', 1))
        per_page = int(request_data.get('per_page', 10))
        search_value = request.GET.get('search_value', '')
        flag, result = account_base_service_ins.get_role_user_info_by_role_id(role_id, search_value, page, per_page)

        if flag is not False:
            data = dict(value=result.get('user_result_format_list'), per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'), total=result.get('paginator_info').get('total'))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    @manage_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        add role's user
        新增角色用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id', 0)
        creator = request.user.username
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        user_id = request_data_dict.get('user_id', 0)

        flag, result = account_base_service_ins.add_role_user(role_id, user_id, creator)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})


@method_decorator(login_required, name='dispatch')
class LoonRoleUserDetailView(LoonBaseView):
    @manage_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
         delete role's user
         删除角色用户
         :param request:
         :param args:
         :param kwargs:
         :return:
         """
        user_id = kwargs.get('user_id', 0)
        flag, result = account_base_service_ins.delete_role_user(user_id)

        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, '', {})


class LoonUserResetPasswordView(LoonBaseView):

    @manage_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        重置密码
        :param requesdt:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        flag, result = account_base_service_ins.reset_password(user_id=user_id)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, result, {})


class LoonUserChangePasswordView(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        修改密码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.user.username

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        new_password = request_data_dict.get('new_password', '')
        source_password = request_data_dict.get('source_password', '')
        new_password_again = request_data_dict.get('new_password_again', '')

        if new_password != new_password_again:
            return api_response(-1, '两次密码不一致，请重新输入', {})
        flag, result = account_base_service_ins.change_password(username, source_password, new_password)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, result, {})


class LoonSimpleUserView(LoonBaseView):

    def get(self, request, *args, **kwargs):
        """
        获取用户简要信息列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        flag, result = account_base_service_ins.get_user_list(search_value, page, per_page, simple=True)
        if flag is not False:
            data = dict(value=result.get('user_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
            code, msg, = 0, ''
        else:
            code, data, msg = -1, '', result
        return api_response(code, msg, data)
