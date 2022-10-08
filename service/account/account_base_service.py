import datetime
import json
import time
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from apps.account.models import AppToken, LoonUser, LoonUserRole, LoonDept, LoonRole, LoonUserDept
from service.base_service import BaseService
from service.common.constant_service import constant_service_ins
from service.common.log_service import auto_log


class AccountBaseService(BaseService):
    """
    account
    """
    @classmethod
    @auto_log
    def get_token_by_app_name(cls, app_name: str)->tuple:
        """
        get app's call token by app_name
        :param app_name:
        :return:
        """
        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        return True, app_token_obj

    @classmethod
    @auto_log
    def get_user_by_username(cls, username: str)->tuple:
        """
        get user info by username
        :return:
        """
        result = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if result:
            return True, result
        else:
            return False, 'username: {} is not existed or has been deleted'.format(username)

    @classmethod
    @auto_log
    def get_user_list_by_usernames(cls, usernames: list)->tuple:
        """
        get user info by username
        :return:
        """
        result = LoonUser.objects.filter(username__in=usernames, is_deleted=0).all()
        if result:
            return True, result
        else:
            return False, 'usernames: {} is not existed or has been deleted'.format(usernames)

    @classmethod
    @auto_log
    def get_user_by_user_id(cls, user_id: int)->tuple:
        """
        get user by user id
        :param user_id:
        :return:
        """
        result = LoonUser.objects.filter(id=user_id, is_deleted=0).first()
        if result:
            return True, result
        else:
            return False, 'user_id: {} is not existed or has been deleted'.format(user_id)

    @classmethod
    @auto_log
    def get_user_name_list_by_id_list(cls, user_id_list: list)->tuple:
        """
        get username list by user id list
        根据用户id的数组获取用户名的list
        :param user_id_list:
        :return:
        """
        user_queryset = LoonUser.objects.filter(id__in=user_id_list, is_deleted=0).all()
        if not user_queryset:
            return False, 'user id is not existed or has been deleted'
        username_list = [user_query.username for user_query in user_queryset]
        return True, dict(username_list=username_list)

    @classmethod
    @auto_log
    def get_user_role_id_list(cls, username: str)->tuple:
        """
        get user's role id list by username
        :param username:
        :return:
        """
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, 'user is not existed or has been deleted'
        user_role_queryset = LoonUserRole.objects.filter(user_id=user_obj.id, is_deleted=0).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        return True, user_role_id_list

    @classmethod
    @auto_log
    def get_user_role_info_by_user_id(cls, user_id: int, search_value: str=0, page: int =1, per_page: int=10)->tuple:
        """
        get user's role info list by user's id and query params: role name、page、per_page
        :param user_id:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        user_role_queryset = LoonUserRole.objects.filter(user_id=user_id, is_deleted=0).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        query_params = Q(is_deleted=False, id__in=user_role_id_list)
        if search_value:
            query_params &= Q(name__contains=search_value)
        role_info_queryset = LoonRole.objects.filter(query_params).all()
        paginator = Paginator(role_info_queryset, per_page)
        try:
            role_info_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            role_info_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            role_info_result_paginator = paginator.page(paginator.num_pages)
        role_result_list = role_info_result_paginator.object_list
        role_result_format_list = []
        for role_info in role_result_list:
            role_result_format_list.append(dict(id=role_info.id, name=role_info.name, description=role_info.description,
                                                label=json.dumps(role_info.label) if role_info.label else {},
                                                creator=role_info.creator, gmt_created=str(role_info.gmt_created)[:19]))
        return True, dict(role_result_format_list=role_result_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def get_role_user_info_by_role_id(cls, role_id: int, search_value: str='', page: int=1, per_page: int =10)->tuple:
        """
        get role's user info list by role_id
        :param role_id:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        user_role_queryset = LoonUserRole.objects.filter(role_id=role_id, is_deleted=0).all()
        role_user_id_list = [user_role.user_id for user_role in user_role_queryset]
        query_params = Q(is_deleted=False, id__in=role_user_id_list)
        if search_value:
            query_params &= Q(username__contains=search_value) | Q(alias__contains=search_value)
        user_info_queryset = LoonUser.objects.filter(query_params).all()
        paginator = Paginator(user_info_queryset, per_page)
        try:
            user_info_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            user_info_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            user_info_result_paginator = paginator.page(paginator.num_pages)
        user_result_list = user_info_result_paginator.object_list
        user_result_format_list = []
        for user_info in user_result_list:
            user_result_format_list.append(user_info.get_dict())
        return True, dict(user_result_format_list=user_result_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def get_user_up_dept_id_list(cls, username: str)->tuple:
        """
        get user's department id list by username, include parent department
        :param username:
        :return:
        """
        dept_id_list = []
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, 'user is not existed or has been deleted'

        def iter_dept(dept_id):
            dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                dept_id_list.append(dept_obj.id)
                if dept_obj.parent_dept_id:
                    iter_dept(dept_obj.parent_dept_id)
        user_dept_queryset = LoonUserDept.objects.filter(user_id=user_obj.id, is_deleted=0).all()
        user_dept_id_list = [user_dept.dept_id for user_dept in user_dept_queryset]
        for user_dept_id in user_dept_id_list:
            iter_dept(user_dept_id)
        dept_id_list = list(set(dept_id_list))
        return True, dept_id_list

    @classmethod
    @auto_log
    def get_user_dept_approver(cls, username: str, dept_id: int=0)->tuple:
        """
        get user's department approver， Preferential access to the approver, without taking tl（team leader）
        :param username:
        :param dept_id: 用于用户可能属于多个部门的情况
        :return:
        """
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if dept_id:
            if LoonUserDept.objects.filter(user_id=user_obj.id, dept_id=dept_id, is_deleted=0).first():
                loon_dept_obj = LoonDept.objects.filter(id=dept_id).first()
                if loon_dept_obj.approver:
                    return True, loon_dept_obj.approver
                else:
                    return True, loon_dept_obj.leader
            else:
                return False, 'dept_id is invalid'
        else:
            # no dept id specified, get all user dept's approver
            user_dept_queryset = LoonUserDept.objects.filter(user_id=user_obj.id, is_deleted=0)
            approver_list = []
            for user_dept in user_dept_queryset:
                if user_dept.dept.approver:
                    approver_list.extend(user_dept.dept.approver.split(','))
                else:
                    approver_list.append(user_dept.dept.leader)
            return True, ','.join(list(set(approver_list)))

    @classmethod
    @auto_log
    def get_user_dept_info(cls, username: str='', user_id: int=0)->tuple:
        """
        get user dept info
        :param username:
        :param user_id:
        :return:
        """
        if username:
            user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
            user_id = user_obj.id
        user_dept_queryset = LoonUserDept.objects.filter(user_id=user_id, is_deleted=0).all()
        user_dept_info = {}
        user_dept_id_list = []
        user_dept_name_list = []
        for user_dept in user_dept_queryset:
            user_dept_id_list.append(str(user_dept.dept_id))
            user_dept_name_list.append(user_dept.dept.name)
        user_dept_info['id'] = ','.join(user_dept_id_list)
        user_dept_info['name'] = ','.join(user_dept_name_list)
        return True, user_dept_info

    @classmethod
    @auto_log
    def get_dept_sub_dept_id_list(cls, dept_id: int)->tuple:
        """
        get department's all subordinate department
        :param dept_id:
        :return:
        """
        dept_id_list = []
        dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
        if dept_obj:
            dept_id_list.append(dept_obj.id)
        else:
            return True, []

        def iter_dept_id_list(new_dept_id):
            new_dept_obj = LoonDept.objects.filter(id=new_dept_id, is_deleted=0).first()
            if new_dept_obj:
                sub_dept_queryset = LoonDept.objects.filter(parent_dept_id=new_dept_obj.id, is_deleted=0).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return True, dept_id_list

    @classmethod
    @auto_log
    def get_dept_username_list(cls, dept_id: object)->tuple:
        """
        get department's all username list
        :param dept_id: int or str
        :return:
        """
        if type(dept_id) == str:
            dept_id_str_list = dept_id.split(',')  # 用于支持多部门
            dept_id_list = [int(dept_id_str) for dept_id_str in dept_id_str_list]
        else:
            dept_id_list = [dept_id]

        sub_dept_id_list_total = []

        for dept_id in dept_id_list:
            flag, sub_dept_id_list = cls.get_dept_sub_dept_id_list(dept_id)
            if flag is False:
                return False, sub_dept_id_list
            sub_dept_id_list_total = sub_dept_id_list_total + sub_dept_id_list

        user_dept_queryset = LoonUserDept.objects.filter(dept_id__in=sub_dept_id_list_total).all()
        user_id_list = [user_dept.user_id for user_dept in user_dept_queryset]

        user_queryset = LoonUser.objects.filter(id__in=user_id_list).all()
        user_name_list = [user.username for user in user_queryset]

        return True, user_name_list

    @classmethod
    @auto_log
    def get_role_username_list(cls, role_id: int)->tuple:
        """
        get role's username list by role_id
        :param role_id:
        :return:
        """
        user_role_queryset = LoonUserRole.objects.filter(role_id=role_id, is_deleted=0).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return True, []
        username_queryset = LoonUser.objects.filter(id__in=user_id_list).all()
        username_list = []
        for username_obj in username_queryset:
            username_list.append(username_obj.username)
        return True, username_list

    @classmethod
    @auto_log
    def get_dept_by_id(cls, dept_id: int)->tuple:
        """
        get department's info by dept_id
        :param dept_id:
        :return:
        """
        return True, LoonDept.objects.filter(id=dept_id, is_deleted=False).first()

    @classmethod
    @auto_log
    def get_dept_by_ids(cls, dept_ids: str)->tuple:
        """
        get department's queryset by dept_ids
        :param dept_ids:
        :return:
        """
        if dept_ids:
            dept_id_list = dept_ids.split(',')
        return True, LoonDept.objects.filter(id__in=dept_id_list, is_deleted=False).all()

    @classmethod
    @auto_log
    def get_role_by_id(cls, role_id: int)->tuple:
        """
        get role's info by role_id
        :param role_id:
        :return:
        """
        return True, LoonRole.objects.filter(id=role_id, is_deleted=False).first()

    @classmethod
    @auto_log
    def app_workflow_permission_list(cls, app_name: str)->tuple:
        """
        get app's authorised workflow_id list by app_name
        :param app_name:
        :return:
        """
        if not app_name:
            return False, 'app_name is not provided'
        if app_name == 'loonflow':
            # loonflow有权限访问所有workflow
            from apps.workflow.models import Workflow
            workflow_query_set = Workflow.objects.filter(is_deleted=0).all()
            workflow_id_list = []
            for workflow_obj in workflow_query_set:
                workflow_id_list.append(workflow_obj.id)
            return True, dict(workflow_id_list=workflow_id_list)

        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        if not app_token_obj:
            return False, 'appname is unauthorized'


    @classmethod
    @auto_log
    def app_workflow_permission_check(cls, app_name: str, workflow_id: int)->tuple:
        """
        appname has permission for workflow check by app_name and workflow_id
        :param app_name:
        :param workflow_id:
        :return:
        """
        if app_name == 'loonflow':
            return True, ''

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        flag, result = workflow_permission_service_ins.get_workflow_id_list_by_permission('api', 'app', app_name)

        if flag and result.get('workflow_id_list') and workflow_id in result.get('workflow_id_list'):
            return True, ''
        else:
            return False, 'the app has no permission to the workflow_id'

    @classmethod
    @auto_log
    def app_ticket_permission_check(cls, app_name: str, ticket_id: int)-> tuple:
        """
        appname has permission to ticket check by app_name and ticket_id
        :param app_name:
        :param ticket_id:
        :return:
        """
        from service.ticket.ticket_base_service import ticket_base_service_ins
        flag, ticket_obj = ticket_base_service_ins.get_ticket_by_id(ticket_id)
        if not flag:
            return False, ticket_obj
        workflow_id = ticket_obj.workflow_id

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        permission_check, msg = workflow_permission_service_ins.workflow_id_permission_check(workflow_id, 'api', 'app', app_name)

        if not permission_check:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def get_user_list(cls, search_value: str, page: int=1, per_page: int=10, simple=False)->tuple:
        """
        get user restful info list by query params: search_value, page, per_page
        :param search_value: support user's username, and user's alias. fuzzy query
        :param page:
        :param per_page:
        :param simple: 是否只返回简单信息
        :return:
        """
        query_params = Q(is_deleted=False)
        if search_value:
            query_params &= Q(username__contains=search_value) | Q(alias__contains=search_value)
        user_objects = LoonUser.objects.filter(query_params)
        paginator = Paginator(user_objects, per_page)
        try:
            user_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            user_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            user_result_paginator = paginator.page(paginator.num_pages)
        user_result_object_list = user_result_paginator.object_list
        user_result_object_format_list = []
        user_id_list = [user_result_object.id for user_result_object in user_result_object_list]
        # 获取用户所在部门信息
        user_dept_list = LoonUserDept.objects.filter(user_id__in=user_id_list, is_deleted=0)

        for user_result_object in user_result_object_list:
            user_result_format_dict = user_result_object.get_dict()
            # todo 获取部门信息
            user_dept_info_list = []
            for user_dept in user_dept_list:
                if user_result_object.id == user_dept.user_id:
                    user_dept_info_list.append(
                        dict(name=user_dept.dept.name, id=user_dept.dept.id))
            user_result_format_dict['user_dept_info_list'] = user_dept_info_list
            if simple:
                # 去除敏感信息
                user_result_format_dict.pop('last_login')
                user_result_format_dict.pop('email')
                user_result_format_dict.pop('creator_info')
                user_result_format_dict.pop('phone')
                user_result_format_dict.pop('type_id')
                user_result_format_dict.pop('gmt_created')
                user_result_format_dict.pop('gmt_modified')
                user_result_format_dict.pop('is_deleted')
            user_result_object_format_list.append(user_result_format_dict)

        return True, dict(user_result_object_format_list=user_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_user(cls, username: str, alias: str, email: str, phone: str, dept_ids: str, is_active: int,
                 type_id: int, creator: str, password: str='')->tuple:
        """
        新增用户， 因为非管理员或者工作流管理员无需登录管理后台，密码字段留空
        add user, not support set password, you need reset password
        :param username:
        :param alias:
        :param email:
        :param phone:
        :param dept_ids: 逗号隔开多个部门
        :param is_active:
        :param dept_ids:
        :param creator:
        :param password:
        :return:
        """
        password_str = make_password(password, None, 'pbkdf2_sha256')
        user_obj = LoonUser(username=username, alias=alias, email=email, phone=phone,
                            is_active=is_active, type_id=type_id,
                            creator=creator, password=password_str)
        user_obj.save()

        queryset_list = []
        for dept_id in dept_ids.split(','):
            queryset_list.append(LoonUserDept(user_id=user_obj.id, dept_id=dept_id))
        LoonUserDept.objects.bulk_create(queryset_list)

        return True, dict(user_id=user_obj.id)

    @classmethod
    @auto_log
    def edit_user(cls, user_id: int, username: str, alias: str, email: str, phone: str, dept_ids: str, is_active: int,
                  type_id: int)-> tuple:
        """
        edit user
        :param user_id:
        :param username:
        :param alias:
        :param email:
        :param phone:
        :param dept_ids:
        :param is_active:
        :param type_id:
        :return:
        """
        user_obj = LoonUser.objects.filter(id=user_id, is_deleted=0)
        user_obj.update(username=username, alias=alias, email=email, phone=phone, is_active=is_active,
                        type_id=type_id)
        # todo 更新部门信息
        dept_id_str_list = dept_ids.split(',')
        dept_id_int_list = [int(dept_id_str) for dept_id_str in dept_id_str_list]
        user_id = user_obj.first().id
        user_dept_queryset = LoonUserDept.objects.filter(user_id=user_id, is_deleted=0).all()
        user_dept_id_exist = [user_dept.dept_id for user_dept in user_dept_queryset]

        need_add_list = [dept_id_int for dept_id_int in dept_id_int_list if dept_id_int not in user_dept_id_exist]
        need_delete_list = [user_dept_id for user_dept_id in user_dept_id_exist if user_dept_id not in dept_id_int_list]
        add_queryset = []
        for need_add in need_add_list:
            add_queryset.append(LoonUserDept(user_id=user_id, dept_id=need_add))
        LoonUserDept.objects.bulk_create(add_queryset)
        LoonUserDept.objects.filter(user_id=user_id, dept_id__in=need_delete_list).update(is_deleted=1)

        return True, {}

    @classmethod
    @auto_log
    def delete_user(cls, user_id: int)->tuple:
        """
        delete user
        :param user_id:
        :return:
        """
        user_obj = LoonUser.objects.filter(id=user_id, is_deleted=0)
        user_obj.update(is_deleted=1)
        return True, {}

    @classmethod
    @auto_log
    def get_role_list(cls, search_value: str, page: int=1, per_page: int=10)->tuple:
        """
        获取角色列表
        get role restful list by search params
        :param search_value: role name or role description Support fuzzy queries
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False)
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
        user_objects = LoonRole.objects.filter(query_params)
        paginator = Paginator(user_objects, per_page)
        try:
            role_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            role_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            role_result_paginator = paginator.page(paginator.num_pages)
        role_result_object_list = role_result_paginator.object_list
        role_result_object_format_list = []
        for role_result_object in role_result_object_list:
            role_result_object_format_list.append(role_result_object.get_dict())

        return True, dict(role_result_object_format_list=role_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_role(cls, name: str, description: str, label: str, creator: str)->tuple:
        """
        add role
        新增角色
        :param name:
        :param description:
        :param label:
        :param creator:
        :return:
        """
        role_obj = LoonRole(name=name, description=description, label=label, creator=creator)
        role_obj.save()
        return True, dict(role_id=role_obj.id)

    @classmethod
    @auto_log
    def add_role_user(cls, role_id: int, user_id: int, creator: str)->tuple:
        """
        add role's user
        新增角色用户
        :param role_id:
        :param user_id:
        :param creator:
        :return:
        """
        # 去重下
        role_user_queryset = LoonUserRole.objects.filter(user_id=user_id, role_id=role_id, is_deleted=0)
        if role_user_queryset:
            return False, 'user has been existed in this role'
        role_user_obj = LoonUserRole(user_id=user_id, role_id=role_id, creator=creator)
        role_user_obj.save()
        return True, dict(role_user_id=role_user_obj.id)

    @classmethod
    @auto_log
    def delete_role_user(cls, user_id: int)->tuple:
        """
        删除角色用户
        :param user_id:
        :return:
        """
        role_user_obj = LoonUserRole.objects.filter(user_id=user_id, is_deleted=0)
        if not role_user_obj:
            return False, 'record is not existed or has been deleted'
        role_user_obj.update(is_deleted=1)
        return True, ''

    @classmethod
    @auto_log
    def update_role(cls, role_id: int, name: str, description: str, label: str)-> tuple:
        """
        update role
        更新角色
        :param role_id:
        :param name:
        :param description:
        :param label:
        :return:
        """
        role_queryset = LoonRole.objects.filter(id=role_id, is_deleted=0)
        if not role_queryset:
            return False, 'role record is not existed'
        role_queryset.update(name=name, description=description, label=label)
        return True, {}

    @classmethod
    @auto_log
    def delete_role(cls, role_id: int)->tuple:
        """
        delete role record
        删除角色
        :param role_id:
        :return:
        """
        role_queryset = LoonRole.objects.filter(id=role_id, is_deleted=0)
        if not role_queryset:
            return False, 'role record is not existed'
        role_queryset.update(is_deleted=1)
        return True, {}

    @classmethod
    @auto_log
    def get_dept_list(cls, search_value: str, page: int=1, per_page: int=10, simple=False)->tuple:
        """
        get dept restful list by search params
        :param search_value: department name or department description Support fuzzy queries
        :param page:
        :param per_page:
        :param simple: 只返回部分数据
        :return:
        """
        query_params = Q(is_deleted=False)
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(label__contains=search_value)
        dept_objects = LoonDept.objects.filter(query_params)
        paginator = Paginator(dept_objects, per_page)
        try:
            dept_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            dept_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            dept_result_paginator = paginator.page(paginator.num_pages)
        dept_result_object_list = dept_result_paginator.object_list
        dept_result_object_format_list = []
        for dept_result_object in dept_result_object_list:
            result_dict = dept_result_object.get_dict()
            if simple:
                simple_result_dict = dict()
                simple_result_dict['id'] = result_dict['id']
                simple_result_dict['name'] = result_dict['name']
                simple_result_dict['parent_dept_info'] = result_dict['parent_dept_info']
            dept_result_object_format_list.append(result_dict)
        return True, dict(dept_result_object_format_list=dept_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_dept(cls, name: str, parent_dept_id: int, leader: str, approver: str, label: str, creator: str)->tuple:
        """
        add department
        新增部门
        :param name:
        :param parent_dept_id:
        :param leader:
        :param approver:
        :param label:
        :param creator:
        :return:
        """
        dept_obj = LoonDept(name=name, parent_dept_id=parent_dept_id, leader=leader, approver=approver, label=label,
                            creator=creator)
        dept_obj.save()
        return True, dict(dept_id=dept_obj.id)

    @classmethod
    @auto_log
    def update_dept(cls, dept_id: int, name: str, parent_dept_id: int, leader: str, approver: str, label: str)->tuple:
        """
        update department record
        更新部门
        :param dept_id:
        :param name:
        :param parent_dept_id:
        :param leader:
        :param approver:
        :param label:
        :return:
        """
        dept_queryset = LoonDept.objects.filter(id=dept_id, is_deleted=0)
        if not dept_queryset:
            return False, 'dept is not existed or has been deleted'
        dept_queryset.update(name=name, parent_dept_id=parent_dept_id, leader=leader, approver=approver, label=label)
        return True, ''

    @classmethod
    @auto_log
    def delete_dept(cls, dept_id: int)-> tuple:
        """
        delete department record
        :param dept_id:
        :return:
        """
        dept_queryset = LoonDept.objects.filter(id=dept_id, is_deleted=0)
        if not dept_queryset:
            return False, 'dept is not existed or has been deleted'
        dept_queryset.update(is_deleted=1)
        return True, ''

    @classmethod
    @auto_log
    def get_token_list(cls, search_value: str, page: int=1, per_page: int=10, simple=False)->tuple:
        """
        get app permission token list
        :param search_value: support app name fuzzy queries
        :param page:
        :param per_page:
        :param simple: 返回简易数据，排除敏感信息
        :return:
        """
        query_params = Q(is_deleted=False)
        if search_value:
            query_params &= Q(app_name__contains=search_value)
        token_objects = AppToken.objects.filter(query_params)
        paginator = Paginator(token_objects, per_page)
        try:
            token_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            token_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            token_result_paginator = paginator.page(paginator.num_pages)
        token_result_object_list = token_result_paginator.object_list
        token_result_object_format_list = []

        for token_result_object in token_result_object_list:
            app_list = [token_result_object.app_name for token_result_object in token_result_object_list]
            # todo: get token permission workflow list
            from service.workflow.workflow_permission_service import workflow_permission_service_ins
            flag, result = workflow_permission_service_ins.get_record_list_by_app_list(app_list)
            permission_list = result.get('permission_query_set')

            token_result_data = token_result_object.get_dict()
            token_workflow_list = []
            if simple:
                token_result_data.pop('token')
            else:
                for permission in permission_list:
                    if permission.user == token_result_data.get('app_name'):
                        token_workflow_list.append(str(permission.workflow_id))
            token_result_data['workflow_ids'] = ','.join(token_workflow_list)

            token_result_object_format_list.append(token_result_data)
        return True, dict(token_result_object_format_list=token_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_token_record(cls, app_name: str, ticket_sn_prefix: str, workflow_ids: str, username: str)-> tuple:
        """
        add app token record
        :param app_name:
        :param ticket_sn_prefix:
        :param workflow_ids:
        :param username:
        :return:
        """
        import uuid
        token = uuid.uuid1()
        query_result = AppToken.objects.filter(app_name=app_name, is_deleted=0)
        if query_result:
            return False, 'app_name existed,please alter app_name'
        app_token_obj = AppToken(app_name=app_name, ticket_sn_prefix=ticket_sn_prefix,
                                 token=token, creator=username)
        app_token_obj.save()

        from apps.workflow.models import WorkflowUserPermission
        permission_sql_list = []
        if workflow_ids:
            for workflow_id in workflow_ids.split(','):
                permission_sql_list.append(WorkflowUserPermission(workflow_id=int(workflow_id), permission='api', user_type='app', user=app_name))
        WorkflowUserPermission.objects.bulk_create(permission_sql_list)

        return True, dict(app_token_id=app_token_obj.id)

    @classmethod
    @auto_log
    def update_token_record(cls, app_token_id: int, ticket_sn_prefix: str, workflow_ids: str)->tuple:
        """
        update token record
        :param app_token_id:
        :param ticket_sn_prefix:
        :param workflow_ids:
        :return:
        """
        app_token_obj = AppToken.objects.filter(id=app_token_id, is_deleted=0).first()
        if not app_token_obj:
            return False, 'record is not exist or has been deleted'

        app_token_obj.ticket_sn_prefix = ticket_sn_prefix
        app_token_obj.save()

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        workflow_permission_service_ins.update_app_permission(app_token_obj.app_name, workflow_ids)
        return True, ''

    @classmethod
    @auto_log
    def del_token_record(cls, app_token_id: int)->tuple:
        """
        del app token record
        :param app_token_id:
        :return:
        """
        app_token_obj = AppToken.objects.filter(id=app_token_id, is_deleted=0).first()
        if not app_token_obj:
            return False, 'record is not exist or has been deleted'
        app_token_obj.is_deleted = True
        app_token_obj.save()

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        workflow_permission_service_ins.del_app_permission(app_token_obj.app_name)
        return True, ''

    @classmethod
    @auto_log
    def admin_permission_check(cls, username: str='', user_id: int=0)->tuple:
        """
        admin permission check
        :param username:
        :param user_id:
        :return:
        """
        if username:
            flag, result = cls.get_user_by_username(username)
        elif user_id:
            flag, result = cls.get_user_by_user_id(user_id)
        else:
            return False, 'username or user_id is needed'
        if flag is False:
            return False, result
        if result.type_id == constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN:
            return True, 'user is admin'
        else:
            return False, 'user is not admin'

    @classmethod
    @auto_log
    def workflow_admin_permission_check(cls, username: str='', user_id: int=0)->tuple:
        """
        workflow admin permission check
        :param username:
        :param user_id:
        :return:
        """
        if username:
            flag, result = cls.get_user_by_username(username)
        elif user_id:
            flag, result = cls.get_user_by_username(username)
        else:
            return False, 'username or user_id is needed'
        if flag is False:
            return False, result
        if result.type_id == constant_service_ins.ACCOUNT_TYPE_WORKFLOW_ADMIN:
            return True, 'user is workflow admin'
        if result.type_id == constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN:
            return True, 'user is admin'
        else:
            return False, 'user is not admin or workflow admin'

    @classmethod
    @auto_log
    def admin_or_workflow_admin_check(cls, username: str='', user_id: int=0)-> tuple:
        """
        admin or workflow admin check
        :param username:
        :param user_id:
        :return:
        """
        if username:
            flag, result = cls.get_user_by_username(username)
        elif user_id:
            flag, result = cls.get_user_by_username(username)
        else:
            return False, 'username or user_id is needed'
        if flag is False:
            return False, result
        if result.type_id in (constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN, constant_service_ins.ACCOUNT_TYPE_WORKFLOW_ADMIN):
            return True, 'user is admin or workflow admin'
        else:
            return False, 'user is not admin or workflow admin'

    @classmethod
    @auto_log
    def reset_password(cls, username: str='', user_id: int=0)-> tuple:
        """
        reset user's password
        just admin or workflow admin need login loonflow's admin,so just admin and workflow admin can rest password
        :param username:
        :param user_id:
        :return:
        """
        flag, result = False, ''
        if username:
            flag, result = cls.get_user_by_username(username)
        if user_id:
            flag, result = cls.get_user_by_user_id(user_id)

        if flag:
            user_obj = result
            # if user_obj.type_id in (constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN, constant_service_ins.ACCOUNT_TYPE_WORKFLOW_ADMIN):
            password_str = make_password('123456', None, 'pbkdf2_sha256')
            user_obj.password = password_str
            user_obj.save()
            return True, 'password has been reset to 123456'
            # else:
            #     return False, 'just admin or workflow admin can be reset password'
        else:
            return False, result

    @classmethod
    @auto_log
    def get_user_jwt(cls, username: str)->tuple:
        """
        get user's jwt
        :param username:
        :return:
        """
        flag, user_obj = cls.get_user_by_username(username)
        if flag is False:
            return False, user_obj
        user_info = user_obj.get_dict()
        timestamp = int(time.time())
        jwt_salt = settings.JWT_SALT
        jwt_info = jwt.encode(
                              {
                                  'exp': datetime.datetime.now() + datetime.timedelta(hours=24),
                                  'iat': datetime.datetime.now(),
                                  'data': user_info},  jwt_salt, algorithm='HS256')
        return True, jwt_info

    @classmethod
    @auto_log
    def change_password(cls, username: str, source_password: str, new_password: str)->tuple:
        """
        修改密码
        :param username:
        :param source_password:
        :param new_password:
        :return:
        """
        flag, user_obj = cls.get_user_by_username(username)
        if flag is False:
            return False, user_obj

        user = authenticate(username=username, password=source_password)
        if user is None:
            return False, '原密码输入错误，不允许修改密码'
        new_password_format = make_password(new_password, None, 'pbkdf2_sha256')

        user_obj.password = new_password_format
        user_obj.save()
        return True, '密码修改成功'


account_base_service_ins = AccountBaseService()
