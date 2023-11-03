import json
import time
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.account.models import User, UserDept, UserRole, Role, Dept
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.exception.custom_common_exception import CustomCommonException


class AccountUserService(BaseService):

    @classmethod
    @auto_log
    def user_type_check(cls, email: str = "", user_id: int = 0, types: str = "") -> tuple:
        """
        user type check
        :param email:
        :param user_id:
        :param types:
        :return:
        """
        if email:
            flag, result = cls.get_user_by_email(email)
        elif user_id:
            flag, result = cls.get_user_by_user_id(user_id)
        else:
            return False, 'username or user_id is needed'
        if flag is False:
            return False, result
        if result.type in (types.split(',')):
            return True, 'user type matched'
        else:
            return False, 'user type is not match'

    @classmethod
    @auto_log
    def get_user_by_username(cls, username: str) -> tuple:
        """
        get user info by username
        :return:
        """
        result = User.objects.filter(username=username).first()
        if result:
            return True, result
        else:
            return False, 'username: {} is not existed or has been deleted'.format(username)

    @classmethod
    @auto_log
    def get_user_by_email(cls, email: str) -> tuple:
        """
        get user info by email
        :return:
        """
        result = User.objects.filter(email=email).first()
        if result:
            return True, result
        else:
            return False, 'user: {} is not existed or has been deleted'.format(email)

    @classmethod
    @auto_log
    def get_user_list_by_usernames(cls, usernames: list) -> tuple:
        """
        get user info by username
        :return:
        """
        result = User.objects.filter(username__in=usernames).all()
        if result:
            return True, result
        else:
            return False, 'usernames: {} is not existed or has been deleted'.format(usernames)

    @classmethod
    @auto_log
    def get_user_by_user_id(cls, user_id: int) -> tuple:
        """
        get user by user id
        :param user_id:
        :return:
        """
        result = User.objects.filter(id=user_id).first()
        if result:
            return True, result
        else:
            return False, 'user_id: {} is not existed or has been deleted'.format(user_id)

    def get_user_format_by_user_id(self, user_id) ->dict:
        """
        get user's format info
        :param user_id:
        :return:
        """
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise CustomCommonException("user is not exist or has been deleted")
        except Exception:
            raise
        user_result = user_obj.get_dict()
        user_dept_list = UserDept.objects.filter(user_id=user_id)
        user_dept_info_list = []
        for user_dept in user_dept_list:
            user_dept_info_list.append(
                dict(name=user_dept.dept.name, id=user_dept.dept.id))
        user_result['department'] = user_dept_info_list
        return user_result


    @classmethod
    @auto_log
    def get_user_name_list_by_id_list(cls, user_id_list: list) -> tuple:
        """
        get username list by user id list
        根据用户id的数组获取用户名的list
        :param user_id_list:
        :return:
        """
        user_queryset = User.objects.filter(id__in=user_id_list).all()
        if not user_queryset:
            return False, 'user id is not existed or has been deleted'
        username_list = [user_query.username for user_query in user_queryset]
        return True, dict(username_list=username_list)

    @classmethod
    @auto_log
    def get_user_role_id_list(cls, username: str) -> tuple:
        """
        get user's role id list by username
        :param username:
        :return:
        """
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            return False, 'user is not existed or has been deleted'
        user_role_queryset = UserRole.objects.filter(user_id=user_obj.id).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        return True, user_role_id_list

    @classmethod
    @auto_log
    def get_user_role_info_by_user_id(cls, user_id: int, search_value: str = 0, page: int = 1,
                                      per_page: int = 10) -> tuple:
        """
        get user's role info list by user's id and query params: role name、page、per_page
        :param user_id:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        user_role_queryset = UserRole.objects.filter(user_id=user_id).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        query_params = Q(is_deleted=False, id__in=user_role_id_list)
        if search_value:
            query_params &= Q(name__contains=search_value)
        role_info_queryset = Role.objects.filter(query_params).all()
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
    def get_user_jwt(cls, email: str) -> tuple:
        """
        get user's jwt
        :param email:
        :return:
        """
        flag, user_obj = cls.get_user_by_email(email)
        if flag is False:
            return False, user_obj
        user_info = user_obj.get_dict()
        user_info.pop('last_login')
        user_info.pop('created_at')
        user_info.pop('updated_at')
        # user_info.pop('creator')
        jwt_salt = settings.JWT_SALT
        jwt_info = jwt.encode(
            {
                'exp': int(time.time()) + 24 * 60 * 30,
                'iat': int(time.time()),
                'data': user_info}, jwt_salt, algorithm='HS256')
        return True, jwt_info

    @classmethod
    @auto_log
    def get_user_up_dept_id_list(cls, username: str) -> tuple:
        """
        get user's department id list by username, include parent department
        :param username:
        :return:
        """
        dept_id_list = []
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            return False, 'user is not existed or has been deleted'

        def iter_dept(dept_id):
            dept_obj = Dept.objects.filter(id=dept_id).first()
            if dept_obj:
                dept_id_list.append(dept_obj.id)
                if dept_obj.parent_dept_id:
                    iter_dept(dept_obj.parent_dept_id)

        user_dept_queryset = UserDept.objects.filter(user_id=user_obj.id).all()
        user_dept_id_list = [user_dept.dept_id for user_dept in user_dept_queryset]
        for user_dept_id in user_dept_id_list:
            iter_dept(user_dept_id)
        dept_id_list = list(set(dept_id_list))
        return True, dept_id_list

    @classmethod
    @auto_log
    def get_user_dept_approver(cls, username: str, dept_id: int = 0) -> tuple:
        """
        get user's department approver， Preferential access to the approver, without taking tl（team leader）
        :param username:
        :param dept_id: 用于用户可能属于多个部门的情况
        :return:
        """
        user_obj = User.objects.filter(username=username).first()
        if dept_id:
            if UserDept.objects.filter(user_id=user_obj.id, dept_id=dept_id).first():
                loon_dept_obj = Dept.objects.filter(id=dept_id).first()
                if loon_dept_obj.approver:
                    return True, loon_dept_obj.approver
                else:
                    return True, loon_dept_obj.leader
            else:
                return False, 'dept_id is invalid'
        else:
            # no dept id specified, get all user dept's approver
            user_dept_queryset = UserDept.objects.filter(user_id=user_obj.id)
            approver_list = []
            for user_dept in user_dept_queryset:
                if user_dept.dept.approver:
                    approver_list.extend(user_dept.dept.approver.split(','))
                else:
                    approver_list.append(user_dept.dept.leader)
            return True, ','.join(list(set(approver_list)))

    @classmethod
    @auto_log
    def get_user_dept_info(cls, username: str = '', user_id: int = 0) -> tuple:
        """
        get user dept info
        :param username:
        :param user_id:
        :return:
        """
        if username:
            user_obj = User.objects.filter(username=username).first()
            user_id = user_obj.id
        user_dept_queryset = UserDept.objects.filter(user_id=user_id).all()
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
    def get_user_list(cls, search_value: str, dept_id: int, page: int = 1, per_page: int = 10) -> dict:
        """
        get user restful info list by query params: search_value, page, per_page
        :param search_value: support user's username, and user's alias. fuzzy query
        :param dept_id:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q()
        if search_value:
            query_params &= Q(username__contains=search_value) | Q(alias__contains=search_value)
        if dept_id:
            query_params &= Q(dept__id__in=Dept.objects.filter(id=dept_id))
        user_objects = User.objects.filter(query_params).order_by("id")
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

        user_dept_list = UserDept.objects.filter(user_id__in=user_id_list)
        for user_result_object in user_result_object_list:
            user_result_format_dict = user_result_object.get_dict()
            user_dept_info_list = []
            for user_dept in user_dept_list:
                if user_result_object.id == user_dept.user_id:
                    user_dept_info_list.append(
                        dict(name=user_dept.dept.name, id=user_dept.dept.id))
            user_result_format_dict['department'] = user_dept_info_list

            user_result_object_format_list.append(user_result_format_dict)

        return dict(user_result_object_format_list=user_result_object_format_list,
                    paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    def add_user(cls, name: str, alias: str, email: str, phone: str, dept_id_list: list, role_id_list, type: str,
                 status: str, avatar: str, lang: str, creator_id: int, password: str = '', tenant_id: int = 1) -> int:
        """
        add user record
        :param name:
        :param alias:
        :param email:
        :param phone:
        :param dept_id_list:
        :param role_id_list:
        :param type:
        :param status:
        :param avatar:
        :param lang:
        :param creator_id:
        :param password:
        :return:
        """
        password_str = make_password(password, None, 'pbkdf2_sha256')
        user_obj = User(name=name, alias=alias, email=email, phone=phone,
                        status=status, type=type, avatar=avatar, lang=lang,
                        creator_id=creator_id, password=password_str, tenant_id=tenant_id)
        user_obj.save()

        queryset_list = []
        for dept_id in dept_id_list:
            queryset_list.append(UserDept(user_id=user_obj.id, dept_id=dept_id))
        UserDept.objects.bulk_create(queryset_list)
        for role_id in role_id_list:
            queryset_list.append(UserRole(user_id=user_obj.id, role_id=role_id))
        UserDept.objects.bulk_create(queryset_list)
        return user_obj.id

    @classmethod
    @auto_log
    def edit_user(cls, user_id: int, name: str, alias: str, email: str, phone: str, dept_id_list: list, role_id_list,
                  type: str,
                  status: str, avatar: str, lang: str, creator_id: int, tenant_id: int = 1) -> tuple:
        """
        update user
        :param user_id:
        :param name:
        :param alias:
        :param email:
        :param phone:
        :param dept_id_list:
        :param role_id_list:
        :param type:
        :param status:
        :param avatar:
        :param lang:
        :param creator_id:
        :param tenant_id:
        :return:
        """
        user_obj = User.objects.filter(id=user_id)
        user_obj.update(name=name, alias=alias, email=email, phone=phone,
                        status=status, type=type, avatar=avatar, lang=lang,
                        creator_id=creator_id, tenant_id=tenant_id)
        # update dept info

        user_id = user_obj.first().id
        user_dept_queryset = UserDept.objects.filter(user_id=user_id).all()
        user_dept_id_exist = [user_dept.dept_id for user_dept in user_dept_queryset]

        need_add_list = [dept_id_int for dept_id_int in dept_id_list if dept_id_int not in user_dept_id_exist]
        need_delete_list = [user_dept_id for user_dept_id in user_dept_id_exist if user_dept_id not in dept_id_list]
        add_queryset = []
        for need_add in need_add_list:
            add_queryset.append(UserDept(user_id=user_id, dept_id=need_add))
        UserDept.objects.bulk_create(add_queryset)
        UserDept.objects.filter(user_id=user_id, dept_id__in=need_delete_list).update(is_deleted=1)

        return True, {}

    @classmethod
    @auto_log
    def delete_user(cls, user_id: int, operator_id: int) -> tuple:
        """
        delete user
        :param user_id:
        :param operator_id:
        :return:
        """
        user_obj = User.objects.get(id=user_id)
        return ArchiveService.archive_record('User', user_obj, operator_id)

    @classmethod
    @auto_log
    def delete_user_list(cls, user_id_list: list, operator_id: int) -> tuple:
        """
        delete user list
        :param user_id_list:
        :param operator_id:
        :return:
        """
        if user_id_list:
            user_queryset = User.objects.filter(id__in=user_id_list).all()
            return ArchiveService.archive_record_list("User", user_queryset, operator_id)
        else:
            return False, "user_id_list can not be a blank list"

    @classmethod
    @auto_log
    def reset_password(cls, username: str = '', user_id: int = 0) -> tuple:
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
    def change_password(cls, username: str, source_password: str, new_password: str) -> tuple:
        """
        change password
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
            return False, "source password is invalid"
        new_password_format = make_password(new_password, None, 'pbkdf2_sha256')

        user_obj.password = new_password_format
        user_obj.save()
        return True, "success"


account_user_service_ins = AccountUserService()
