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

    @staticmethod
    @auto_log
    def get_workflows(query_value='', per_page=10, page=1):
        """
        获取获取工作流程
        :param query_value: 查询条件
        :param per_page:
        :param page:
        :return:
        """
        if query_value:
            query_params = Q(name__contains=query_value) | Q(description__contains=query_value) & Q(is_deleted=False)
        else:
            query_params = Q(is_deleted=0)

        workflow_objects = Workflow.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_objects, per_page)
        try:
            workflow_result = paginator.page(page)
        except PageNotAnInteger:
            workflow_result = paginator.page(1)
        except EmptyPage:
            workflow_result = paginator.page(paginator.num_pages)
        return workflow_result, dict(per_page=per_page, page=page, total=paginator.count)

    @staticmethod
    @auto_log
    def get_workflow_by_id(workflow_id):
        """
        通过id获取工作流
        :param workflow_id:
        :return:
        """
        workflow_object = Workflow.objects.filter(id=workflow_id, is_deleted=False).first()
        return workflow_object, ''

    @staticmethod
    @auto_log
    def del_workflow_by_id(workflow_id):
        """
        删除工作流
        :param workflow_id:
        :return:
        """
        Workflow.objects.filter(id=workflow_id).update(is_deleted=True)
        return True, ''

