from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.account.models import UserRole, User, Role
from service.base_service import BaseService
from service.common.log_service import auto_log


class AccountRoleService(BaseService):
    @classmethod
    @auto_log
    def get_role_user_info_by_role_id(cls, role_id: int, search_value: str = '', page: int = 1,
                                      per_page: int = 10) -> tuple:
        """
        get role's user info list by role_id
        :param role_id:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        user_role_queryset = UserRole.objects.filter(role_id=role_id).all()
        role_user_id_list = [user_role.user_id for user_role in user_role_queryset]
        query_params = Q(is_deleted=False, id__in=role_user_id_list)
        if search_value:
            query_params &= Q(username__contains=search_value) | Q(alias__contains=search_value)
        user_info_queryset = User.objects.filter(query_params).all()
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
    def get_role_by_id(cls, role_id: int) -> tuple:
        """
        get role's info by role_id
        :param role_id:
        :return:
        """
        return True, Role.objects.filter(id=role_id, is_deleted=False).first()

    @classmethod
    @auto_log
    def get_role_list(cls, search_value: str, page: int = 1, per_page: int = 10) -> tuple:
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
        user_objects = Role.objects.filter(query_params)
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
    def add_role(cls, name: str, description: str, label: str, creator: str) -> tuple:
        """
        add role
        :param name:
        :param description:
        :param label:
        :param creator:
        :return:
        """
        role_obj = Role(name=name, description=description, label=label, creator=creator)
        role_obj.save()
        return True, dict(role_id=role_obj.id)

    @classmethod
    @auto_log
    def add_role_user(cls, role_id: int, user_id: int, creator: str) -> tuple:
        """
        add role's user
        :param role_id:
        :param user_id:
        :param creator:
        :return:
        """
        # 去重下
        role_user_queryset = UserRole.objects.filter(user_id=user_id, role_id=role_id)
        if role_user_queryset:
            return False, 'user has been existed in this role'
        role_user_obj = UserRole(user_id=user_id, role_id=role_id, creator=creator)
        role_user_obj.save()
        return True, dict(role_user_id=role_user_obj.id)

    @classmethod
    @auto_log
    def delete_role_user(cls, user_id: int) -> tuple:
        """
        删除角色用户
        :param user_id:
        :return:
        """
        role_user_obj = UserRole.objects.filter(user_id=user_id)
        if not role_user_obj:
            return False, 'record is not existed or has been deleted'
        role_user_obj.update(is_deleted=1)
        return True, ''

    @classmethod
    @auto_log
    def update_role(cls, role_id: int, name: str, description: str, label: str) -> tuple:
        """
        update role
        更新角色
        :param role_id:
        :param name:
        :param description:
        :param label:
        :return:
        """
        role_queryset = Role.objects.filter(id=role_id)
        if not role_queryset:
            return False, 'role record is not existed'
        role_queryset.update(name=name, description=description, label=label)
        return True, {}

    @classmethod
    @auto_log
    def delete_role(cls, role_id: int) -> tuple:
        """
        delete role record
        删除角色
        :param role_id:
        :return:
        """
        role_queryset = Role.objects.filter(id=role_id)
        if not role_queryset:
            return False, 'role record is not existed'
        role_queryset.update(is_deleted=1)
        return True, {}

    @classmethod
    @auto_log
    def get_role_username_list(cls, role_id: int) -> tuple:
        """
        get role's username list by role_id
        :param role_id:
        :return:
        """
        user_role_queryset = UserRole.objects.filter(role_id=role_id).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return True, []
        username_queryset = User.objects.filter(id__in=user_id_list).all()
        username_list = []
        for username_obj in username_queryset:
            username_list.append(username_obj.username)
        return True, username_list

account_role_service_ins = AccountRoleService()
