from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.manage.models import Notification
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins
from service.util.encrypt_service import encrypt_service_ins


class NotificationService(BaseService):

    @classmethod
    def get_notification_list(cls, tenant_id, search_value, page, per_page, simple=False):
        """"
        pass
        """
        query_params = Q(tenant_id=tenant_id)
        if search_value:
            query_params &= Q(name__contains=search_value)
        notification_queryset = Notification.objects.filter(query_params).order_by('-created_at')
        paginator = Paginator(notification_queryset, per_page)
        try:
            notification_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            notification_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            notification_result_paginator = paginator.page(paginator.num_pages)
        notification_result_object_list = notification_result_paginator.object_list
        notification_result_format_list = []
        for notification_result_object in notification_result_object_list:
            result = notification_result_object.get_dict()
            if simple:
                need_delete_field_list = ["created_at", "updated_at", "type", "extra", "creator_info"]
                for need_delete_field in need_delete_field_list:
                    result.pop(need_delete_field)
            notification_result_format_list.append(result)

        return dict(notification_list=notification_result_format_list, page=page, per_page=per_page, total=paginator.count)

    @classmethod
    def add_notification(cls, tenant_id: int, operator_id: int, name: str, description: str, type: str, extra: dict) -> str:
        """
        add notice
        :param tenant_id:
        :param operator_id:
        :param name:
        :param description:
        :param type:
        :param extra:
        :return:
        """
        encrypt_field = {
            "hook": "hook_token",
            "dingtalk": "dt_app_secret",
            "wecom": "wc_corp_secret",
            "feishu": "fs_app_secret"
        }
        extra[encrypt_field[type]] = encrypt_service_ins.encrypt(extra[encrypt_field[type]])
        notice_obj = Notification(tenant_id=tenant_id, name=name, description=description, type=type, extra=extra, creator_id=operator_id)
        notice_obj.save()
        return str(notice_obj.id)

    @classmethod
    def get_notification_detail(cls, tenant_id:str, notification_id: str) -> dict:
        """
        get notice detail
        :param notification_id:
        :return:
        """
        try:
            notification_obj = Notification.objects.get(id=notification_id, tenant_id=tenant_id)
        except Notification.DoesNotExist as e:
            return CustomCommonException("notification is not exist or has been deleted")
        except Exception:
            raise
        result = notification_obj.get_dict()
        # todo: decrypt
        if result.get("type") == "hook":
            result["extra"]["hook_token"] = encrypt_service_ins.decrypt(result["extra"]["hook_token"])
        elif result.get("type") == "dingtalk":
            result["extra"]["dt_app_secret"] = encrypt_service_ins.decrypt(result["extra"]["dt_app_secret"])
        elif result.get("type") == "wecom":
            result["extra"]["wc_corp_secret"] = encrypt_service_ins.decrypt(result["extra"]["wc_corp_secret"])
        elif result.get("type") == "feishu":
            result["extra"]["fs_app_secret"] = encrypt_service_ins.decrypt(result["extra"]["fs_app_secret"])
        return result

    @classmethod
    def update_notification(cls, tenant_id:str, notification_id: int, name: str, description: str, type: str, extra: dict):
        """
        update notice
        :param tenant_id:
        :param notification_id:
        :param operator_id:
        :param name:
        :param description:
        :param type:
        :param extra:
        :return:
        """
        encrypt_field = {
            "hook": "hook_token",
            "dingtalk": "dt_app_secret",
            "wecom": "wc_corp_secret",
            "feishu": "fs_app_secret"
        }
        extra[encrypt_field[type]] = encrypt_service_ins.encrypt(extra[encrypt_field[type]])

        notice_queryset = Notification.objects.filter(id=notification_id, tenant_id=tenant_id)
        if not notice_queryset:
            raise CustomCommonException("notice is not exist or has been deleted")
        notice_queryset.update(name=name, description=description, type=type, extra=extra)
        return True

    @classmethod
    def delete_notification(cls, tenant_id:str, operator_id: str, notification_id:str):
        """
        delete notice
        :param tenant_id:
        :param operator_id:
        :param notification_id:
        :return:
        """
        try:
            notification_obj = Notification.objects.get(id=notification_id, tenant_id=tenant_id)
        except Notification.DoesNotExist as e:
            raise CustomCommonException("notice is not exist or has been deleted")
        archive_service_ins.archive_record("Notice", notification_obj, operator_id)
        return True


notification_service_ins = NotificationService()
