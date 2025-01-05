import json
import logging
import traceback
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from loonflow.wsgi import application
from service.account.account_application_service import account_application_service_ins
from service.account.account_base_service import account_base_service_ins
from service.account.account_dept_service import account_dept_service_ins
from service.account.account_role_service import account_role_service_ins
from service.account.account_tenant_service import account_tenant_service_ins
from service.account.account_user_service import account_user_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from apps.loon_base_view import BaseView
from schema import Schema, Regex, And, Or, Use, Optional

from service.permission.user_permission import user_permission_check
from service.common.schema_valid_service import SchemaValidService

logger = logging.getLogger("django")


class UserView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        Optional('alias'): str,
        'email': And(str, lambda n: n != '', error='alias is needed'),
        Optional('password'): str,
        Optional('phone'): str,
        Optional('dept_id_list'): list,
        Optional('role_id_list'): list,
        'type': And(str, lambda n: n in ["admin", "workflow_admin", "common"], error="type should be admin, workflow_admin, common"),
        'status': And(str, lambda n: n in ["in_post", "resigned"], error="type should be in_post, resigned"),
        Optional('avatar'): str,
        Optional('lang'): str,
    })

    delete_schema = Schema({
        "user_id_list": And(list, lambda n: len(n)>0, error="user_id_list can not be blank"),
    })

    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        get user list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page')) if request_data.get('per_page') else 10
        page = int(request_data.get('page')) if request_data.get('page') else 1
        dept_id = int(request_data.get('dept_id')) if request_data.get('department_id') else 0
        try:
            result = account_user_service_ins.get_user_list(search_value, dept_id, page, per_page)
            data = dict(user_list=result.get('user_result_object_format_list'),
                        per_page=result.get('paginator_info').get('per_page'),
                        page=result.get('paginator_info').get('page'),
                        total=result.get('paginator_info').get('total'))
            return api_response(0, "", data)
        except CustomCommonException as e:
            return api_response(-1, {}, str(e))
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, {}, "Internal Server Error")

    @user_permission_check('admin')
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
        name = request_data_dict.get('name')
        alias = request_data_dict.get('alias')
        email = request_data_dict.get('email')
        password = request_data_dict.get('password')
        phone = request_data_dict.get('phone')
        dept_id_list = request_data_dict.get('dept_id_list')
        role_id_list = request_data_dict.get('role_id_list')
        type = request_data_dict.get('type')
        status = request_data_dict.get('status')
        avatar = request_data_dict.get('avatar')
        lang = request_data_dict.get('lang')
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            user_id = account_base_service_ins.add_user(name, alias, email, phone, dept_id_list, role_id_list, type, status, avatar, lang, creator_id, password, tenant_id)
        except CustomCommonException as e:
            return api_response(-1, {}, str(e))
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, {}, "Internal Server Error")
        return api_response(0, "", dict(user_id=user_id))

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        delete uer in batches
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        user_id_list = request_data_dict.get('user_id_list', [])
        operator_id = request.META.get('HTTP_USERID')
        flag, result = account_base_service_ins.delete_user_list(user_id_list, operator_id)
        if flag is False:
            return api_response(-1, result, {})
        return api_response(0, "", dict(user_info=result))


class UserProfileView(BaseView):
    patch_schema = Schema({
        'lang': str,
    })

    def get(self, request, *args, **kwargs):
        """
        user profile
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = request.META.get('HTTP_USERID')
        if not user_id:
            return api_response(-1, "no user login", {})
        try:
            user_info = account_user_service_ins.get_user_format_by_user_id(user_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "",  {"user_info": user_info})

    def patch(self, request, *args, **kwargs):
        """
        update profile
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = request.META.get('HTTP_USERID')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        lang = request_data_dict.get("lang")
        try:
            account_user_service_ins.update_user_profile(user_id, lang)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "", {})


class UserDetailView(BaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        Optional('alias'): str,
        'email': And(str, lambda n: n != '', error='alias is needed'),
        Optional('password'): str,
        Optional('phone'): str,
        Optional('dept_id_list'): list,
        Optional('role_id_list'): list,
        'type': And(str, lambda n: n in ["admin", "workflow_admin", "common"],
                    error="type should be admin, workflow_admin, common"),
        'status': And(str, lambda n: n in ["in_post", "resigned"], error="type should be in_post, resigned"),
        Optional('avatar'): str,
        Optional('lang'): str,
    })

    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        get user detail
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            result = account_user_service_ins.get_user_format_by_user_id(kwargs.get('user_id'))
        except CustomCommonException as e:
            return api_response(-1, {}, str(e))
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, {}, "Internal Server Error")
        return api_response(0, "", dict(user_info=result))

    @user_permission_check('admin')
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
        name = request_data_dict.get('name')
        alias = request_data_dict.get('alias')
        email = request_data_dict.get('email')
        phone = request_data_dict.get('phone')
        dept_id_list = request_data_dict.get('dept_id_list')
        role_id_list = request_data_dict.get('role_id_list')
        type = request_data_dict.get('type')
        status = request_data_dict.get('status')
        avatar = request_data_dict.get('avatar')
        lang = request_data_dict.get('lang')
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')

        flag, result = account_base_service_ins.edit_user(user_id, name, alias, email, phone, dept_id_list, role_id_list, type, status, avatar, lang, creator_id, tenant_id)
        if flag is not False:
            code, msg, data = 0, '', {}
        else:
            code, msg, data = -1, result, {}
        return api_response(code, msg, data)

    @user_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete user record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        operator_id = request.META.get('HTTP_USERID')
        flag, result = account_base_service_ins.delete_user(user_id, operator_id)
        if flag:
            code, msg, data = 0, '', {}
            return api_response(code, msg, data)
        code, msg, data = -1, result, {}
        return api_response(code, msg, data)


class RoleView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != ''),
        Optional('description'): str,
        Optional('label'): str,
    })

    delete_schema = Schema({
        "role_id_list": list
    })
    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        get role list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        try:
            result = account_role_service_ins.get_role_list(search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        data = dict(role_list=result.get('role_result_object_format_list'),
                    per_page=result.get('paginator_info').get('per_page'),
                    page=result.get('paginator_info').get('page'),
                    total=result.get('paginator_info').get('total'))

        return api_response(0, "", data)

    @user_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        add role
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
        tenant_id = request.META.get('HTTP_TENANTID')
        creator_id = request.META.get('HTTP_USERID')
        try:
            role_id = account_role_service_ins.add_role(name=name, description=description, label=label, tenant_id=tenant_id,
                                                         creator_id=creator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, "", {"role_id": role_id})

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        batch delete role record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        role_id_list = request_data_dict.get('role_id_list')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_role_service_ins.batch_delete_role(role_id_list, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "deleted", {})


class RoleDetailView(BaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is need'),
        Optional('description'): str,
        Optional('label'): str,
    })

    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get role detail
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id')
        try:
            result = account_role_service_ins.get_role_detail(role_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "", dict(role_info=result))

    @user_permission_check('admin')
    def patch(self, request, *args, **kwargs):
        """
        update role record
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
        try:
            account_role_service_ins.update_role(role_id, name, description, label)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())

        return api_response(0, '', {})

    @user_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete role
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_role_service_ins.delete_role(role_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, 'delete successfully', {})

class SimpleRoleView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get simple role list, for common user query role list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        try:
            result = account_role_service_ins.get_role_list(search_value, page, per_page, True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        data = dict(role_list=result.get('role_result_object_format_list'),
                    per_page=result.get('paginator_info').get('per_page'),
                    page=result.get('paginator_info').get('page'),
                    total=result.get('paginator_info').get('total'))

        return api_response(0, "", data)


class DeptTreeView(BaseView):
    get_schema = Schema({
        "search_value": Use(SchemaValidService.parse_str_list, error="Search_value must be None or a string"),
        "parent_dept_id": Use(SchemaValidService.parse_integer_list, error="parent_department_id must be None or a int")
    })

    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get department tree
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        tenant_id = request.META.get('HTTP_TENANTID')
        parent_dept_id = int(request_data.get('parent_dept_id')) if request_data.get('parent_dept_id') else 0
        try:
            result = account_dept_service_ins.get_dept_tree(tenant_id, search_value, parent_dept_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, '', dict(dept_list=result))

class SimpleDeptTreeView(BaseView):
    get_schema = Schema({
        "search_value": Use(SchemaValidService.parse_str_list, error="Search_value must be None or a string"),
        "parent_dept_id": Use(SchemaValidService.parse_integer_list, error="parent_dept_id must be None or a int")
    })

    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get simple department tree, without leader info and approver info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        tenant_id = request.META.get('HTTP_TENANTID')
        parent_dept_id = int(request_data.get('parent_deptt_id')) if request_data.get('parent_dept_id') else 0
        try:
            result = account_dept_service_ins.get_dept_tree(tenant_id, search_value, parent_dept_id, True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server error", {})
        return api_response(0, '', dict(dept_list=result))

class DeptView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != ''),
        Optional('parent_dept_id'): int,
        Optional('leader_id'): int,
        Optional('approver_id_list'): list,
        Optional('label'): str,
    })

    @user_permission_check("admin")
    def post(self, request, *args, **kwargs):
        """
        create department record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        parent_dept_id = request_data_dict.get('parent_dept_id')
        leader_id = request_data_dict.get('leader_id')
        approver_id_list = request_data_dict.get('approver_id_list')
        label = request_data_dict.get('label')
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            dept_id = account_dept_service_ins.add_dept(name, parent_dept_id, leader_id, approver_id_list, label, creator_id, tenant_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, "", dict(dept_id=dept_id))

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        batch delete dept record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        dept_id_list = request_data_dict.get('dept_id_list')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_dept_service_ins.batch_delete_dept(dept_id_list, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "", {})


class DeptDetailView(BaseView):
    patch_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is need'),
        Optional('parent_dept_id'): int,
        Optional('leader_id'): int,
        Optional('approver_id_list'): list,
        Optional('label'): str,
    })

    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        dept detail
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_id = kwargs.get('dept_id')
        try:
            result = account_dept_service_ins.get_dept_detail_by_id(dept_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, "", result)


    @user_permission_check('admin')
    def delete(self, request, *args, **kwargs):
        """
        delete dept record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_id = kwargs.get('dept_id')
        operator_id = request.META.get('HTTP_USERID')
        try:
            account_dept_service_ins.delete_dept(dept_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, '', {})

    @user_permission_check('admin')
    def patch(self, request, *args, **kwargs):
        """
        update dept
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dept_id = kwargs.get('dept_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        parent_dept_id = int(request_data_dict.get('parent_dept_id')) if request_data_dict.get('parent_dept_id') else 0
        leader = request_data_dict.get('leader')
        approver_id_list = request_data_dict.get('approver_id_list')
        leader_id = request_data_dict.get('leader_id')
        label = request_data_dict.get('label')

        try:
            account_dept_service_ins.update_dept(dept_id, name, parent_dept_id, leader_id, approver_id_list, label)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, '', {})


class SimpleDeptView(BaseView):
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
class AppTokenView(BaseView):
    post_schema = Schema({
        'app_name': And(str, lambda n: n != '', error='app_name is needed'),
        Optional('ticket_sn_prefix'): str,
        Optional('workflow_ids'): str,
    })

    @user_permission_check('admin')
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

    @user_permission_check('admin')
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
class SimpleAppTokenView(BaseView):
    @user_permission_check('workflow_admin')
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


class JwtLoginView(BaseView):
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'invalid params', {})
        request_data_dict = json.loads(json_str)
        email = request_data_dict.get('email', '')
        password = request_data_dict.get('password', '')
        try:
            user = authenticate(email=email, password=password)
        except Exception as e:
            return api_response(-1, e.__str__(), {})
        if user is not None:
            flag, jwt_info = account_user_service_ins.get_user_jwt(email)
            if flag is False:
                return api_response(-1, '', {})
            else:
                return api_response(0, '', {'jwt': jwt_info})
        else:
            return api_response(-1, 'username or password is invalid', {})


class UserRoleView(BaseView):
    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        user's role info
        """
        user_id = kwargs.get('user_id', 0)
        search_value = request.GET.get('search_value', '')
        try:
            result = account_user_service_ins.get_user_role_info_by_user_id(user_id, search_value)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)


class RoleUserView(BaseView):
    post_schema = Schema({
        'user_id': And(int, error='user_id is needed and should be int')
    })
    delete_schema = Schema({
        'role_user_id_list': list
    })

    @user_permission_check('admin')
    def get(self, request, *args, **kwargs):
        """
        role's user list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id', 0)
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        search_value = request.GET.get('search_value', '')
        try:
            result = account_role_service_ins.get_role_user_info_by_role_id(role_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)

    @user_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        add role's user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        role_id = kwargs.get('role_id', 0)
        creator = request.user.username
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        user_id_list = request_data_dict.get('user_id_list', 0)

        try:
            account_base_service_ins.add_role_user(role_id, user_id_list, creator)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "success", {})

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        delete role's user list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        role_user_id_list = request_data_dict.get("role_user_id_list")
        try:
            account_role_service_ins.delete_role_user(role_user_id_list, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "success", {})


class UserResetPasswordView(BaseView):
    @user_permission_check('admin')
    def post(self, request, *args, **kwargs):
        """
        reset user's password
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_id = kwargs.get('user_id')
        try:
            account_user_service_ins.reset_password(user_id=user_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "password has been updated to 123456", {})


class UserChangePasswordView(BaseView):
    def post(self, request, *args, **kwargs):
        """
         change password
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        new_password = request_data_dict.get('new_password', '')
        source_password = request_data_dict.get('source_password', '')
        new_password_again = request_data_dict.get('new_password_again', '')

        if new_password != new_password_again:
            return api_response(-1, "passwords are different between two input", {})
        try:
            account_user_service_ins.change_password(operator_id, source_password, new_password)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "success", {})

class SimpleUserView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get simple user list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        dept_id = int(request_data.get('dept_id', 0)) if request_data.get('dept_id', 0) else 0
        try:
            result = account_user_service_ins.get_user_list(search_value, dept_id, page, per_page, simple=True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        data = dict(user_list=result.get('user_result_object_format_list'),
                    per_page=result.get('paginator_info').get('per_page'),
                    page=result.get('paginator_info').get('page'),
                    total=result.get('paginator_info').get('total'))
        return api_response(0, "", data)


class ApplicationView(BaseView):
    post_schema = Schema({
        "name": And(str, lambda n: n != "", error="name is need"),
        "type": And(str, lambda n: n != "", error="type is need"),
        Optional('description'): str,
    })
    delete_schema = Schema({
        "application_id_list": list
    })

    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get application list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = request.META.get('HTTP_TENANTID')
        search_value = request.GET.get('search_value', '')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        try:
            result = account_application_service_ins.get_application_list(tenant_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)

    @user_permission_check("admin")
    def post(self, request, *args, **kwargs):
        """
        add application record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name', '')
        type = request_data_dict.get('type', '')
        description = request_data_dict.get('description', '')
        try:
            result = account_application_service_ins.add_application(tenant_id, operator_id, name, description, type)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(application_id=result))

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        batch delete application record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        application_id_list = request_data_dict.get('application_id_list', [])
        try:
            account_application_service_ins.batch_delete_application_list(tenant_id, operator_id, application_id_list)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
        return api_response(0, "deleted", {})


class SimpleApplicationView(BaseView):
    @user_permission_check("workflow_admin")
    def get(self, request, *args, **kwargs):
        """
        get simple application list. used by select application in workflow config page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = request.META.get('HTTP_TENANTID')
        search_value = request.GET.get('search_value', '')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        try:
            result = account_application_service_ins.get_application_list(tenant_id, search_value, page, per_page, True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)


class ApplicationDetailView(BaseView):
    patch_schema = Schema({
        "name": str,
        Optional("description"): str,
        "type": And(str, lambda n: n in ["admin", "workflow_admin"], error="type should be admin or workflow_admin")
    })
    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get application detail
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = kwargs.get("application_id")
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_application_service_ins.get_application_detail(tenant_id, application_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(application_info=result))

    @user_permission_check("admin")
    def patch(self, request, *args, **kwargs):
        """
        update application info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        application_id = kwargs.get("application_id")
        tenant_id = request.META.get('HTTP_TENANTID')

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name', '')
        description = request_data_dict.get('description', '')
        type = request_data_dict.get('type', '')
        try:
            account_application_service_ins.update_application_detail(tenant_id, application_id, name, description, type)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "internal Server Error")
        return api_response(0, "", {})

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        delete app
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        application_id = kwargs.get("application_id")
        try:
            account_application_service_ins.batch_delete_application_list(tenant_id, operator_id, [application_id])
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "internal Server Error")
        return api_response(0, "", {})


class ApplicationWorkflowView(BaseView):
    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get application's authorized workflow list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = kwargs.get("application_id")
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        try:
            result = account_application_service_ins.get_application_workflow_list(application_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)


class TenantDetailView(BaseView):
    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get tenant detail info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = kwargs.get("tenant_id")
        try:
            result = account_tenant_service_ins.get_tenant_detail(tenant_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Erro")
        return api_response(0, "", dict(tenant_info=result))

