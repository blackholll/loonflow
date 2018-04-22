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
    def checkout_new_permission(cls, username, workflow_id):
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


