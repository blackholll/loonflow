import uuid

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.account.models import Application
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins


class AccountApplicationService(BaseService):

    @classmethod
    def add_application(cls, tenant_id: int, operator_id: int, name: str, description: str, type: str) -> str:
        """
        add application record
        :param tenant_id:
        :param operator_id:
        :param name:
        :param description:
        :param type:
        :return:
        """
        token = uuid.uuid4()
        application_obj = Application(tenant_id=tenant_id, creator_id=operator_id, name=name, description=description, type=type, token=token)
        application_obj.save()
        return str(application_obj.id)

    @classmethod
    def get_application_list(cls, tenant_id: int, search_value: str, app_ids: str, page: int, per_page: int, simple=False, type='all') -> dict:
        """
        get application list
        :param tenant_id:
        :param search_value:
        :param app_ids:
        :param page:
        :param per_page:
        :param simple:
        :return:
        """
        query_params = Q(tenant_id=tenant_id)
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
        if type != 'all':
            query_params &= Q(type=type)
        if app_ids:
            query_params &= Q(id__in=app_ids.split(','))
        application_queryset = Application.objects.filter(query_params).order_by("id")
        paginator = Paginator(application_queryset, per_page)
        try:
            application_paginator = paginator.page(page)
        except PageNotAnInteger:
            application_paginator = paginator.page(1)
        except EmptyPage:
            application_paginator = paginator.page(paginator.num_pages)
        application_object_list = application_paginator.object_list
        application_result_list = []
        for application_object in application_object_list:
            result = application_object.get_dict()
            if simple:
                need_del_field_list = ["label", "creator_info", "created_at", "updated_at", "token", "tenant_id"]
                for need_del_field in need_del_field_list:
                    result.pop(need_del_field)
            application_result_list.append(result)

        return dict(application_list=application_result_list, per_page=per_page, page=page, total=paginator.count)

    @classmethod
    def batch_delete_application_list(cls, tenant_id: str, operator_id: int, application_id_list: list) -> bool:
        """
        batch delete application list
        :param tenant_id:
        :param operator_id:
        :param application_id_list:
        :return:
        """
        application_queryset = Application.objects.filter(tenant_id=tenant_id, id__in=application_id_list)
        archive_service_ins.archive_record_list("Application", application_queryset, operator_id)
        return True

    @classmethod
    def get_application_detail(cls, tenant_id:str, application_id: str) -> dict:
        """
        get application detail
        :param tenant_id:
        :param application_id:
        :return:
        """
        try:
            application_obj = Application.objects.get(tenant_id=tenant_id, id=application_id)
        except Application.DoesNotExist as e:
            raise CustomCommonException("application is not not exist or has been deleted")
        except Exception:
            raise
        return application_obj.get_dict()

    @classmethod
    def update_application_detail(cls, tenant_id:str, application_id: int, name: str, description: str, type: str) -> bool:
        """
        update application detail
        :param tenant_id:
        :param application_id:
        :param name:
        :param description:
        :param type:
        :return:
        """
        application_queryset = Application.objects.filter(tenant_id=tenant_id, id=application_id)
        if not application_queryset:
            raise CustomCommonException('application is not exist or has been deleted')
        application_queryset.update(name=name, description=description, type=type)
        return True

    @classmethod
    def app_type_check(cls, tenant_id:str, application_name:str, type:str, workflow_id:str)->bool:
        """
        check application type
        :param tenant_id:
        :param application_name:
        :param type:
        :return:
        """
        app_record = Application.objects.get(id=tenant_id, name=application_name)
        app_type = app_record.type
        if type == 'admin':
            if app_type == 'admin':
                return True
            raise CustomCommonException(f'permission check fail, need {type}')
        elif type == 'workflow_admin':
            if app_type == 'admin':
                return True
            else:
                if not cls.application_workflow_checker(tenant_id, app_record.id, workflow_id):
                    raise CustomCommonException(f'permission check fail, need admin or workflow_admin')
                return True
    @classmethod
    def application_workflow_checker(cls, tenant_id:str, application_id:str, workflow_id:str):
        """
        check where application is workflow admin of one workflow
        """
        try:
            ApplicationWorkflow.objects.get(tenant_id=tenant_id, application_id=application_id, workflow_id=workflow_id)
            return True
        except Exception as e:
            return  False


account_application_service_ins = AccountApplicationService()
