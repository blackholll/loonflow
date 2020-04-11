from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from apps.workflow.models import Transition
from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowTransitionService(BaseService):
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_state_transition_queryset(cls, state_id: int)->tuple:
        """
        获取状态可以执行的操作
        get state can do transitions queryset
        :param state_id:
        :return:
        """
        return True, Transition.objects.filter(is_deleted=0, source_state_id=state_id).all()

    @classmethod
    @auto_log
    def get_workflow_transition_by_id(cls, transition_id: int)->tuple:
        """
        获取transition
        get transition by id
        :param transition_id:
        :return:
        """
        return True, Transition.objects.filter(is_deleted=0, id=transition_id).first()

    @classmethod
    @auto_log
    def get_transition_by_args(cls, arg_dict: dict)->tuple:
        """
        获取流转
        get transtion list by params
        :param arg_dict: 条件字典
        :return:
        """
        arg_dict.update(is_deleted=0)
        return True, Transition.objects.filter(**arg_dict).all()

    @classmethod
    @auto_log
    def get_transitions_serialize_by_workflow_id(cls, workflow_id: int, per_page: int=10, page: int=1,
                                                 query_value: str='')->tuple:
        """
        根据workflow id获取工作流的流转记录
        get transition serialize record by workflow and params
        :param workflow_id:
        :param per_page:
        :param page:
        :param query_value:
        :return:
        """
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
            from service.workflow.workflow_state_service import workflow_state_service_ins
            flag1, source_state_obj = workflow_state_service_ins.get_workflow_state_by_id(
                workflow_transitions_object.source_state_id)
            flag2, destination_state_obj = workflow_state_service_ins.get_workflow_state_by_id(
                workflow_transitions_object.destination_state_id)
            if flag1 and source_state_obj:
                source_state_info['name'] = source_state_obj.name
                source_state_info['id'] = source_state_obj.id
            else:
                source_state_info['name'] = '未知'
                source_state_info['id'] = workflow_transitions_object.source_state_id

            if flag2 and destination_state_obj:
                destination_state_info['name'] = destination_state_obj.name
                destination_state_info['id'] = destination_state_obj.id
            else:
                if workflow_transitions_object.condition_expression != '[]':
                    destination_state_info['name'] = '见条件表达式'
                else:
                    destination_state_info['name'] = '请指定目标状态或设置条件表达式'
                destination_state_info['id'] = workflow_transitions_object.destination_state_id

            result_dict = workflow_transitions_object.get_dict()
            result_dict['source_state_info'] = source_state_info
            result_dict['destination_state_info'] = destination_state_info

            workflow_transitions_restful_list.append(result_dict)
        return True, dict(workflow_transitions_restful_list=workflow_transitions_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_workflow_transition(cls, workflow_id: int, name: str, transition_type_id: int, timer: int,
                                source_state_id: int, destination_state_id: int, condition_expression: str,
                                attribute_type_id: int, field_require_check: int, alert_enable: int, alert_text: str,
                                creator: str)->tuple:
        transition_obj = Transition(workflow_id=workflow_id, name=name, transition_type_id=transition_type_id,
                                    timer=timer, source_state_id=source_state_id,
                                    destination_state_id=destination_state_id,
                                    condition_expression=condition_expression,
                                    attribute_type_id=attribute_type_id, field_require_check=field_require_check,
                                    alert_enable=alert_enable, alert_text=alert_text, creator=creator)
        transition_obj.save()
        return True, dict(transition_id=transition_obj.id)

    @classmethod
    @auto_log
    def edit_workflow_transition(cls, transition_id: int, workflow_id: int, name, transition_type_id: int, timer: int,
                                 source_state_id: int, destination_state_id: int, condition_expression: str,
                                 attribute_type_id: int, field_require_check: int, alert_enable: int,
                                 alert_text: str)->tuple:
        transition_queryset = Transition.objects.filter(is_deleted=0, id=transition_id)
        if transition_queryset:
            transition_queryset.update(workflow_id=workflow_id, name=name, transition_type_id=transition_type_id,
                                       timer=timer, source_state_id=source_state_id,
                                       destination_state_id=destination_state_id,
                                       condition_expression=condition_expression,
                                       attribute_type_id=attribute_type_id, field_require_check=field_require_check,
                                       alert_enable=alert_enable, alert_text=alert_text)
        return True, ''

    @classmethod
    @auto_log
    def del_workflow_transition(cls, transition_id: int)->tuple:
        transition_queryset = Transition.objects.filter(is_deleted=0, id=transition_id)
        if transition_queryset:
            transition_queryset.update(is_deleted=1)
        return True, ''


workflow_transition_service_ins = WorkflowTransitionService()

