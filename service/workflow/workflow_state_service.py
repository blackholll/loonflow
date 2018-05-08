import json

from django.db.models import QuerySet

from apps.workflow.models import State
from service.base_service import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.workflow.workflow_transition_service import WorkflowTransitionService


class WorkflowStateService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_workflow_states(workflow_id):
        """
        获取流程的状态列表，每个流程的state不会很多，所以不分页
        :param self:
        :param workflow_id:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        else:
            workflow_states = State.objects.filter(workflow_id=workflow_id, is_deleted=False).order_by('order_id')
            return workflow_states, ''

    @staticmethod
    @auto_log
    def get_workflow_state_by_id(state_id):
        """
        获取state详情
        :param self:
        :param state_id:
        :return:
        """
        if not state_id:
            return False, 'except state_id but not provided'
        else:
            workflow_state = State.objects.filter(id=state_id, is_deleted=False).first()
            if not workflow_state:
                return False, '工单状态不存在或已被删除'
            return workflow_state, ''

    @classmethod
    @auto_log
    def get_restful_state_info_by_id(cls, state_id):
        if not state_id:
            return False, 'except state_id but not provided'
        else:
            workflow_state = State.objects.filter(id=state_id, is_deleted=False).first()
            if not workflow_state:
                return False, '工单状态不存在或已被删除'
            state_info_dict = dict(id=workflow_state.id, name=workflow_state.name, workflow_id=workflow_state.workflow_id,
                                   sub_workflow_id=workflow_state.sub_workflow_id, distribute_type_id=workflow_state.distribute_type_id,
                                   is_hidden=workflow_state.is_hidden, order_id=workflow_state.order_id, type_id=workflow_state.type_id,
                                   participant_type_id=workflow_state.participant_type_id, participant=workflow_state.participant,
                                   state_field=json.loads(workflow_state.state_field_str), label=json.loads(workflow_state.label),
                                   creator=workflow_state.creator, gmt_created=str(workflow_state.gmt_created)[:19]
                                   )
            return state_info_dict, ''


    @classmethod
    @auto_log
    def get_workflow_start_state(cls, workflow_id):
        """
        获取工作流初始状态
        :param workflow_id:
        :return:
        """
        workflow_state_queryset = State.objects.filter(is_deleted=0, workflow_id=workflow_id).all()
        for workflow_state in workflow_state_queryset:
            if workflow_state.type_id == CONSTANT_SERVICE.STATE_TYPE_START:
                return workflow_state, ''
        return False, '该工作流未配置初始状态，请检查工作流配置'

    @classmethod
    @auto_log
    def get_states_info_by_state_id_list(cls, state_id_list):
        state_queryset = State.objects.filter(is_deleted=0, id__in=state_id_list).all()
        state_info_dict = {}
        for state in state_queryset:
            state_info_dict[state.id] = state.name
        return state_info_dict, ''

    @classmethod
    @auto_log
    def get_workflow_init_state(cls, workflow_id):
        """
        获取工作的初始状态信息，包括允许的transition
        :param workflow_id:
        :return:
        """
        init_state_obj = State.objects.filter(workflow_id=workflow_id, is_deleted=False, type_id=CONSTANT_SERVICE.STATE_TYPE_START).first()
        if not init_state_obj:
            return False, '该工作流尚未配置初始状态'

        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(init_state_obj.id)
        transition_info_list = []
        for transition in transition_queryset:
            transition_info_list.append(dict(transition_id=transition.id, transition_name=transition.name))
        state_info_dict = dict(id=init_state_obj.id, name=init_state_obj.name, workflow_id=init_state_obj.workflow_id,
                               sub_workflow_id=init_state_obj.sub_workflow_id, distribute_type_id=init_state_obj.distribute_type_id,
                               is_hidden=init_state_obj.is_hidden, order_id=init_state_obj.order_id, type_id=init_state_obj.type_id,
                               participant_type_id=init_state_obj.participant_type_id, participant=init_state_obj.participant,
                               state_field=json.loads(init_state_obj.state_field_str), label=json.loads(init_state_obj.label),
                               creator=init_state_obj.creator, gmt_created=str(init_state_obj.gmt_created)[:19],
                               transition=transition_info_list
                               )
        return state_info_dict, ''
