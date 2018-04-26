from apps.workflow.models import State, Transition
from service.base_service import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log


class WorkflowTransitionService(BaseService):
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_state_transition_queryset(cls, state_id):
        """
        获取状态可以执行的操作
        :param state_id:
        :return:
        """
        return Transition.objects.filter(is_deleted=0, source_state_id=state_id).all(), ''

    @classmethod
    @auto_log
    def get_workflow_transition_by_id(cls, transition_id):
        """
        获取transiton
        :param transition_id:
        :return:
        """
        return Transition.objects.filter(is_deleted=0, id=transition_id).first(), ''