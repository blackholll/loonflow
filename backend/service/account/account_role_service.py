import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.account.models import UserRole, User, Role
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins


class AccountRoleService(BaseService):
    @classmethod
    def get_role_user_info_by_role_id(cls, role_id: int, search_value: str = '', page: int = 1,
                                      per_page: int = 10) -> dict:
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
        query_params = Q(id__in=role_user_id_list)
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
        return dict(user_list=user_result_format_list, per_page=per_page, page=page, total=paginator.count)

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
    def get_role_detail(cls, role_id: int) -> dict:
        """
        get role detail
        :param role_id:
        :return:
        """
        try:
            role_obj = Role.objects.get(id=role_id)
        except Role.DoesNotExist as e:
            raise CustomCommonException("role is not exist or has been deleted")
        except Exception:
            raise

        return role_obj.get_dict()

    @classmethod
    def get_role_list(cls, search_value: str, role_ids: str, page: int = 1, per_page: int = 10, simple:bool = False) -> dict:
        """
        get role list
        get role restful list by search params
        :param search_value: role name or role description Support fuzzy queries
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q()
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
        if role_ids:
            query_params &= Q(id__in=role_ids.split(','))
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
        need_remove_field_list = ["creator_info", "created_at", "updated_at", "label", "tenant_id"]
        for role_result_object in role_result_object_list:
            role_obj = role_result_object.get_dict()
            if simple:
                for need_remove_field in need_remove_field_list:
                    role_obj.pop(need_remove_field)
            role_result_object_format_list.append(role_obj)

        return dict(role_result_object_format_list=role_result_object_format_list,
                    paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    def add_role(cls, name: str, description: str, label: str, tenant_id: int, creator_id: int) -> str:
        """
        add role
        :param name:
        :param description:
        :param label:
        :param tenant_id:
        :param creator_id:
        :return:
        """
        role_obj = Role(name=name, description=description, label=label, tenant_id=tenant_id, creator_id=creator_id)
        role_obj.save()
        return str(role_obj.id)

    @classmethod
    def add_role_user(cls, role_id: int, user_id_list: int, creator: str) -> bool:
        """
        add role's user
        :param role_id:
        :param user_id_list:
        :param creator:
        :return:
        """
        role_user_queryset = UserRole.objects.filter(role_id=role_id).all()
        need_add_user_list = []
        exist_user_id_list = [role_user.user_id for role_user in role_user_queryset]
        for user_id in user_id_list:
            if user_id not in exist_user_id_list:
                user_role_obj = UserRole(role_id=role_id, user_id=user_id)
                need_add_user_list.append(user_role_obj)
                time.sleep(0.001)  # temporarily for SnowflakeIDGenerator bug
        UserRole.objects.bulk_create(need_add_user_list)
        return True

    @classmethod
    def delete_role_user(cls, role_user_id_list: list, operator_id:int) -> bool:
        """
        del role user
        :param role_user_id_list:
        :param operator_id:
        :return:
        """

        role_user_queryset = UserRole.objects.filter(id__in=role_user_id_list).all()
        archive_service_ins.archive_record_list("UserRole", role_user_queryset, operator_id)
        return True

    @classmethod
    def update_role(cls, tenant_id: str, role_id: str, name: str, description: str, label: dict) -> bool:
        """
        update role record
        :param role_id:
        :param name:
        :param description:
        :param label:
        :return:
        """
        try:
            Role.objects.get(id=role_id)
        except Role.DoesNotExist as e:
            raise CustomCommonException("role is not exist or has been deleted")
        role_queryset = Role.objects.filter(id=role_id)
        role_queryset.update(name=name, description=description, label=label)
        return True

    @classmethod
    def delete_role(cls, role_id: int, operator_id: int) -> bool:
        """
        delete role record
        :param role_id:
        :param operator_id:
        :return:
        """
        role_queryset = Role.objects.filter(id=role_id)
        if not role_queryset:
            raise CustomCommonException("role is not exist or has been deleted")
        archive_service_ins.archive_record("Role", role_queryset[0], operator_id)
        return True

    @classmethod
    def batch_delete_role(cls, role_id_list: list, operator_id:int) -> bool:
        """
        batch delete role
        :param role_id_list:
        :param operator_id:
        :return:
        """
        record_queryset = Role.objects.filter(id__in=role_id_list)
        archive_service_ins.archive_record_list("Role", record_queryset, operator_id)
        return True

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
