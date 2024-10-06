import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.manage.models import Notice
from apps.workflow.models import WorkflowNotice
from service.base_service import BaseService
from service.common.constant_service import constant_service_ins
from service.common.log_service import auto_log


class WorkflowNoticeService(BaseService):

    @classmethod
    def add_workflow_notice(cls, operator_id: int, tenant_id: int, workflow_id:int, notice_info:dict) -> int:
        """
        add workflow notice
        :param operator_id:
        :param tenant_id:
        :param workflow_id:
        :param notice_info:
        :return:
        """
        notice_id_list = notice_info.get("notice_id_list")
        notice_id_str_list = [str(notice_id) for notice_id in notice_id_list]
        notices = ",".join(notice_id_str_list)
        workflow_notice_info = WorkflowNotice(workflow_id=workflow_id, creator_id=operator_id, tenant_id=tenant_id,
                                              title_template=notice_info.get("title_template"), content_template=
                                              notice_info.get("content_template"), notices=notices)
        workflow_notice_info.save()
        return workflow_notice_info.id

    @classmethod
    @auto_log
    def get_notice_list(cls, query_value: str, page: int, per_page: int, simple: bool=False)->tuple:
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

        custom_notice_querset = Notice.objects.filter(query_params).order_by('id')
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
    @auto_log
    def add_custom_notice(cls, name: str, description: str, type_id: int, corpid: str, corpsecret: str, appkey: str,
                          appsecret: str, hook_url: str, hook_token: str, creator: str)->tuple:
        """
        新增自定义通知记录
        :param name:
        :param description:
        :param type_id:
        :param corpid:
        :param corpsecret:
        :param appkey:
        :param appsecret:
        :param hook_url:
        :param hook_token:
        :param creator:
        :return:
        """
        notice_obj = Notice(name=name, description=description, type_id=type_id, corpid=corpid,
                                  corpsecret=corpsecret, appkey=appkey, appsecret=appsecret, hook_url=hook_url,
                                  hook_token=hook_token, creator=creator)
        notice_obj.save()
        return True, dict(notice_id=notice_obj.id)

    @classmethod
    @auto_log
    def update_custom_notice(cls, custom_notice_id: int, name: str, description: str, type_id: int,
                             corpid: str, corpsecret: str, appkey: str, appsecret: str, hook_url: str,
                             hook_token: str)->tuple:
        """
        更新自定义通知
        :param custom_notice_id:
        :param name:
        :param description:
        :param hook_url:
        :param hook_token:
        :return:
        """
        custom_notice_obj = Notice.objects.filter(id=custom_notice_id)
        if custom_notice_obj:
            custom_notice_obj.update(name=name, description=description, hook_url=hook_url, hook_token=hook_token,
                                     type_id=type_id, corpid=corpid, corpsecret=corpsecret, appkey=appkey,
                                     appsecret=appsecret)
        else:
            return False, 'the record is not existed or has been deleted'
        return True, ''

    @classmethod
    @auto_log
    def del_custom_notice(cls, custom_notice_id: int)->tuple:
        """
        删除脚本
        :id: 
        :return:
        """
        custom_notice_obj = Notice.objects.filter(id=custom_notice_id)
        if custom_notice_obj:
            custom_notice_obj.update(is_deleted=True)
            return True, ''
        else:
            return False, 'the record is not exist or has been deleted'

    @classmethod
    @auto_log
    def get_notice_detail(cls, custom_notice_id: int)->tuple:
        """
        获取通知详情
        :param custom_notice_id:
        :return:
        """
        custom_notice_obj = Notice.objects.filter(id=custom_notice_id).first()
        if custom_notice_obj:
            custom_notice_info = custom_notice_obj.get_dict()
            return True, custom_notice_info
        else:
            return False, 'record is not exist or has been deleted'


workflow_notice_service_ins = WorkflowNoticeService()
