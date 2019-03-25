from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

    @classmethod
    @auto_log
    def get_transition_by_args(cls, arg_dict):
        """
        获取流转
        :param arg_dict: 条件字典
        :return:
        """
        arg_dict.update(is_deleted=0)
        return Transition.objects.filter(**arg_dict).all(), ''

    @classmethod
    @auto_log
    def get_transitions_serialize_by_workflow_id(cls, workflow_id, per_page=10, page=1):
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        workflow_transitions = Transition.objects.filter(workflow_id=workflow_id, is_deleted=False)

        paginator = Paginator(workflow_transitions, per_page)

        try:
            workflow_transitions_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_transitions_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_transitions_result_paginator = paginator.page(paginator.num_pages)
        workflow_transitions_object_list = workflow_transitions_result_paginator.object_list
        workflow_transitions_restful_list = []
        for workflow_transitions_object in workflow_transitions_object_list:
            result_dict = dict(id=workflow_transitions_object.id, name=workflow_transitions_object.name,
                               creator=workflow_transitions_object.creator,
                               source_state_id=workflow_transitions_object.source_state_id,
                               destination_state_id=workflow_transitions_object.destination_state_id,
                               gmt_created=str(workflow_transitions_object.gmt_created)[:19])
            workflow_transitions_restful_list.append(result_dict)
        return workflow_transitions_restful_list, dict(per_page=per_page, page=page, total=paginator.count)
