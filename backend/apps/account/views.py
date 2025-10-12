import json
import logging
import traceback
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from schema import Schema, And, Optional
from apps.loon_base_view import BaseView
from service.format_response import api_response
from service.permission.user_permission import user_permission_check
from service.account.account_base_service import account_base_service_ins
from service.account.account_dept_service import account_dept_service_ins
from service.account.account_role_service import account_role_service_ins
from service.account.account_user_service import account_user_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.account.account_tenant_service import account_tenant_service_ins
from service.account.account_application_service import account_application_service_ins


logger = logging.getLogger("django")


class UserView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != '', error='name is needed'),
        Optional('alias'): str,
        'email': And(str, lambda n: n != '', error='alias is needed'),
        Optional('password'): str,
        Optional('password1'): str,
        Optional('phone'): str,
        Optional('dept_id_list'): list,
        Optional('role_id_list'): list,
        'type': And(str, lambda n: n in ["admin", "workflow_admin", "normal"], error="type should be admin, workflow_admin, normal"),
        'is_active': bool,
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
        dept_id = request_data.get('dept_id') if request_data.get('dept_id') else '00000000-0000-0000-0000-000000000000'
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_user_service_ins.get_user_list(tenant_id, search_value, '', dept_id, page, per_page)
            data = dict(user_info_list=result.get('user_result_object_format_list'),
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
        password1 = request_data_dict.get('password1')
        phone = request_data_dict.get('phone')
        dept_id_list = request_data_dict.get('dept_id_list')
        type = request_data_dict.get('type')
        is_active = request_data_dict.get('is_active')
        avatar = request_data_dict.get('avatar','')
        lang = request_data_dict.get('lang', 'zh-CN')
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        if password!= password1:
            return api_response(-1, 'password is not same', {})
        try:
            user_id = account_user_service_ins.add_user(name, alias, email, phone, dept_id_list, [], type, is_active, avatar, lang, creator_id, password, tenant_id)
        except CustomCommonException as e:
            return api_response(-1,  str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
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
        try:
            account_user_service_ins.delete_user_list(user_id_list, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "", {})

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
        tenant_id = request.META.get('HTTP_TENANTID')
        if not user_id:
            return api_response(-1, "no user login", {})
        try:
            user_info = account_user_service_ins.get_user_format_by_user_id(tenant_id, user_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            return api_response(-1, "Internal Server Error", {})
        my_profile = {
            "name": user_info.get('name'),
            "alias": user_info.get('alias'),
            "email": user_info.get('email'),
            "phone": user_info.get('phone'),
            "avatar": user_info.get('avatar'),
            "lang": user_info.get('lang'),
            "dept_info_list": user_info.get('dept_info_list'),
        }
        return api_response(0, "",  {"my_profile": my_profile})

    def patch(self, request, *args, **kwargs):
        """
        update profile, only support change lang for now
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
        'type': And(str, lambda n: n in ["admin", "workflow_admin", "normal"],
                    error="type should be admin, workflow_admin, normal"),
        'is_active': bool,
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
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_user_service_ins.get_user_format_by_user_id(tenant_id, kwargs.get('user_id'))
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
        alias = request_data_dict.get('alias', '')
        email = request_data_dict.get('email')
        phone = request_data_dict.get('phone', '')
        dept_id_list = request_data_dict.get('dept_id_list', [])
        role_id_list = request_data_dict.get('role_id_list', [])
        type = request_data_dict.get('type')
        is_active = request_data_dict.get('is_active', False)
        avatar = request_data_dict.get('avatar', '')
        lang = request_data_dict.get('lang', 'zh-CN')
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')

        flag, result = account_user_service_ins.edit_user(user_id, name, alias, email, phone, dept_id_list, role_id_list, type, is_active, avatar, lang, creator_id, tenant_id)
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
        try:
            account_user_service_ins.delete_user(user_id, operator_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "", {})

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
        role_ids = request_data.get('role_ids', '')
        try:
            result = account_role_service_ins.get_role_list(search_value, role_ids, page, per_page)
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
        label = request_data_dict.get('label', {})
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            account_role_service_ins.update_role(tenant_id, role_id, name, description, label)
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

class SimpleRolesView(BaseView):
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
        role_ids = request_data.get('role_ids', '')
        try:
            result = account_role_service_ins.get_role_list(search_value, role_ids, page, per_page, True)
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
        tenant_id = request.META.get('HTTP_TENANTID')
        is_simple = True if request_data.get('is_simple') == 'true' else False
        try:
            result = account_dept_service_ins.get_dept_tree(tenant_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        
        return api_response(0, '', dict(dept_list=result))

class DeptPathView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get department link list, eg."technical department-infrastructure"
        """
        request_data = request.GET
        dept_id = kwargs.get('dept_id', 0)
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_dept_service_ins.get_dept_path(tenant_id, dept_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc()) 
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, '', dict(dept_path=result))

class DeptPathsView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get department link list, eg."technical department-infrastructure"
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        tenant_id = request.META.get('HTTP_TENANTID')
        dept_ids = request_data.get('dept_ids', '')
        try:
            result = account_dept_service_ins.get_dept_path_list(tenant_id, dept_ids, search_value)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc()) 
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, '', dict(dept_path_list=result))

class DeptView(BaseView):
    post_schema = Schema({
        'name': And(str, lambda n: n != ''),
        Optional('parent_dept_id'): str,
        Optional('leader_id'): str,
        Optional('approver_id_list'): [str],
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
        label = request_data_dict.get('label', {})
        creator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            dept_id = account_dept_service_ins.add_dept(name, parent_dept_id, leader_id, approver_id_list, creator_id, tenant_id, label)
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
        Optional('parent_dept_id'): str,
        Optional('leader_id'): str,
        Optional('approver_id_list'): list,
        Optional('label'): dict,
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
        
        return api_response(0, "", dict(dept_info=result))


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
        tenant_id = request.META.get('HTTP_TENANTID')
        dept_id = kwargs.get('dept_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name')
        parent_dept_id = request_data_dict.get('parent_dept_id') if request_data_dict.get('parent_dept_id') else ''
        leader = request_data_dict.get('leader')
        approver_id_list = request_data_dict.get('approver_id_list')
        leader_id = request_data_dict.get('leader_id')
        label = request_data_dict.get('label', {})

        try:
            account_dept_service_ins.update_dept(tenant_id, dept_id, name, parent_dept_id, leader_id, approver_id_list, label)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, '', {})

class DeptParentDeptView(BaseView):
    patch_schema = Schema({
        'parent_dept_id': str,
    })
    def patch(self, request, *args, **kwargs):
        tenant_id = request.META.get('HTTP_TENANTID')
        dept_id = kwargs.get('dept_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        parent_dept_id = request_data_dict.get('parent_dept_id') if request_data_dict.get('parent_dept_id') else ''

        try:
            account_dept_service_ins.update_dept_parent_dept(tenant_id, dept_id, parent_dept_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        return api_response(0, '', {})

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
            if not user.is_active:
                return api_response(-1, 'user is not active', {})
            flag, jwt_info = account_user_service_ins.get_user_jwt(email)
            if flag is False:
                return api_response(-1, '', {})
            else:
                return api_response(0, '', {'jwt': jwt_info})
        else:
            return api_response(-1, 'username or password is incorrect', {})

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
        'user_ids': And(list, error='user_ids is required, and should be a list')
    })
    delete_schema = Schema({
        'user_ids': And(list, error='user_ids is required, and should be a list')
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
        role_id = kwargs.get('role_id', '')
        request_data = request.GET
        tenant_id = request.META.get('HTTP_TENANTID')

        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        search_value = request.GET.get('search_value', '')
        try:
            result = account_role_service_ins.get_role_user_info_list_by_role_id(tenant_id,role_id, search_value, page, per_page)
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
        role_id = kwargs.get('role_id', '')
        creator = request.user.username
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        user_id_list = request_data_dict.get('user_ids', [])
        tenant_id = request.META.get('HTTP_TENANTID')

        try:
            account_role_service_ins.add_role_user(tenant_id, role_id, user_id_list, creator)
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
        user_ids = request_data_dict.get("user_ids", [])
        role_id = kwargs.get('role_id', '')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            account_role_service_ins.delete_role_user(tenant_id, role_id, user_ids, operator_id)
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
        tenant_id = request.META.get('HTTP_TENANTID')

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        new_password = request_data_dict.get('new_password', '')
        source_password = request_data_dict.get('source_password', '')
        new_password_again = request_data_dict.get('new_password_again', '')

        if new_password != new_password_again:
            return api_response(-1, "passwords are different between two input", {})
        try:
            account_user_service_ins.change_password(tenant_id, operator_id, source_password, new_password)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})
        return api_response(0, "success", {})

class SimpleUsersView(BaseView):
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
        dept_id = request_data.get('dept_id', '')
        user_ids = request_data.get('user_ids', '')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_user_service_ins.get_user_list(tenant_id, search_value, user_ids, dept_id, page, per_page, simple=True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error", {})

        data = dict(user_info_list=result.get('user_result_object_format_list'),
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
        app_ids = request.GET.get('app_ids', '')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        type = request_data.get('type', 'all')
        try:
            result = account_application_service_ins.get_application_list(tenant_id, search_value, app_ids, page, per_page, type=type)
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
        app_ids = request.GET.get('app_ids', '')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        type = request_data.get('type', 'all')
        try:
            result = account_application_service_ins.get_application_list(tenant_id, search_value, app_ids, page, per_page, True, type)
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
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = account_application_service_ins.get_application_workflow_list(tenant_id, application_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)

    @user_permission_check("admin")
    def post(self, request, *args, **kwargs):
        """
        add application workflow permission
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = kwargs.get("application_id")
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        workflow_ids = request_data_dict.get('workflow_ids', [])
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        
        try:
            result = account_application_service_ins.add_application_workflow_permission(
                tenant_id, application_id, workflow_ids, operator_id
            )
            if result:
                return api_response(0, "添加工作流权限成功", {})
            else:
                return api_response(-1, "添加工作流权限失败", {})
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        delete application workflow permission
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = kwargs.get("application_id")
        request_data = request.GET
        workflow_id = request_data.get('workflow_id')
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        
        if not workflow_id:
            return api_response(-1, "workflow_id is required", {})
        
        try:
            result = account_application_service_ins.delete_application_workflow_permission(
                tenant_id, application_id, workflow_id, operator_id
            )
            if result:
                return api_response(0, "删除工作流权限成功", {})
            else:
                return api_response(-1, "删除工作流权限失败", {})
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")

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
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(tenant_info=result))

class TenantDomainView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get tenant detail info by domain, only return basic info, id, icon, name
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        domain = request.GET.get('domain')
        if not domain:
            return api_response(-1, "domain is required", {})
        try:
            result = account_tenant_service_ins.get_tenant_by_domain(domain)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(tenant_info=result))

class ApplicationWorkflowPermissionListView(BaseView):
    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get application workflow permission list
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
        tenant_id = request.META.get('HTTP_TENANTID')
        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        try:
            result = workflow_permission_service_ins.get_workflow_info_list_by_app_id(tenant_id, application_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        return api_response(0, "", result)