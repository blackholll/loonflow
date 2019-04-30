import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import CustomNotice
from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowCustomNoticeService(BaseService):
    """
    工作流通知服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_notice_list(cls, query_value, page, per_page):
        """
        获取通知列表
        :param query_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value) | Q(description__contains=query_value)

        custom_notice_querset = CustomNotice.objects.filter(query_params).order_by('id')
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
            custom_notice_result_restful_list.append(dict(id=custom_notice_result_object.id, name=custom_notice_result_object.name,
                                                          description=custom_notice_result_object.description,
                                                          creator=custom_notice_result_object.creator,
                                                          script=custom_notice_result_object.script.name,
                                                          title_template=custom_notice_result_object.title_template,
                                                          content_template=custom_notice_result_object.content_template,
                                                          gmt_created=str(custom_notice_result_object.gmt_created)[:19]))
        return custom_notice_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def add_custom_notice(cls, name, script, description, title_template, content_template , creator):
        """
        新增通知脚本
        :param name:
        :param script:
        :param description:
        :param title_template:
        :param content_template:
        :param creator:
        :return:
        """
        script_obj = CustomNotice(name=name, script=script, description=description, title_template=title_template, content_template=content_template , creator=creator)
        script_obj.save()
        return True, script_obj.id

    @classmethod
    @auto_log
    def edit_custom_notice(cls, id, name, script, description, title_template, content_template):
        """
        编辑通知脚本
        :param name:
        :param saved_name:
        :param description:
        :param title_template:
        :param content_template:
        :return:
        """
        custom_notice_obj = CustomNotice.objects.filter(id=id, is_deleted=0)
        if script:
            custom_notice_obj.update(name=name, script=script, description=description, title_template=title_template, content_template=content_template)
        else:
            custom_notice_obj.update(name=name, script=script, description=description, title_template=title_template, content_template=content_template)
        return True, custom_notice_obj.first().id

    @classmethod
    @auto_log
    def del_custom_notice(cls, id):
        """
        删除脚本
        :id: 
        :return:
        """
        custom_notice_obj = CustomNotice.objects.filter(id=id, is_deleted=0)
        if custom_notice_obj:
            custom_notice_obj.update(is_deleted=True)
            return True, ''
        else:
            return False, 'the record is not exist or has been deleted'
