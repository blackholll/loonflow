import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from apps.account.models import AppToken, LoonUser, LoonUserRole, LoonDept, LoonRole
from service.base_service import BaseService
from service.common.log_service import auto_log


class AccountBaseService(BaseService):
    """
    account
    """
    @classmethod
    @auto_log
    def get_token_by_app_name(cls, app_name):
        """
        get app's call token by app_name
        :param app_name:
        :return:
        """
        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        return True, app_token_obj

    @classmethod
    @auto_log
    def get_user_by_username(cls, username):
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
    def get_user_by_user_id(cls, user_id):
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
    def get_user_name_list_by_id_list(cls, user_id_list):
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
    def get_user_role_id_list(cls, username):
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
    def get_user_role_info_by_user_id(cls, user_id, search_value=0, page=1, per_page=10):
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
                          paginator_info=dict(per_page=per_page,page=page, total=paginator.count))

    @classmethod
    @auto_log
    def get_role_user_info_by_role_id(cls, role_id, search_value=0, page=1, per_page=10):
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
    def get_user_up_dept_id_list(cls, username):
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

        iter_dept(user_obj.dept_id)
        return True, dept_id_list

    @classmethod
    @auto_log
    def get_user_dept_approver(cls, username):
        """
        get user's department approver， Preferential access to the approver, without taking tl（team leader）
        :param username:
        :return:
        """
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        loon_dept_obj = LoonDept.objects.filter(id=user_obj.dept_id).first()
        if loon_dept_obj.approver:
            return True, loon_dept_obj.approver
        else:
            return True, loon_dept_obj.leader

    @classmethod
    @auto_log
    def get_dept_sub_dept_id_list(cls, dept_id):
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

        def iter_dept_id_list(dept_id):
            dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                sub_dept_queryset = LoonDept.objects.filter(parent_dept_id=dept_obj.id, is_deleted=0).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return True, dept_id_list

    @classmethod
    @auto_log
    def get_dept_username_list(cls, dept_id):
        """
        get department's all username list
        :param dept_id:
        :return:
        """
        flag, sub_dept_id_list = cls.get_dept_sub_dept_id_list(dept_id)
        if flag is False:
            return False, sub_dept_id_list
        user_name_list = []
        if sub_dept_id_list:
            user_queryset = LoonUser.objects.filter(dept_id__in = sub_dept_id_list).all()
            for user in user_queryset:
                user_name_list.append(user.username)
        return True, user_name_list

    @classmethod
    @auto_log
    def get_role_username_list(cls, role_id):
        """
        get role's username list by role_id
        :param role_id:
        :return:
        """
        user_role_queryset = LoonUserRole.objects.filter(role_id=role_id).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return True, []
        username_queryset = LoonUser.objects.filter(id__in=(user_id_list)).all()
        username_list = []
        for username_obj in username_queryset:
            username_list.append(username_obj.username)
        return True, username_list

    @classmethod
    @auto_log
    def get_dept_by_id(cls, dept_id):
        """
        get department's info by dept_id
        :param dept_id:
        :return:
        """
        return True, LoonDept.objects.filter(id=dept_id, is_deleted=False).first()

    @classmethod
    @auto_log
    def get_role_by_id(cls, role_id):
        """
        get role's info by role_id
        :param role_id:
        :return:
        """
        return LoonRole.objects.filter(id=role_id, is_deleted=False).first(), ''

    @classmethod
    @auto_log
    def app_workflow_permission_list(cls, app_name):
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
            return True, workflow_id_list

        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        if not app_token_obj:
            return False, 'appname is unauthorized'
        workflow_ids = app_token_obj.workflow_ids
        if workflow_ids:
            workflow_id_list = workflow_ids.split(',')
            workflow_id_list = [int(workflow_id) for workflow_id in workflow_id_list]
            return True, workflow_id_list
        else:
            return True, []

    @classmethod
    @auto_log
    def app_workflow_permission_check(cls, app_name, workflow_id):
        """
        appname has permission for workflow check by app_name and workflow_id
        :param app_name:
        :param workflow_id:
        :return:
        """
        if app_name == 'loonflow':
            return True, ''
        flag, app_workflow_permission_list = cls.app_workflow_permission_list(app_name)

        if flag and app_workflow_permission_list and workflow_id in app_workflow_permission_list:
            return True, ''
        else:
            return False, 'the app has no permission to the workflow_id'

    @classmethod
    @auto_log
    def app_ticket_permission_check(cls, app_name, ticket_id):
        """
        appname has permission to ticket check by app_name and ticket_id
        :param app_name:
        :param ticket_id:
        :return:
        """
        from service.ticket.ticket_base_service import TicketBaseService
        # ticket_obj, msg = TicketBaseService.get_ticket_by_id(ticket_id)
        flag, ticket_obj = TicketBaseService.get_ticket_by_id(ticket_id)
        if not flag:
            return False, ticket_obj
        workflow_id = ticket_obj.workflow_id
        permission_check, msg = cls.app_workflow_permission_check(app_name, workflow_id)
        if not permission_check:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def get_user_list(cls, search_value, page=1, per_page=10):
        """
        get user restful info list by query params: search_value, page, per_page
        :param search_value: support user's username, and user's alias. fuzzy query
        :param page:
        :param per_page:
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
        for user_result_object in user_result_object_list:
            user_result_object_format_list.append(user_result_object.get_dict())

        return True, dict(user_result_object_format_list=user_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_user(cls, username, alias, email, phone, dept_id, is_active, is_admin, is_workflow_admin, creator, password=''):
        """
        新增用户， 因为非管理员或者工作流管理员无需登录管理后台，密码字段留空
        add user, not support set password, you need reset password
        :param username:
        :param alias:
        :param email:
        :param phone:
        :param dept_id:
        :param is_active:
        :param is_admin:
        :param is_workflow_admin:
        :param creator:
        :param password:
        :return:
        """
        password_str = make_password(password, None, 'pbkdf2_sha256')
        user_obj = LoonUser(username=username, alias=alias, email=email, phone=phone, dept_id=dept_id,
                            is_active=is_active, is_admin=is_admin, is_workflow_admin=is_workflow_admin,
                            creator=creator, password=password_str)
        user_obj.save()
        return True, dict(user_id=user_obj.id)

    @classmethod
    @auto_log
    def edit_user(cls, user_id, username, alias, email, phone, dept_id, is_active, is_admin, is_workflow_admin):
        """
        edit user
        :param user_id:
        :param username:
        :param alias:
        :param email:
        :param phone:
        :param dept_id:
        :param is_active:
        :param is_admin:
        :param is_workflow_admin:
        :return:
        """
        user_obj = LoonUser.objects.filter(id=user_id, is_deleted=0)
        user_obj.update(username=username, alias=alias, email=email, phone=phone, dept_id=dept_id, is_active=is_active,
                        is_admin=is_admin, is_workflow_admin=is_workflow_admin)
        user_obj.save()
        return True, {}

    @classmethod
    @auto_log
    def delete_user(cls, user_id):
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
    def get_role_list(cls, search_value, page=1, per_page=10):
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
    def add_role(cls, name, description, label, creator):
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
    def add_role_user(cls, role_id, user_id, creator):
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
    def delete_role_user(cls, role_user_id):
        """
        删除角色用户
        :param role_user_id:
        :return:
        """
        role_user_obj = LoonUserRole.objects.filter(id=role_user_id, is_deleted=0)
        if not role_user_obj:
            return False, 'record is not existed or has been deleted'
        role_user_obj.update(is_deleted=1)
        return True, ''

    @classmethod
    @auto_log
    def update_role(cls, role_id, name, description, label):
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
    def delete_role(cls, role_id):
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
    def get_dept_list(cls, search_value, page=1, per_page=10):
        """
        get dept restful list by search params
        :param search_value: department name or department description Support fuzzy queries
        :param page:
        :param per_page:
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
            dept_result_object_format_list.append(dept_result_object.get_dict())
        return True, dict(dept_result_object_format_list=dept_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_dept(cls, name, parent_dept_id, leader, approver, label, creator):
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
    def update_dept(cls, dept_id, name, parent_dept_id, leader, approver, label):
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
    def delete_dept(cls, dept_id):
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
    def get_token_list(cls, search_value, page=1, per_page=10):
        """
        get app permission token list
        :param search_value: support app name fuzzy queries
        :param page:
        :param per_page:
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
            token_result_object_format_list.append(token_result_object.get_dict())
        return True, dict(token_result_object_format_list= token_result_object_format_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_token_record(cls, app_name, ticket_sn_prefix, workflow_ids, username):
        """
        add app token record
        :param app_name:
        :param ticket_sn_prefix:
        :param workflows_ids:
        :return:
        """
        import uuid
        token = uuid.uuid1()
        app_token_obj = AppToken(app_name=app_name, ticket_sn_prefix=ticket_sn_prefix, workflow_ids=workflow_ids, token=token, creator=username)
        app_token_obj.save()
        return True, dict(app_token_id=app_token_obj.id)

    @classmethod
    @auto_log
    def update_token_record(cls, app_token_id, app_name, ticket_sn_prefix, workflow_ids):
        """
        update token record
        :param app_token_id:
        :param app_name:
        :param ticket_sn_prefix:
        :param workflow_ids:
        :return:
        """
        app_token_obj = AppToken.objects.filter(id=app_token_id, is_deleted=0).first()
        if not app_token_obj:
            return False, 'record is not exist or has been deleted'
        app_token_obj.app_name = app_name
        app_token_obj.ticket_sn_prefix = ticket_sn_prefix
        app_token_obj.workflow_ids = workflow_ids
        app_token_obj.save()
        return True, ''

    @classmethod
    @auto_log
    def del_token_record(cls, app_token_id):
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
        return True, ''

    @classmethod
    @auto_log
    def admin_permission_check(cls, username='', user_id=0):
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
        if result.is_admin:
            return True, 'user is admin'
        else:
            return False, 'user is not admin'

    @classmethod
    @auto_log
    def workflow_admin_permission_check(cls, username='', user_id=0):
        """
        workflow admin permission check
        :param username:
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
        if result.is_workflow_admin:
            return True, 'user is workflow admin'
        else:
            return False, 'user is not workflow admin'

    @classmethod
    @auto_log
    def admin_or_workflow_admin_check(cls, username='', user_id=0):
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
        if result.is_workflow_admin or result.is_admin:
            return True, 'user is admin or workflow admin'
        else:
            return False, 'user is not admin or workflow admin'

    @classmethod
    @auto_log
    def reset_password(cls, username='', user_id=''):
        """
        reset user's password
        just admin or workflow admin need login loonflow's admin,so just admin and workflow admin can rest password
        :param username:
        :param user_id:
        :return:
        """
        if username:
            flag, result = cls.get_user_by_username(username)
        if user_id:
            flag, result = cls.get_user_by_user_id(user_id)

        if flag:
            user_obj = result
            if user_obj.is_admin or user_obj.is_workflow_admin:
                password_str = make_password('123456', None, 'pbkdf2_sha256')
                user_obj.password = password_str
                user_obj.save()
                return True, 'password has been reset to 123456'
            else:
                return False, 'just admin or workflow admin can be reset password'
        else:
            return False, result
