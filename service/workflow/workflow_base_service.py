from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Workflow

from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowBaseService(BaseService):
    """
    流程服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_workflow_list(cls, name, page, per_page):
        """
        获取工作流列表
        :param name:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False)
        if name:
            query_params &= Q(name__contains=name)
        workflow_querset = Workflow.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_querset, per_page)
        try:
            workflow_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_result_paginator = paginator.page(paginator.num_pages)
        workflow_result_object_list = workflow_result_paginator.object_list
        workflow_result_restful_list = []
        for workflow_result_object in workflow_result_object_list:
            workflow_result_restful_list.append(dict(id=workflow_result_object.id, name=workflow_result_object.name, description=workflow_result_object.description,
                                                     creator=workflow_result_object.creator, gmt_created=str(workflow_result_object.gmt_created)[:19]))
        return workflow_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def check_new_permission(cls, username, workflow_id):
        """
        判断用户是否有新建工单的权限
        :param username:
        :param workflow_id:
        :return:
        """
        return True, ''

    @classmethod
    @auto_log
    def get_by_id(cls, workflow_id):
        """
        获取工作流 by id
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(is_deleted=0, id=workflow_id).first()
        if not workflow_obj:
            return False, '工作流不存在'
        return workflow_obj, ''
