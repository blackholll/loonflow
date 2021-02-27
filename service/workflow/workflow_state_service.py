import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import State
from service.account.account_base_service import account_base_service_ins
from service.base_service import BaseService
from service.common.constant_service import constant_service_ins
from service.common.log_service import auto_log
from service.workflow.workflow_custom_field_service import workflow_custom_field_service_ins
from service.workflow.workflow_runscript_service import workflow_run_script_service_ins
from service.workflow.workflow_transition_service import workflow_transition_service_ins


class WorkflowStateService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_workflow_states(workflow_id: int)->tuple:
        """
        获取流程的状态列表，每个流程的state不会很多，所以不分页
        get workflow state queryset
        :param workflow_id:
        :return:
        """
        if not workflow_id:
            return False, 'except workflow_id but not provided'
        else:
            workflow_states = State.objects.filter(workflow_id=workflow_id, is_deleted=False).order_by('order_id')
            return True, workflow_states

    @staticmethod
    @auto_log
    def get_workflow_states_serialize(workflow_id: int, per_page: int=10, page: int=1, query_value: str='', simple=False)->tuple:
        """
        获取序列化工作流状态记录
        get restful workflow's state by params
        :param workflow_id:
        :param per_page:
        :param page:
        :param query_value:
        :param simle: 是否只返回简单数据
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
            flag, participant_info = WorkflowStateService.get_format_participant_info(
                workflow_states_object.participant_type_id, workflow_states_object.participant)
            result_dict = workflow_states_object.get_dict()
            result_dict['state_field_str'] = json.loads(result_dict['state_field_str'])
            result_dict['label'] = json.loads(result_dict['label'])
            result_dict['participant_info'] = participant_info
            if simple:
                result_new_dict = dict(id=workflow_states_object.id, name=workflow_states_object.name)
                result_dict = result_new_dict

            workflow_states_restful_list.append(result_dict)
        return True, dict(workflow_states_restful_list=workflow_states_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @staticmethod
    @auto_log
    def get_workflow_state_by_id(state_id: int)->tuple:
        """
        获取state详情
        get state info by id
        :param state_id:
        :return:
        """
        if not state_id:
            return False, 'except state_id but not provided'
        else:
            workflow_state = State.objects.filter(id=state_id, is_deleted=False).first()
            if not workflow_state:
                return False, '工单状态不存在或已被删除'
            return True, workflow_state

    @classmethod
    @auto_log
    def get_restful_state_info_by_id(cls, state_id: int)->tuple:
        if not state_id:
            return False, 'except state_id but not provided'
        else:
            workflow_state = State.objects.filter(id=state_id, is_deleted=False).first()
            if not workflow_state:
                return False, '工单状态不存在或已被删除'
            state_info_dict = dict(
                id=workflow_state.id, name=workflow_state.name, workflow_id=workflow_state.workflow_id,
                distribute_type_id=workflow_state.distribute_type_id,
                is_hidden=workflow_state.is_hidden, order_id=workflow_state.order_id, type_id=workflow_state.type_id,
                participant_type_id=workflow_state.participant_type_id, participant=workflow_state.participant,
                state_field=json.loads(workflow_state.state_field_str), label=json.loads(workflow_state.label),
                creator=workflow_state.creator, gmt_created=str(workflow_state.gmt_created)[:19])
            return True, state_info_dict

    @classmethod
    @auto_log
    def get_workflow_start_state(cls, workflow_id: int)->tuple:
        """
        获取工作流初始状态
        get workflow's init state
        :param workflow_id:
        :return:
        """
        workflow_state_obj = State.objects.filter(
            is_deleted=0, workflow_id=workflow_id, type_id=constant_service_ins.STATE_TYPE_START).first()
        if workflow_state_obj:
            return True, workflow_state_obj
        else:
            return False, 'This workflow have no init state, please check the config'

    @classmethod
    @auto_log
    def get_states_info_by_state_id_list(cls, state_id_list)->tuple:
        state_queryset = State.objects.filter(is_deleted=0, id__in=state_id_list).all()
        state_info_dict = {}
        for state in state_queryset:
            state_dict = state.get_dict()
            state_info_dict[state.id] = state_dict
        return True, state_info_dict

    @classmethod
    @auto_log
    def get_workflow_end_state(cls, workflow_id: int)->tuple:
        """
        获取工作流结束状态
        get workflow's end state
        :param workflow_id:
        :return:
        """
        workflow_state_obj = State.objects.filter(
            is_deleted=0, workflow_id=workflow_id, type_id=constant_service_ins.STATE_TYPE_END).first()
        if workflow_state_obj:
            return True, workflow_state_obj
        else:
            return False, '该工作流未配置结束状态，请检查工作流配置'

    @classmethod
    @auto_log
    def get_workflow_init_state(cls, workflow_id: int)->tuple:
        """
        获取工作流的初始状态信息，包括允许的transition
        get workflow's init state, include allow transition
        :param workflow_id:
        :return:
        """
        init_state_obj = State.objects.filter(workflow_id=workflow_id, is_deleted=False, type_id=constant_service_ins.STATE_TYPE_START).first()
        if not init_state_obj:
            return False, '该工作流尚未配置初始状态'

        flag, transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(init_state_obj.id)
        if flag is False:
            return False, transition_queryset
        transition_info_list = []
        for transition in transition_queryset:
            transition_info_dict = dict(
                transition_id=transition.id, transition_name=transition.name,
                attribute_type_id=transition.attribute_type_id, field_require_check=transition.field_require_check,
                alert_enable=transition.alert_enable, alert_text=transition.alert_text
            )

            transition_info_list.append(transition_info_dict)

        # 工单基础字段及属性
        field_list = []
        field_list.append(dict(
            field_key='title', field_name=u'标题', field_value=None, order_id=20,
            field_type_id=constant_service_ins.FIELD_TYPE_STR, field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,
            description='', field_choice={}, boolean_field_display={}, default_value=None, field_template='',
            placeholder='', label={}))
        flag, custom_field_dict = workflow_custom_field_service_ins.get_workflow_custom_field(workflow_id)
        for key, value in custom_field_dict.items():
            field_list.append(dict(field_key=key, field_name=custom_field_dict[key]['field_name'],
                                   field_value=None, order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,
                                   default_value=custom_field_dict[key]['default_value'],
                                   description=custom_field_dict[key]['description'],
                                   placeholder=custom_field_dict[key]['placeholder'],
                                   field_template=custom_field_dict[key]['field_template'],
                                   boolean_field_display=json.loads(custom_field_dict[key]['boolean_field_display'])
                                   if custom_field_dict[key]['boolean_field_display'] else {},  # 之前model允许为空了，为了兼容先这么写,
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
        state_info_dict = init_state_obj.get_dict()
        state_info_dict.update(
            field_list=new_field_list, label=json.loads(init_state_obj.label), transition=transition_info_list)
        state_info_dict.pop('state_field_str')
        return True, state_info_dict

    @classmethod
    @auto_log
    def get_format_participant_info(cls, participant_type_id: int, participant: str)->tuple:
        """
        获取格式化的参与人信息
        get format participant info
        :param participant_type_id:
        :param participant:
        :return:
        """
        participant_name = participant
        participant_type_name = ''
        participant_alias = ''
        if participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
            participant_type_name = '个人'
            flag, participant_user_obj = account_base_service_ins.get_user_by_username(participant)
            if not flag:
                participant_alias = participant
            else:
                participant_alias = participant_user_obj.alias
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            participant_type_name = '多人'
            # 依次获取人员信息
            participant_name_list = participant_name.split(',')
            participant_alias_list = []
            for participant_name0 in participant_name_list:
                flag, participant_user_obj = account_base_service_ins.get_user_by_username(participant_name0)
                if not flag:
                    participant_alias_list.append(participant_name0)
                else:
                    participant_alias_list.append(participant_user_obj.alias)
            participant_alias = ','.join(participant_alias_list)
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            participant_type_name = '部门'
            # 支持多部门
            flag, dept_queryset = account_base_service_ins.get_dept_by_ids(participant)
            dept_info_dict = {}
            for dept0 in dept_queryset:
                dept_info_dict[str(dept0.id)] = dept0.name
            participant_split_id_str_list = participant.split(',')

            participant_dept_info_list = []
            for participant_split_id_str in participant_split_id_str_list:
                if dept_info_dict.get(participant_split_id_str):
                    participant_dept_info_list.append(dept_info_dict.get(participant_split_id_str))
                else:
                    participant_dept_info_list.append('未知')

            participant_alias = ','.join(participant_dept_info_list)

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            participant_type_name = '角色'
            flag, role_obj = account_base_service_ins.get_role_by_id(int(participant))
            if flag is False or (not role_obj):
                participant_alias = '未知'
            else:
                participant_alias = role_obj.name
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_VARIABLE:
            participant_type_name = '变量'
            # 支持多变量的展示
            participant_name_list = participant_name.split(',')
            participant_name_alias_list = []
            for participant_name0 in participant_name_list:
                if participant_name0 == 'creator':
                    participant_name_alias_list.append('工单创建人')
                elif participant_name0 == 'creator_tl':
                    participant_name_alias_list.append('工单创建人tl')
                else:
                    participant_name_alias_list.append('未知')
            participant_alias = ','.join(participant_name_alias_list)


        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
            if participant:
                flag, result = workflow_run_script_service_ins.get_run_script_by_id(int(participant))
                if flag:
                    participant_alias = result.get('script_obj').name
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
            participant_type_name = 'hook'
            participant_alias = participant_name

        return True, dict(participant=participant, participant_name=participant_name,
                          participant_type_id=participant_type_id, participant_type_name=participant_type_name,
                          participant_alias=participant_alias)

    @classmethod
    @auto_log
    def add_workflow_state(cls, workflow_id: int, name: str, is_hidden: int, order_id: int,
                           type_id: int, remember_last_man_enable: int, participant_type_id: int, participant: str,
                           distribute_type_id: int, state_field_str: str, label: str, creator: str,
                           enable_retreat: int)->tuple:
        """
        新增工作流状态
        add workflow state
        :param workflow_id:
        :param name:
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
        :param enable_retreat:
        :return:
        """
        workflow_state_obj = State(
            workflow_id=workflow_id, name=name, is_hidden=is_hidden, order_id=order_id,
            type_id=type_id, remember_last_man_enable=remember_last_man_enable, participant_type_id=participant_type_id,
            participant=participant, distribute_type_id=distribute_type_id, state_field_str=state_field_str,
            label=label, creator=creator, enable_retreat=enable_retreat)
        workflow_state_obj.save()
        return True, dict(workflow_state_id=workflow_state_obj.id)

    @classmethod
    @auto_log
    def edit_workflow_state(cls, state_id: int, workflow_id: int, name: str, is_hidden: int,
                            order_id: int, type_id: int, remember_last_man_enable: int, participant_type_id: int,
                            participant: str, distribute_type_id: int, state_field_str: str, label: str,
                            enable_retreat: int)->tuple:
        """
        新增工作流状态
        edit workflow state
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
        :param enable_retreat:
        :return:
        """
        state_obj = State.objects.filter(id=state_id, is_deleted=0)
        if state_obj:
            state_obj.update(workflow_id=workflow_id, name=name,
                             is_hidden=is_hidden, order_id=order_id, type_id=type_id,
                             remember_last_man_enable=remember_last_man_enable, participant_type_id=participant_type_id,
                             participant=participant, distribute_type_id=distribute_type_id,
                             state_field_str=state_field_str, label=label, enable_retreat=enable_retreat)
        return True, ''

    @classmethod
    @auto_log
    def del_workflow_state(cls, state_id: int)->tuple:
        """
        删除状态
        :param state_id:
        :return:
        """
        state_obj = State.objects.filter(id=state_id, is_deleted=0)
        if state_obj:
            state_obj.update(is_deleted=1)
        return True, {}


workflow_state_service_ins = WorkflowStateService()
