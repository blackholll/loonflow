import json
import time
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from apps.account.models import User, UserRole, Dept, Role, UserDept, Application
from service.util.archive_service import ArchiveService
from service.base_service import BaseService
from service.common.constant_service import constant_service_ins
from service.common.log_service import auto_log


class AccountBaseService(BaseService):
    """
    account
    """

    @classmethod
    @auto_log
    def get_token_by_app_name(cls, app_name: str) -> tuple:
        """
        get app's call token by app_name
        :param app_name:
        :return:
        """
        app_token_obj = Application.objects.filter(app_name=app_name).first()
        return True, app_token_obj








    @classmethod
    @auto_log
    def app_workflow_permission_list(cls, app_name: str) -> tuple:
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

        app_token_obj = Application.objects.filter(app_name=app_name).first()
        if not app_token_obj:
            return False, 'appname is unauthorized'

    @classmethod
    @auto_log
    def app_workflow_permission_check(cls, app_name: str, workflow_id: int) -> tuple:
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
    def app_ticket_permission_check(cls, app_name: str, ticket_id: int) -> tuple:
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
        permission_check, msg = workflow_permission_service_ins.workflow_id_permission_check(workflow_id, 'api', 'app',
                                                                                             app_name)

        if not permission_check:
            return False, msg
        return True, ''








    @classmethod
    @auto_log
    def get_token_list(cls, search_value: str, page: int = 1, per_page: int = 10, simple=False) -> tuple:
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
        token_objects = Application.objects.filter(query_params)
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
    def add_token_record(cls, app_name: str, ticket_sn_prefix: str, workflow_ids: str, username: str) -> tuple:
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
        query_result = Application.objects.filter(app_name=app_name)
        if query_result:
            return False, 'app_name existed,please alter app_name'
        app_token_obj = Application(app_name=app_name, ticket_sn_prefix=ticket_sn_prefix,
                                    token=token, creator=username)
        app_token_obj.save()

        from apps.workflow.models import WorkflowUserPermission
        permission_sql_list = []
        if workflow_ids:
            for workflow_id in workflow_ids.split(','):
                permission_sql_list.append(
                    WorkflowUserPermission(workflow_id=int(workflow_id), permission='api', user_type='app',
                                           user=app_name))
        WorkflowUserPermission.objects.bulk_create(permission_sql_list)

        return True, dict(app_token_id=app_token_obj.id)

    @classmethod
    @auto_log
    def update_token_record(cls, app_token_id: int, ticket_sn_prefix: str, workflow_ids: str) -> tuple:
        """
        update token record
        :param app_token_id:
        :param ticket_sn_prefix:
        :param workflow_ids:
        :return:
        """
        app_token_obj = Application.objects.filter(id=app_token_id).first()
        if not app_token_obj:
            return False, 'record is not exist or has been deleted'

        app_token_obj.ticket_sn_prefix = ticket_sn_prefix
        app_token_obj.save()

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        workflow_permission_service_ins.update_app_permission(app_token_obj.app_name, workflow_ids)
        return True, ''

    @classmethod
    @auto_log
    def del_token_record(cls, app_token_id: int) -> tuple:
        """
        del app token record
        :param app_token_id:
        :return:
        """
        app_token_obj = Application.objects.filter(id=app_token_id).first()
        if not app_token_obj:
            return False, 'record is not exist or has been deleted'
        app_token_obj.is_deleted = True
        app_token_obj.save()

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        workflow_permission_service_ins.del_app_permission(app_token_obj.app_name)
        return True, ''

    @classmethod
    @auto_log
    def admin_permission_check(cls, username: str = '', user_id: int = 0) -> tuple:
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
    def workflow_admin_permission_check(cls, username: str = '', user_id: int = 0) -> tuple:
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
    def admin_or_workflow_admin_check(cls, username: str = '', user_id: int = 0) -> tuple:
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
        if result.type_id in (
        constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN, constant_service_ins.ACCOUNT_TYPE_WORKFLOW_ADMIN):
            return True, 'user is admin or workflow admin'
        else:
            return False, 'user is not admin or workflow admin'








account_base_service_ins = AccountBaseService()
