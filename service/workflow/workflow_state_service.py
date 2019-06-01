# import json
import json

from django.db.models import QuerySet, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.ticket.models import TicketCustomField
from apps.workflow.models import State
from service.account.account_base_service import AccountBaseService
from service.base_service import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.workflow.workflow_custom_field_service import WorkflowCustomFieldService
from service.workflow.workflow_runscript_service import WorkflowRunScriptService
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
    def get_workflow_states_serialize(workflow_id, per_page=10, page=1, query_value=''):
        """
        获取序列化工作流状态记录
        :param workflow_id:
        :param per_page:
        :param page:
        :param search_value:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        query_params = Q(workflow_id=workflow_id, is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value)

        workflow_states = State.objects.filter(query_params).order_by('order_id')

        paginator = Paginator(workflow_states, per_page)

        try:
            workflow_states_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_states_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_states_result_paginator = paginator.page(paginator.num_pages)
        workflow_states_object_list = workflow_states_result_paginator.object_list
        workflow_states_restful_list = []
        for workflow_states_object in workflow_states_object_list:
            participant_info, msg = WorkflowStateService.get_format_participant_info(workflow_states_object.participant_type_id, workflow_states_object.participant)
            result_dict = dict(id=workflow_states_object.id, name=workflow_states_object.name, workflow_id=workflow_states_object.workflow_id,
                               sub_workflow_id=workflow_states_object.sub_workflow_id, is_hidden=workflow_states_object.is_hidden,
                               order_id=workflow_states_object.order_id, type_id=workflow_states_object.type_id,
                               participant_type_id=workflow_states_object.participant_type_id, participant=workflow_states_object.participant,
                               distribute_type_id=workflow_states_object.distribute_type_id,
                               state_field_str=json.loads(workflow_states_object.state_field_str), label=json.loads(workflow_states_object.label),
                               creator=workflow_states_object.creator, participant_info=participant_info,
                               remember_last_man_enable=1 if workflow_states_object.remember_last_man_enable else 0,
                               gmt_created=str(workflow_states_object.gmt_created)[:19])
            workflow_states_restful_list.append(result_dict)
        return workflow_states_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

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
        workflow_state_obj = State.objects.filter(
            is_deleted=0, workflow_id=workflow_id, type_id=CONSTANT_SERVICE.STATE_TYPE_START).first()
        if workflow_state_obj:
            return workflow_state_obj, ''
        else:
            return None, '该工作流未配置初始状态，请检查工作流配置'

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

        # 工单基础字段及属性
        field_list = []
        field_list.append(dict(field_key='title', field_name=u'标题', field_value=None, order_id=20,
                               field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                               field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的标题',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(workflow_id)
        for key, value in custom_field_dict.items():
            field_list.append(dict(field_key=key, field_name=custom_field_dict[key]['field_name'], field_value=None, order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO,
                                   default_value=custom_field_dict[key]['default_value'],
                                   description=custom_field_dict[key]['description'],
                                   field_template=custom_field_dict[key]['field_template'],
                                   boolean_field_display=json.loads(custom_field_dict[key]['boolean_field_display']) if custom_field_dict[key]['boolean_field_display'] else {},  # 之前model允许为空了，为了兼容先这么写,
                                   field_choice=json.loads(custom_field_dict[key]['field_choice']),
                                   label=json.loads(custom_field_dict[key]['label'])
                                   ))

        state_field_dict = json.loads(init_state_obj.state_field_str)
        state_field_key_list = state_field_dict.keys()

        new_field_list = []
        for field0 in field_list:
            if field0['field_key'] in state_field_key_list:
                field0['field_attribute'] = state_field_dict[field0['field_key']]
                new_field_list.append(field0)

        # 字段排序
        new_field_list = sorted(new_field_list, key=lambda r: r['order_id'])
        state_info_dict = dict(id=init_state_obj.id, name=init_state_obj.name, workflow_id=init_state_obj.workflow_id,
                               sub_workflow_id=init_state_obj.sub_workflow_id, distribute_type_id=init_state_obj.distribute_type_id,
                               is_hidden=init_state_obj.is_hidden, order_id=init_state_obj.order_id, type_id=init_state_obj.type_id,
                               participant_type_id=init_state_obj.participant_type_id, participant=init_state_obj.participant,
                               field_list=new_field_list, label=json.loads(init_state_obj.label),
                               creator=init_state_obj.creator, gmt_created=str(init_state_obj.gmt_created)[:19],
                               transition=transition_info_list
                               )
        return state_info_dict, ''

    @classmethod
    @auto_log
    def get_format_participant_info(cls, participant_type_id, participant):
        """
        获取格式化的参与人信息
        :param participant_type_id:
        :param participant:
        :return:
        """
        participant_name = participant
        participant_type_name = ''
        participant_alias = ''
        if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            participant_type_name = '个人'
            participant_user_obj, msg = AccountBaseService.get_user_by_username(participant)
            if not participant_user_obj:
                participant_alias = participant
            else:
                participant_alias = participant_user_obj.alias
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
            participant_type_name = '多人'
            # 依次获取人员信息
            participant_name_list = participant_name.split(',')
            participant_alias_list = []
            for participant_name0 in participant_name_list:
                participant_user_obj, msg = AccountBaseService.get_user_by_username(participant_name0)
                if not participant_user_obj:
                    participant_alias_list.append(participant_name0)
                else:
                    participant_alias_list.append(participant_user_obj.alias)
            participant_alias = ','.join(participant_alias_list)
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            participant_type_name = '部门'
            dept_obj, msg = AccountBaseService.get_dept_by_id(int(participant))
            if not dept_obj:
                return False, 'dept is not existed or has been deleted'
            participant_name = dept_obj.name
            participant_alias = participant_name
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            participant_type_name = '角色'
            role_obj, msg = AccountBaseService.get_role_by_id(int(participant))
            if not role_obj:
                return False, 'role is not existedor has been deleted'
            participant_name = role_obj.name
            participant_alias = participant_name
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            participant_type_name = '变量'
            if participant_name == 'creator':
                participant_alias = '工单创建人'
            elif participant_name == 'creator_tl':
                participant_alias = '工单创建人的tl'
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            if participant:
                flag, result = WorkflowRunScriptService.get_run_script_by_id(int(participant))
                if flag:
                    participant_alias = result.name

        return dict(participant=participant, participant_name=participant_name, participant_type_id=participant_type_id,
                    participant_type_name=participant_type_name, participant_alias=participant_alias), ''

    @classmethod
    @auto_log
    def add_workflow_state(cls, workflow_id, name, sub_workflow_id, is_hidden, order_id, type_id, remember_last_man_enable,
                           participant_type_id, participant, distribute_type_id, state_field_str, label, creator):
        """
        新增工作流状态
        :param workflow_id:
        :param name:
        :param sub_workflow_id:
        :param is_hidden:
        :param order_id:
        :param type_id:
        :param remember_last_man_enable:
        :param participant_type_id:
        :param participant:
        :param distribute_type_id:
        :param state_field_str:
        :param label:
        :param creator:
        :return:
        """
        workflow_state_obj = State(workflow_id=workflow_id, name=name, sub_workflow_id=sub_workflow_id, is_hidden=is_hidden,
                                   order_id=order_id, type_id=type_id, remember_last_man_enable=remember_last_man_enable,
                                   participant_type_id=participant_type_id, participant=participant, distribute_type_id=distribute_type_id,
                                   state_field_str=state_field_str, label=label, creator=creator)
        workflow_state_obj.save()
        return workflow_state_obj.id, ''

    @classmethod
    @auto_log
    def edit_workflow_state(cls, state_id, workflow_id, name, sub_workflow_id, is_hidden, order_id, type_id,
                           remember_last_man_enable,
                           participant_type_id, participant, distribute_type_id, state_field_str, label, creator):
        """
        新增工作流状态
        :param state_id:
        :param workflow_id:
        :param name:
        :param sub_workflow_id:
        :param is_hidden:
        :param order_id:
        :param type_id:
        :param remember_last_man_enable:
        :param participant_type_id:
        :param participant:
        :param distribute_type_id:
        :param state_field_str:
        :param label:
        :param creator:
        :return:
        """
        state_obj = State.objects.filter(id=state_id, is_deleted=0)
        if state_obj:
            state_obj.update(workflow_id=workflow_id, name=name, sub_workflow_id=sub_workflow_id,
                             is_hidden=is_hidden, order_id=order_id, type_id=type_id,
                             remember_last_man_enable=remember_last_man_enable, participant_type_id=participant_type_id,
                             participant=participant, distribute_type_id=distribute_type_id,
                             state_field_str=state_field_str, label=label)
        return state_id, ''

    @classmethod
    @auto_log
    def del_workflow_state(cls, state_id):
        """
        删除状态
        :param state_id:
        :return:
        """
        state_obj = State.objects.filter(id=state_id, is_deleted=0)
        if state_obj:
            state_obj.update(is_deleted=1)
        return state_id, ''
