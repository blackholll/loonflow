from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.manage.models import Notice
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins


class NoticeService(BaseService):

    @classmethod
    def get_notice_list(cls, tenant_id, search_value, page, per_page, simple=False):
        """"
        pass
        """
        query_params = Q(tenant_id=tenant_id)
        if search_value:
            query_params &= Q(name__contains=search_value)
        notice_queryset = Notice.objects.filter(query_params)
        paginator = Paginator(notice_queryset, per_page)
        try:
            notice_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            notice_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            notice_result_paginator = paginator.page(paginator.num_pages)
        notice_result_object_list = notice_result_paginator.object_list
        notice_result_format_list = []
        for notice_result_object in notice_result_object_list:
            result = notice_result_object.get_dict()
            if simple:
                need_delete_field_list = ["created_at", "updated_at", "type", "extra", "creator_info"]
                for need_delete_field in need_delete_field_list:
                    result.pop(need_delete_field)
            notice_result_format_list.append(result)

        return dict(notice_list=notice_result_format_list, page=page, per_page=per_page, total=paginator.count)

    @classmethod
    def add_notice(cls, tenant_id: int, operator_id: int, name: str, description: str, type: str, extra: dict) -> int:
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
        notice_obj = Notice(tenant_id=tenant_id, name=name, description=description, type=type, extra=extra, creator_id=operator_id)
        notice_obj.save()
        return notice_obj.id

    @classmethod
    def get_notice_detail(cls, notice_id: int) -> dict:
        """
        get notice detail
        :param notice_id:
        :return:
        """
        try:
            notice_obj = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist as e:
            return CustomCommonException("notice is not exist or has been deleted")
        except Exception:
            raise
        return notice_obj.get_dict()

    @classmethod
    def update_notice(cls, notice_id: int, name: str, description: str, type: str, extra: dict):
        """
        update notice
        :param notice_id:
        :param operator_id:
        :param name:
        :param description:
        :param type:
        :param extra:
        :return:
        """
        notice_queryset = Notice.objects.filter(id=notice_id)
        if not notice_queryset:
            raise CustomCommonException("notice is not exist or has been deleted")
        notice_queryset.update(name=name, description=description, type=type, extra=extra)
        return True

    @classmethod
    def delete_notice(cls, operator_id: int, notice_id:int):
        """
        delete notice
        :param operator_id:
        :param notice_id:
        :return:
        """
        try:
            notice_obj = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist as e:
            raise CustomCommonException("notice is not exist or has been deleted")
        archive_service_ins.archive_record("Notice", notice_obj, operator_id)
        return True


notice_service_ins = NoticeService()
