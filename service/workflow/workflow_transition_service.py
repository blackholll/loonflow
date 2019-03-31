from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

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
    def get_transitions_serialize_by_workflow_id(cls, workflow_id, per_page=10, page=1, query_value=''):
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        query_params = Q(workflow_id=workflow_id, is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value)

        workflow_transitions = Transition.objects.filter(query_params)

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
            source_state_info = {}
            destination_state_info = {}
            from service.workflow.workflow_state_service import WorkflowStateService
            source_state_obj, msg = WorkflowStateService.get_workflow_state_by_id(workflow_transitions_object.source_state_id)
            destination_state_obj, msg = WorkflowStateService.get_workflow_state_by_id(workflow_transitions_object.destination_state_id)
            if source_state_obj:
                source_state_info['name'] = source_state_obj.name
                source_state_info['id'] = source_state_obj.id

            if destination_state_obj:
                destination_state_info['name'] = destination_state_obj.name
                destination_state_info['id'] = destination_state_obj.id
            result_dict = dict(id=workflow_transitions_object.id, name=workflow_transitions_object.name,
                               creator=workflow_transitions_object.creator,
                               source_state_id=workflow_transitions_object.source_state_id,
                               source_state_info=source_state_info,
                               destination_state_info=destination_state_info,
                               destination_state_id=workflow_transitions_object.destination_state_id,
                               transition_type_id=workflow_transitions_object.transition_type_id,
                               timer=workflow_transitions_object.timer,
                               condition_expression=workflow_transitions_object.condition_expression,
                               attribute_type_id=workflow_transitions_object.attribute_type_id,
                               field_require_check=workflow_transitions_object.field_require_check,
                               alert_enable=workflow_transitions_object.alert_enable,
                               alert_text=workflow_transitions_object.alert_text,
                               gmt_created=str(workflow_transitions_object.gmt_created)[:19])
            workflow_transitions_restful_list.append(result_dict)
        return workflow_transitions_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def add_workflow_transition(cls, workflow_id, name, transition_type_id, timer, source_state_id,
                                               destination_state_id, condition_expression, attribute_type_id,
                                               field_require_check, alert_enable, alert_text, creator):
        transition_obj = Transition(workflow_id=workflow_id, name=name, transition_type_id=transition_type_id,
                                    timer=timer, source_state_id=source_state_id,
                                    destination_state_id=destination_state_id, condition_expression=condition_expression,
                                    attribute_type_id=attribute_type_id, field_require_check=field_require_check,
                                    alert_enable=alert_enable, alert_text=alert_text, creator=creator)
        transition_obj.save()
        return transition_obj.id, ''

    @classmethod
    @auto_log
    def edit_workflow_transition(cls, transition_id, workflow_id, name, transition_type_id, timer, source_state_id,
                                 destination_state_id, condition_expression, attribute_type_id,
                                 field_require_check, alert_enable, alert_text):
        transition_queryset = Transition.objects.filter(is_deleted=0, id=transition_id)
        if transition_queryset:
            transition_queryset.update(workflow_id=workflow_id, name=name, transition_type_id=transition_type_id,
                                       timer=timer, source_state_id=source_state_id,
                                       destination_state_id=destination_state_id, condition_expression=condition_expression,
                                       attribute_type_id=attribute_type_id, field_require_check=field_require_check,
                                       alert_enable=alert_enable, alert_text=alert_text)
        return transition_id, ''

    @classmethod
    @auto_log
    def del_workflow_transition(cls, transition_id):
        transition_queryset = Transition.objects.filter(is_deleted=0, id=transition_id)
        if transition_queryset:
            transition_queryset.update(is_deleted=1)
        return transition_id, ''
