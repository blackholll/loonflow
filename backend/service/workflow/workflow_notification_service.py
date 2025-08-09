import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Notification as WorkflowNotification
from service.base_service import BaseService
from service.common.constant_service import constant_service_ins
from service.common.log_service import auto_log


class WorkflowNotificationService(BaseService):

    @classmethod
    def add_workflow_notification(cls, operator_id: str, tenant_id: str, workflow_id:str, version_id:str, notification_info:dict) -> int:
        """
        add workflow notification
        :param operator_id:
        :param tenant_id:
        :param workflow_id:
        :param notification_info:
        :return:
        """
        selected_channel_list = notification_info.get("selected_channel_list")
        workflow_notice_info = WorkflowNotification(workflow_id=workflow_id, creator_id=operator_id, tenant_id=tenant_id, version_id=version_id,
                                              title_template=notification_info.get("title_template"), content_template=
                                              notification_info.get("content_template"), channels=','.join(selected_channel_list))
        workflow_notice_info.save()
        return workflow_notice_info.id

    @classmethod
    def get_workflow_fd_notification(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow full definition notification
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        notification_queryset = WorkflowNotification.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).first()
        if notification_queryset:
            notification_result = dict(
                title_template=notification_queryset.title_template,
                content_template=notification_queryset.content_template,
                selected_channel_list=notification_queryset.channels.split(','),
            )
        else:
            notification_result = {}
        return notification_result
            

    @classmethod
    def get_notification_list(cls, query_value: str, page: int, per_page: int, simple: bool=False)->tuple:
        """
        获取通知列表
        :param query_value:
        :param page:
        :param per_page:
        :param simple: 简单数据
        :return:
        """
        query_params = Q(is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value) | Q(description__contains=query_value)

        custom_notice_querset = WorkflowNotification.objects.filter(query_params).order_by('id')
        paginator = Paginator(custom_notice_querset, per_page)
        try:
            custom_notice_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            custom_notice_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            custom_notice_result_paginator = paginator.page(paginator.num_pages)
        custom_notice_result_object_list = custom_notice_result_paginator.object_list
        custom_notice_result_restful_list = []
        for custom_notice_result_object in custom_notice_result_object_list:
            per_notice_data = custom_notice_result_object.get_dict()
            if simple:
                per_notice_data.pop("corpid")
                per_notice_data.pop("corpsecret")
                per_notice_data.pop("appkey")
                per_notice_data.pop("appsecret")
                per_notice_data.pop("hook_url")
                per_notice_data.pop("hook_token")
            custom_notice_result_restful_list.append(per_notice_data)
        return custom_notice_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)



    @classmethod
    def update_workflow_notification(cls, tenant_id: str, workflow_id: str, version_id: str, notification_info: dict):
        """
        update workflow notification
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param notification_info:
        :return:
        """
        WorkflowNotification.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id).update(title_template=notification_info.get("title_template"), content_template=notification_info.get("content_template"), channels=','.join(notification_info.get("selected_channel_list")))


workflow_notification_service_ins = WorkflowNotificationService()
