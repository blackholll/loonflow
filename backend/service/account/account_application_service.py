import uuid

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.account.models import Application, ApplicationWorkflow
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins


class AccountApplicationService(BaseService):

    @classmethod
    def add_application(cls, tenant_id: int, operator_id: int, name: str, description: str, type: str) -> int:
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
        return application_obj.id

    @classmethod
    def get_application_list(cls, tenant_id: int, search_value: str, page: int, per_page: int, simple=False) -> dict:
        """
        get application list
        :param tenant_id:
        :param search_value:
        :param page:
        :param per_page:
        :param simple:
        :return:
        """
        query_params = Q(tenant_id=tenant_id)
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
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
                need_del_field_list = ["label", "creator_info", "created_at", "updated_at", "type", "token", "tenant_id"]
                for need_del_field in need_del_field_list:
                    result.pop(need_del_field)
            application_result_list.append(result)

        return dict(application_list=application_result_list, per_page=per_page, page=page, total=paginator.count)

    @classmethod
    def batch_delete_application_list(cls, operator_id: int, application_id_list: list) -> bool:
        """
        batch delete application list
        :param operator_id:
        :param application_id_list:
        :return:
        """
        application_queryset = Application.objects.filter(id__in=application_id_list)
        archive_service_ins.archive_record_list("Application", application_queryset, operator_id)
        return True

    @classmethod
    def get_application_detail(cls, application_id: int) -> dict:
        """
        get application detail
        :param application_id:
        :return:
        """
        try:
            application_obj = Application.objects.get(id=application_id)
        except Application.DoesNotExist as e:
            raise CustomCommonException("application is not not exist or has been deleted")
        except Exception:
            raise
        return application_obj.get_dict()

    @classmethod
    def update_application_detail(cls, application_id: int, name: str, description: str, type: str) -> bool:
        """
        update application detail
        :param application_id:
        :param name:
        :param description:
        :param type:
        :return:
        """
        application_queryset = Application.objects.filter(id=application_id)
        if not application_queryset:
            raise CustomCommonException('application is not exist or has been deleted')
        application_queryset.update(name=name, description=description, type=type)
        return True

    @classmethod
    def get_application_workflow_list(cls, application_id: int, search_value: str, page: int, per_page: int):
        """
        get application authorized workflow_list
        :param application_id:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(application_id=application_id)
        if search_value:
            query_params &= Q(application__name__contains=search_value) | Q(application__description__contains=search_value)
        application_workflow_queryset = ApplicationWorkflow.objects.filter(query_params)
        workflow_obj_queryset = [application_workflow.workflow for application_workflow in application_workflow_queryset]

        paginator = Paginator(workflow_obj_queryset, per_page)
        try:
            workflow_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_result_paginator = paginator.page(paginator.num_pages)
        workflow_result_object_list = workflow_result_paginator.object_list
        workflow_result_list = [workflow_result_object.get_dict() for workflow_result_object in workflow_result_object_list]
        return dict(workflow_list=workflow_result_list, page=page, per_page=per_page, total=paginator.count)


account_application_service_ins = AccountApplicationService()