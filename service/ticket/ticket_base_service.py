import copy
import json
import datetime
import random
import functools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from apps.ticket.models import TicketRecord, TicketCustomField, TicketFlowLog
from apps.workflow.models import CustomField
from service.account.account_base_service import AccountBaseService
from service.base_service import BaseService
from service.common.common_service import CommonService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.workflow.workflow_base_service import WorkflowBaseService
from service.workflow.workflow_custom_field_service import WorkflowCustomFieldService
from service.workflow.workflow_state_service import WorkflowStateService
from service.workflow.workflow_transition_service import WorkflowTransitionService


class TicketBaseService(BaseService):
    """
    工单基础服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_ticket_by_id(cls, ticket_id):
        """
        获取工单对象
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if ticket_obj:
            return ticket_obj, ''
        else:
            return False, 'ticket is not existed or has been deleted'

    @classmethod
    @auto_log
    def get_ticket_list(cls, sn='', title='', username='', create_start='', create_end='', workflow_ids='', state_ids='', ticket_ids= '', category='', reverse=1, per_page=10, page=1, app_name='', is_end='', is_rejected=''):
        """
        工单列表
        :param sn:
        :param title:
        :param username:
        :param create_start: 创建时间起
        :param create_end: 创建时间止
        :param workflow_ids: 工作流id,str,逗号隔开
        :param state_ids: 状态id,str,逗号隔开
        :param category: 查询类别(创建的，待办的，关联的:包括创建的、处理过的、曾经需要处理但是没有处理的)
        :param reverse: 按照创建时间倒序
        :param per_page:
        :param page:
        :param app_name:
        :param is_end: 已结束
        :param is_rejected: 已拒绝

        :return:
        """
        category_list = ['all', 'owner', 'duty', 'relation']
        if category not in category_list:
            return False, '查询类别错误'
        query_params = Q(is_deleted=False)

        # 获取app_name 有权限的workflow_id_list
        permission_workflow_id_list, msg = AccountBaseService.app_workflow_permission_list(app_name)
        if not permission_workflow_id_list:
            return False, 'This app_name have not workflow permission'
        else:
            query_params &= Q(workflow_id__in=permission_workflow_id_list)
        if is_end:
            if is_end == '0':
                query_params &= Q(is_end=0)
            elif is_end == '1':
                query_params &= Q(is_end=1)
        if is_rejected and is_rejected == '0':
            query_params &= Q(is_rejected=0)
        if is_rejected and is_rejected == '1':
            query_params &= Q(is_rejected=1)

        if sn:
            query_params &= Q(sn__startswith=sn)
        if title:
            query_params &= Q(title__contains=title)
        if create_start:
            query_params &= Q(gmt_created__gte=create_start)
        if create_end:
            query_params &= Q(gmt_created__lte=create_end)
        if workflow_ids:
            workflow_id_str_list = workflow_ids.split(',')
            workflow_id_list = [int(workflow_id_str) for workflow_id_str in workflow_id_str_list]
            query_params &= Q(workflow_id__in=workflow_id_list)
        if state_ids:
            state_id_str_list = state_ids.split(',')
            state_id_list = [int(state_id_str) for state_id_str in state_id_str_list]
            query_params &= Q(state_id__in=state_id_list)
        if ticket_ids:
            ticket_id_str_list = ticket_ids.split(',')
            ticket_id_list = [int(ticket_id_str) for ticket_id_str in ticket_id_str_list]
            query_params &= Q(id__in=ticket_id_list)

        if reverse:
            order_by_str = '-gmt_created'
        else:
            order_by_str = 'gmt_created'

        if category == 'owner':
            query_params &= Q(creator=username)
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str)
        elif category == 'duty':
            # 获取用户部门id列表, 角色id列表，工单的实际当前处理人只会有个人、多人、角色、部门、脚本(变量、工单字段、父工单字段这些类型会在工单流转的时候计算为实际的值)
            user_obj, msg = AccountBaseService.get_user_by_username(username)
            if not user_obj:
                return False, msg
            user_dept_id_list, msg2 = AccountBaseService.get_user_up_dept_id_list(username)
            user_role_id_list, msg3 = AccountBaseService.get_user_role_id_list(username)
            if user_dept_id_list is False:
                return False, msg2
            if user_role_id_list is False:
                return False, msg3
            user_dept_id_str_list = [str(user_dept_id) for user_dept_id in user_dept_id_list]
            user_role_id_str_list = [str(user_role_id) for user_role_id in user_role_id_list]
            duty_query_expression = Q(participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, participant=username)
            duty_query_expression |= Q(participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT, participant__in=user_dept_id_str_list)
            duty_query_expression |= Q(participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE, participant__in=user_role_id_str_list)

            # 多人的情况，逗号隔开，需要用extra查询实现, 这里会存在注入问题，后续改进下
            ticket_query_set1 = TicketRecord.objects.filter(query_params).extra(where=['FIND_IN_SET("{}", participant)'.format(username), 'participant_type_id in ({}, {})'.format(CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI, CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL)])
            query_params &= duty_query_expression
            ticket_query_set2 = TicketRecord.objects.filter(query_params)

            ticket_objects = (ticket_query_set1 | ticket_query_set2).order_by(order_by_str)

        elif category == 'relation':
            ticket_objects = TicketRecord.objects.filter(query_params).extra(where=['FIND_IN_SET("{}", relation)'.format(username)]).order_by(order_by_str)
        else:
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str)

        paginator = Paginator(ticket_objects, per_page)


        try:
            ticket_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            ticket_result_paginator = paginator.page(paginator.num_pages)

        ticket_result_object_list = ticket_result_paginator.object_list
        ticket_result_restful_list = []
        for ticket_result_object in ticket_result_object_list:
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_result_object.state_id)
            state_name = state_obj.name
            participant_info, msg = cls.get_ticket_format_participant_info(ticket_result_object.id)

            workflow_obj, msg = WorkflowBaseService.get_by_id(ticket_result_object.workflow_id)
            workflow_info_dict = dict(workflow_id=workflow_obj.id, workflow_name=workflow_obj.name)

            creator_obj, msg = AccountBaseService.get_user_by_username(ticket_result_object.creator)
            if creator_obj:
                dept_id = creator_obj.dept_id
                # 获取部门信息
                dept_info, msg = AccountBaseService.get_dept_by_id(dept_id)
                if dept_info:
                    dept_dict_info = dept_info.get_dict()
                else:
                    dept_dict_info = dict(id=dept_id, name='')
                creator_info = dict(username=creator_obj.username, alias=creator_obj.alias, is_active=creator_obj.is_active,
                                    email=creator_obj.email, phone=creator_obj.phone, dept_info=dept_dict_info)
            else:
                creator_info = dict(username=ticket_result_object.creator, alias='', is_active=False, email='', phone='', dept_info={})
            ticket_result_restful_list.append(dict(id=ticket_result_object.id,
                                                   title=ticket_result_object.title,
                                                   workflow=workflow_info_dict,
                                                   sn=ticket_result_object.sn,
                                                   state=dict(state_id=ticket_result_object.state_id, state_name=state_name, state_label=json.loads(state_obj.label)),
                                                   parent_ticket_id=ticket_result_object.parent_ticket_id,
                                                   parent_ticket_state_id=ticket_result_object.parent_ticket_state_id,
                                                   participant_info=participant_info,
                                                   creator=ticket_result_object.creator,
                                                   creator_info=creator_info,
                                                   gmt_created=str(ticket_result_object.gmt_created)[:19],
                                                   gmt_modified=str(ticket_result_object.gmt_modified)[:19],
                                                   is_end=ticket_result_object.is_end,
                                                   ))
        return ticket_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def new_ticket(cls, request_data_dict, app_name=''):
        """
        新建工单
        :param request_data_dict:
        :param app_name:调用源app_name
        :return:
        """
        workflow_id = request_data_dict.get('workflow_id')
        transition_id = request_data_dict.get('transition_id')
        username = request_data_dict.get('username')

        parent_ticket_id = request_data_dict.get('parent_ticket_id', 0)
        parent_ticket_state_id = request_data_dict.get('parent_ticket_state_id', 0)
        suggestion = request_data_dict.get('suggestion', '')
        if not (workflow_id and transition_id and username):
            return False, u'参数不合法,请提供workflow_id，username，transition_id'

        request_field_arg_list = [key for key, value in request_data_dict.items() if (key not in ['workflow_id', 'suggestion', 'username'])]

        # 判断用户是否有权限新建该工单
        has_permission, msg = WorkflowBaseService.check_new_permission(username, workflow_id)
        if not has_permission:
            return False, msg
        # 获取工单必填信息
        ## 获取工作流初始状态
        start_state, msg = WorkflowStateService.get_workflow_start_state(workflow_id)
        if not start_state:
            return False, msg
        # 获取初始状态必填字段 及允许更新的字段
        flag, state_info_dict = cls.get_state_field_info(start_state.id)
        require_field_list = state_info_dict.get('require_field_list', [])
        update_field_list = state_info_dict.get('update_field_list', [])

        # 校验是否所有必填字段都有提供，如果transition_id对应设置为不校验必填则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))
        flag, msg = cls.get_next_state_id_by_transition_and_ticket_info(0, request_data_dict)
        if flag:
            destination_state_id = msg.get('destination_state_id')
        else:
            return False, msg

        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(destination_state_id)

        # 获取目标状态的信息
        flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id, ticket_req_dict=request_data_dict)
        if not flag:
            return False, participant_info
        destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
        destination_participant = participant_info.get('destination_participant', '')
        multi_all_person = participant_info.get('multi_all_person', '{}')

        # 生成流水号
        ticket_sn, msg = cls.gen_ticket_sn(app_name)
        if not ticket_sn:
            return False, msg
        # 新增工单基础表数据
        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END:
            is_end = True
        else:
            is_end = False

        new_ticket_obj = TicketRecord(sn=ticket_sn, title=request_data_dict.get('title', ''), workflow_id=workflow_id,
                                      state_id=destination_state_id, parent_ticket_id=parent_ticket_id, parent_ticket_state_id=parent_ticket_state_id, participant=destination_participant,
                                      participant_type_id=destination_participant_type_id, relation=username, creator=username, is_end=is_end, multi_all_person=multi_all_person)
        new_ticket_obj.save()
        # 更新工单关系人
        add_relation, msg = cls.get_ticket_dest_relation(destination_participant_type_id, destination_participant)
        if add_relation:
            new_relation, msg = cls.add_ticket_relation(new_ticket_obj.id, add_relation)  # 更新关系人信息
        # 新增自定义字段，只保存required_field
        request_data_dict_allow = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                request_data_dict_allow[key] = value

        update_ticket_custom_field_result, msg = cls.update_ticket_custom_field(new_ticket_obj.id, request_data_dict_allow)
        if not update_ticket_custom_field_result:
            return False, msg
        # 新增流转记录
        ## 获取工单所有字段的值
        all_ticket_data, msg = cls.get_ticket_all_field_value(new_ticket_obj.id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)
        new_ticket_flow_log_dict = dict(ticket_id=new_ticket_obj.id, transition_id=transition_id, suggestion=suggestion,
                                        participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, participant=username,
                                        state_id=start_state.id, ticket_data=all_ticket_data_json)
        add_ticket_flow_log_result, msg = cls.add_ticket_flow_log(new_ticket_flow_log_dict)
        if not add_ticket_flow_log_result:
            return False, msg
        # 通知消息
        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[new_ticket_obj.id], queue='loonflow')

        # 如果下个状态为脚本处理，则开始执行脚本
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            from tasks import run_flow_task # 放在文件开头会存在循环引用
            run_flow_task.apply_async(args=[new_ticket_obj.id, destination_participant, destination_state_id], queue='loonflow')

        # 如果下个状态是hook，开始触发hook
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_HOOK:
            # 因为工单基础表中不保存hook配置，所以从状态表中获取
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(new_ticket_obj.state_id)
            from tasks import flow_hook_task  # 放在文件开头会存在循环引用
            flow_hook_task.apply_async(args=[new_ticket_obj.id], queue='loonflow')


        # 定时器处理逻辑
        cls.handle_timer_transition(new_ticket_obj.id, destination_state_id)

        # 父工单逻辑处理
        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END and new_ticket_obj.parent_ticket_id and new_ticket_obj.parent_ticket_state_id:
                # 如果存在父工单，判断是否该父工单的下属子工单都已经结束状态，如果都是结束状态则自动流转父工单到下个状态
            other_sub_ticket_queryset = TicketRecord.objects.filter(parent_ticket_id=new_ticket_obj.parent_ticket_id, parent_ticket_state_id= new_ticket_obj.parent_ticket_state_id,
                                                                    is_deleted=0).all()
            # 所有子工单使用相同的工作流,所以state都一样，检测是否都是ticket_obj.state_id即可判断是否都是结束状态
            other_sub_ticket_state_id_list = [other_sub_ticket.state_id for other_sub_ticket in other_sub_ticket_queryset]
            if set(other_sub_ticket_state_id_list) == set([new_ticket_obj.state_id]):
                parent_ticket_obj = TicketRecord.objects.filter(id=new_ticket_obj.parent_ticket_id, is_deleted=0).first()
                parent_ticket_state_id = parent_ticket_obj.state_id
                parent_ticket_transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(parent_ticket_state_id)
                # 含有子工单的工单状态只支持单路径流转到下个状态
                parent_ticket_transition_id = parent_ticket_transition_queryset[0].id
                cls.handle_ticket(parent_ticket_obj.id, dict(transition_id=parent_ticket_transition_id,
                                                             username='loonrobot', suggestion='所有子工单处理完毕，自动流转'))
        return new_ticket_obj.id, ''

    @classmethod
    @auto_log
    def gen_ticket_sn(cls, app_name=''):
        redis_host = settings.REDIS_HOST
        redis_db = settings.REDIS_DB
        redis_port = settings.REDIS_PORT
        redis_password = settings.REDIS_PASSWORD
        import redis
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        import datetime
        ticket_day_count_key = 'ticket_day_count_{}'.format(str(datetime.datetime.now())[:10])
        ticket_day_count = r.get(ticket_day_count_key)
        if ticket_day_count is None:
            # 查询数据库中个数
            # 今天和明天
            today = str(datetime.datetime.now())[:10] + " 00:00:00"
            next_day = str(datetime.datetime.now() + datetime.timedelta(days=1))[:10] + " 00:00:00"
            # 包括is_deleted=1的数据

            ticket_day_count = TicketRecord.objects.filter(gmt_created__gte=today, gmt_created__lte=next_day).count()
        new_ticket_day_count = int(ticket_day_count) + 1
        r.set(ticket_day_count_key, new_ticket_day_count, 86400)
        now_day = datetime.datetime.now()
        if not app_name:
            sn_prefix = 'loonflow'
        else:
            app_token_obj, msg = AccountBaseService.get_token_by_app_name(app_name)
            sn_prefix = app_token_obj.ticket_sn_prefix

        return '%s_%04d%02d%02d%04d' % (sn_prefix, now_day.year, now_day.month, now_day.day, new_ticket_day_count), ''

    @classmethod
    @auto_log
    def get_ticket_field_value(cls, ticket_id, field_key):
        """
        获取工单字段的值
        :param ticket_id:
        :param field_key:
        :return:
        """
        #分为基础字段和自定义字段
        if field_key in CONSTANT_SERVICE.TICKET_BASE_FIELD_LIST:
            ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
            ticket_obj_dict = ticket_obj.__dict__
            value = ticket_obj_dict.get(field_key)
            msg = ''
        else:
            value, msg = cls.get_ticket_custom_field_value(ticket_id, field_key)
        return value, msg

    @classmethod
    @auto_log
    def get_ticket_format_custom_field_key_dict(cls, ticket_id):
        """
        获取工单的自定义字段的格式化dict信息
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        custom_field_queryset = CustomField.objects.filter(is_deleted=0, workflow_id=ticket_obj.workflow_id).all()
        format_field_key_dict = {}
        for custom_field in custom_field_queryset:
            format_field_key_dict[custom_field.field_key] = dict(field_type_id=custom_field.field_type_id, name=custom_field.field_name, bool_field_display=custom_field.boolean_field_display,
                                                                 field_choice=custom_field.field_choice, field_from='custom')

        return format_field_key_dict, ''

    @classmethod
    @auto_log
    def get_ticket_custom_field_value(cls, ticket_id, field_key):
        """
        获取工单的自定义字段的值
        :param ticket_id:
        :param field_key:
        :return:
        """
        format_field_key_dict, msg = cls.get_ticket_format_custom_field_key_dict(ticket_id)
        if not format_field_key_dict:
            return False, msg   # 这里不好区分是出错了，还是这个field_key对应的值确实是False. 后续想想有没什么好的方法

        field_type_id = format_field_key_dict[field_key]['field_type_id']
        ticket_custom_field_obj = TicketCustomField.objects.filter(field_key=field_key, ticket_id=ticket_id, is_deleted=0).first()

        if not ticket_custom_field_obj:
            # 因为有可能该字段还没赋值
            value = None
        else:
            if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                value = ticket_custom_field_obj.char_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                value = ticket_custom_field_obj.int_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                value = ticket_custom_field_obj.float_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                value = ticket_custom_field_obj.bool_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                value = str(ticket_custom_field_obj.date_value)
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                value = str(ticket_custom_field_obj.datetime_value)
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                value = ticket_custom_field_obj.radio_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                value = ticket_custom_field_obj.checkbox_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                value = ticket_custom_field_obj.select_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                value = ticket_custom_field_obj.multi_select_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                value = ticket_custom_field_obj.text_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                value = ticket_custom_field_obj.username_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                value = ticket_custom_field_obj.multi_username_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                value = ticket_custom_field_obj.char_value
        return value, ''

    @classmethod
    @auto_log
    def get_ticket_field_name(cls, ticket_id, field_key):
        """
        获取工单的字段名称
        :param ticket_id:
        :param field_key:
        :return:
        """
        if field_key in CONSTANT_SERVICE.TICKET_BASE_FIELD_LIST:
            return field_key, ''
        else:
            field_name, msg = cls.get_ticket_custom_field_name(ticket_id, field_key)

        return field_name, ''

    @classmethod
    @auto_log
    def get_ticket_custom_field_name(cls, ticket_id, field_key):
        """
        获取工单自定义字段的名称
        :param ticket_id:
        :param field_key:
        :return:
        """
        format_field_key_dict, msg = cls.get_ticket_format_custom_field_key_dict(ticket_id)
        field_name = format_field_key_dict[field_key]['field_name']

        return field_name, ''

    @classmethod
    @auto_log
    def update_ticket_custom_field(cls, ticket_id, update_dict):
        """
        更新工单自定义字段（新增或者修改）
        :param ticket_id:
        :param update_dict:
        :return:
        """
        # 获取工单的自定义字段
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        format_custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(ticket_obj.workflow_id)
        if format_custom_field_dict is False:
            return False, msg
        custom_field_key_list = [key for key, value in format_custom_field_dict.items()]

        # 因为工单的自定义字段不会太多，且有可能是新增有可能是更新， 所以直接遍历处理
        for key, value in update_dict.items():
            if key in custom_field_key_list:
                # 判断是否存在，如果存在则更新，如果不存在则新增
                ticket_custom_field_queryset = TicketCustomField.objects.filter(ticket_id=ticket_id, field_key=key)
                field_type_id = format_custom_field_dict[key]['field_type_id']

                if update_dict.get(key) is None:
                    # 值为None。说明此字段为可选，且用户未填写或者清空了该字段,需要清空字段
                    if ticket_custom_field_queryset:
                        # 已经存在，需要删除
                        ticket_custom_field_queryset.update(is_deleted=1)
                    else:
                        # 不存在的，直接忽略
                        pass
                else:
                    if ticket_custom_field_queryset:
                        if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                            ticket_custom_field_queryset.update(char_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                            ticket_custom_field_queryset.update(int_value=int(update_dict.get(key)))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                            ticket_custom_field_queryset.update(float_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                            ticket_custom_field_queryset.update(bool_value=int(update_dict.get(key)))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                            ticket_custom_field_queryset.update(date_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                            ticket_custom_field_queryset.update(datetime_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                            ticket_custom_field_queryset.update(radio_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                            ticket_custom_field_queryset.update(checkbox_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                            ticket_custom_field_queryset.update(select_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                            ticket_custom_field_queryset.update(multi_select_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                            ticket_custom_field_queryset.update(text_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                            ticket_custom_field_queryset.update(username_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                            ticket_custom_field_queryset.update(multi_username_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                            ticket_custom_field_queryset.update(char_value=update_dict.get(key))
                    elif not ticket_custom_field_queryset:
                        if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'], ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, char_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, int_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, float_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, bool_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, date_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, datetime_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, radio_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, checkbox_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, select_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, multi_select_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, text_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, username_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, multi_username_value=update_dict.get(key))
                        elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                            new_ticket_custom_field_record = TicketCustomField(name=format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, char_value=update_dict.get(key))
                        new_ticket_custom_field_record.save()
        return True, ''

    @classmethod
    @auto_log
    def update_ticket_field_value(cls, ticket_id, update_dict):
        """
        更新工单字段的值
        :param ticket_id:
        :param update_dict:
        :return:
        """
        base_field_dict = {}
        for key, value in update_dict.items():
            if key in CONSTANT_SERVICE.TICKET_BASE_FIELD_LIST:
                base_field_dict[key] = value
        # 更新工单基础字段的值
        if base_field_dict:
            TicketRecord.objects.filter(id=ticket_id, is_deleted=0).update(**base_field_dict)
        cls.update_ticket_custom_field(ticket_id, update_dict)

        return True, ''

    @classmethod
    @auto_log
    def add_ticket_flow_log(cls, kwargs):
        """
        新增工单流转记录
        :param kwargs:
        :return:
        """
        # suggestion长度处理,在某些mysql版本默认配置中，如果插入时候字段长度大于字段定义的长度会报错，而不是自动截断
        if len(kwargs.get('suggestion', '')) > 1000:
            kwargs['suggestion'] = '{}...(超过字段定义长度,自动截断)'.format(kwargs.get('suggestion', '')[:960])
        if not kwargs.get('creator'):
            kwargs['creator'] = kwargs.get('participant', '')
        new_ticket_flow_log = TicketFlowLog(**kwargs)
        new_ticket_flow_log.save()
        return new_ticket_flow_log.id, ''

    @classmethod
    @auto_log
    def get_ticket_detail(cls, ticket_id, username):
        """
        获取工单详情,有处理权限，则按照当前状态返回对应的字段信息，只有查看权限则返回该工单对应工作流配置的展示字段信息
        :param ticket_id:
        :param username:
        :return:
        """
        handle_permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not handle_permission:
            view_permission, msg = cls.ticket_view_permission_check(ticket_id, username)
            if not view_permission:
                return False, msg
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        field_list, msg = cls.get_ticket_base_field_list(ticket_id)

        new_field_list = []

        if handle_permission:
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_obj.state_id)
            if not state_obj:
                return False, msg
            state_field_str = state_obj.state_field_str
            state_field_dict = json.loads(state_field_str)
            state_field_key_list = state_field_dict.keys()
            for field in field_list:
                if field['field_key'] in state_field_key_list:
                    field['field_attribute'] = state_field_dict[field['field_key']]
                    new_field_list.append(field)
        else:
            # 查看权限
            workflow_obj, msg = WorkflowBaseService.get_by_id(workflow_id=ticket_obj.workflow_id)
            display_form_field_list = json.loads(workflow_obj.display_form_str)
            for field in field_list:
                if field['field_key'] in display_form_field_list:
                    new_field_list.append(field)
        # 字段排序
        new_field_list = sorted(new_field_list, key=lambda r: r['order_id'])

        creator_obj, msg = AccountBaseService.get_user_by_username(ticket_obj.creator)
        if creator_obj:
            dept_id = creator_obj.dept_id
            # 获取部门信息
            dept_info, msg = AccountBaseService.get_dept_by_id(dept_id)
            if dept_info:
                dept_dict_info = dept_info.get_dict()
            else:
                dept_dict_info = dict(id=dept_id, name='')

            creator_info = dict(username=creator_obj.username, alias=creator_obj.alias,
                                is_active=creator_obj.is_active, email=creator_obj.email,
                                phone=creator_obj.phone, dept_info=dept_dict_info)
        else:
            creator_info = dict(username=ticket_obj.creator, alias='', is_active=False, email='', phone='', dept_info={})

        return dict(id=ticket_obj.id, sn=ticket_obj.sn, title=ticket_obj.title, state_id=ticket_obj.state_id, parent_ticket_id=ticket_obj.parent_ticket_id,
                    participant=ticket_obj.participant, participant_type_id=ticket_obj.participant_type_id, workflow_id=ticket_obj.workflow_id,
                    creator=ticket_obj.creator, gmt_created=str(ticket_obj.gmt_created)[:19], gmt_modified=str(ticket_obj.gmt_modified)[:19],
                    script_run_last_result=ticket_obj.script_run_last_result, field_list=new_field_list, creator_info=creator_info), ''

    @classmethod
    @auto_log
    def get_ticket_base_field_list(cls, ticket_id):
        """
        获取工单字段信息,
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_obj.state_id)
        if not state_obj:
            return False, msg
        state_name = state_obj.name

        # 工单基础字段及属性
        field_list = []
        participant_info_dict, msg = cls.get_ticket_format_participant_info(ticket_id)
        workflow_obj, msg = WorkflowBaseService.get_by_id(ticket_obj.workflow_id)
        workflow_name = workflow_obj.name

        field_list.append(dict(field_key='sn', field_name=u'流水号', field_value=ticket_obj.sn, order_id=10, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的流水号', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='title', field_name=u'标题', field_value=ticket_obj.title, order_id=20, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的标题', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='state_id', field_name=u'状态id', field_value=ticket_obj.state_id, order_id=40, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前状态的id', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='participant_info.participant_name', field_name=u'当前处理人', field_value=participant_info_dict['participant_name'], order_id=50, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的当前处理人', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='participant_info.participant_alias', field_name=u'当前处理人', field_value=participant_info_dict['participant_alias'], order_id=55, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前处理人(alias)', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))

        field_list.append(dict(field_key='workflow.workflow_name', field_name=u'工作流名称', field_value=workflow_name, order_id=60, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单所属工作流的名称', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))

        field_list.append(dict(field_key='creator', field_name=u'创建人', field_value=ticket_obj.creator, order_id=80, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的创建人', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='gmt_created', field_name=u'创建时间', field_value=str(ticket_obj.gmt_created)[:19], order_id=100, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的创建时间', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='gmt_modified', field_name=u'更新时间', field_value=str(ticket_obj.gmt_modified)[:19], order_id=120, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的更新时间', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))
        field_list.append(dict(field_key='state.state_name', field_name=u'状态名', field_value=state_name, order_id=41, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前状态的名称', field_choice={}, boolean_field_display={}, default_value=None, field_template='', label={}))

        # 工单所有自定义字段
        custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(ticket_obj.workflow_id)
        custom_field_key_list = [key for key, value in custom_field_dict.items()]
        ticket_custom_field_objs = TicketCustomField.objects.filter(ticket_id=ticket_id, field_key__in=custom_field_key_list, is_deleted=0).all()
        key_value_dict = {}
        for ticket_custom_field_obj in ticket_custom_field_objs:
            key_value_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj
        for key, value in custom_field_dict.items():
            field_type_id = value['field_type_id']
            field_value_obj = key_value_dict.get(key)
            if not field_value_obj:
                field_value = None
            else:
                # 根据字段类型 获取对应列的值
                if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                    field_value = field_value_obj.char_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                    field_value = field_value_obj.int_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                    field_value = field_value_obj.float_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                    field_value = field_value_obj.bool_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                    field_value = str(field_value_obj.date_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                    field_value = str(field_value_obj.datetime_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                    field_value = field_value_obj.radio_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                    field_value = field_value_obj.checkbox_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                    field_value = field_value_obj.select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                    field_value = field_value_obj.multi_select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                    field_value = field_value_obj.text_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                    field_value = field_value_obj.username_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                    field_value = field_value_obj.multi_username_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                    field_value = field_value_obj.char_value

            field_list.append(dict(field_key=key, field_name=custom_field_dict[key]['field_name'], field_value=field_value, order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO,
                                   default_value=custom_field_dict[key]['default_value'],
                                   description=custom_field_dict[key]['description'],
                                   field_template=custom_field_dict[key]['field_template'],
                                   boolean_field_display=json.loads(custom_field_dict[key]['boolean_field_display']) if custom_field_dict[key]['boolean_field_display'] else {},  # 之前model允许为空了，为了兼容先这么写
                                   field_choice=json.loads(custom_field_dict[key]['field_choice']),
                                   label=json.loads(custom_field_dict[key]['label'])

                                   ))
        return field_list, ''

    @classmethod
    @auto_log
    def get_ticket_format_participant_info(cls, ticket_id):
        """
        获取工单参与人信息
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        participant = ticket_obj.participant
        participant_name = ticket_obj.participant
        participant_type_id = ticket_obj.participant_type_id
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
        # elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL:
        #     participant_type_name = '多人且全部处理'
        #     # 从multi_all_person中获取处理人信息
        #     multi_all_person_dict = json.loads(ticket_obj.multi_all_person)
        #     participant_alias0_list = []
        #     for key, value in multi_all_person_dict.items():
        #         participant_user_obj, msg = AccountBaseService.get_user_by_username(key)
        #         if not participant_user_obj:
        #             participant_alias0 = key
        #         else:
        #             participant_alias0 = participant_user_obj.alias
        #         if value:
        #             participant_alias0_list.append('{}({})已处理:{}'.format(participant_alias0, key, value.get('transition_name')))
        #         else:
        #             participant_alias0_list.append('{}({})未处理:{}'.format(participant_alias0, key, value.get('transition_name')))
        #     participant_alias = ';'.join(participant_alias0_list)

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            participant_type_name = '部门'
            dept_obj, msg = AccountBaseService.get_dept_by_id(int(ticket_obj.participant))
            if not dept_obj:
                return False, 'dept is not existed or has been deleted'
            participant_name = dept_obj.name
            participant_alias = participant_name
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            participant_type_name = '角色'
            role_obj, msg = AccountBaseService.get_role_by_id(int(ticket_obj.participant))
            if not role_obj:
                return False, 'role is not existedor has been deleted'
            participant_name = role_obj.name
            participant_alias = participant_name
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            # 脚本类型参数与人是脚本记录的id
            from apps.workflow.models import WorkflowScript
            script_obj = WorkflowScript.objects.filter(id=int(participant), is_deleted=0).first()
            if script_obj:
                participant_name = participant
                participant_alias = '脚本:{}'.format(script_obj.name)

        if json.loads(ticket_obj.multi_all_person):
            participant_type_name = '多人且全部处理'
            # 从multi_all_person中获取处理人信息
            multi_all_person_dict = json.loads(ticket_obj.multi_all_person)
            participant_alias0_list = []
            for key, value in multi_all_person_dict.items():
                participant_user_obj, msg = AccountBaseService.get_user_by_username(key)
                if not participant_user_obj:
                    participant_alias0 = key
                else:
                    participant_alias0 = participant_user_obj.alias
                if value:
                    participant_alias0_list.append(
                        '{}({})已处理:{}'.format(participant_alias0, key, value.get('transition_name')))
                else:
                    participant_alias0_list.append(
                        '{}({})未处理:{}'.format(participant_alias0, key, value.get('transition_name')))
            participant_alias = ';'.join(participant_alias0_list)
        # 工单基础表中不存在参与人为其他类型的情况
        return dict(participant=participant, participant_name=participant_name, participant_type_id=participant_type_id,
                    participant_type_name=participant_type_name, participant_alias=participant_alias), ''

    @classmethod
    @auto_log
    def ticket_handle_permission_check(cls, ticket_id, username, by_timer=False, by_task=False, by_hook=False):
        """
        处理权限校验: 获取当前状态是否需要处理， 该用户是否有权限处理
        :param ticket_id:
        :param username:
        :param by_timer:是否为定时器流转
        :param by_task:是否为通过脚本流转
        :param by_hook:是否hook回调触发的流转
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        ticket_state_id = ticket_obj.state_id
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(ticket_state_id)
        if not transition_queryset:
            return None, '工单当前状态无需操作'
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_state_id)
        if not state_obj:
            return False, '工单当前状态id不存在或已被删除'
        if by_timer and username == 'loonrobot':
            # 定时器流转，有权限
            return True, dict(need_accept=False, in_add_node=False, msg='定时器流转，放开处理权限')
        if by_task and username == 'loonrobot':
            # 脚本流转，有权限
            return True, dict(need_accept=False, in_add_node=False, msg='脚本流转，放开处理权限')
        if by_hook and username == 'loonrobot':
            # hook触发流转，有权限
            return True, dict(need_accept=False, in_add_node=False, msg='hook触发流转，放开处理权限')

        participant_type_id = ticket_obj.participant_type_id
        participant = ticket_obj.participant

        current_participant_count = 1  # 当前处理人个数，用于当处理人大于1时 可能需要先接单再处理

        if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            if username != participant:
                return None, '非当前处理人，无权处理'
        elif participant_type_id in [CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI, CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL]:
            if username not in participant.split(','):
                return None, '非当前处理人，无权处理'
            current_participant_count = len(participant.split(','))
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            dept_user_list, msg = AccountBaseService.get_dept_username_list(dept_id=int(participant))
            if username not in dept_user_list:
                return None, '非当前处理人，无权处理'
            current_participant_count = len(dept_user_list)

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            role_user_list, msg = AccountBaseService.get_role_username_list(int(participant))
            if username not in role_user_list:
                return None, '非当前处理人，无权处理'
            current_participant_count = len(role_user_list)
        else:
            return None, '非当前处理人，无权处理'
        # PARTICIPANT_TYPE_VARIABLE, PARTICIPANT_TYPE_FIELD, PARTICIPANT_TYPE_PARENT_FIELD类型会在流转时保存为实际的处理人

        if current_participant_count > 1 and state_obj.distribute_type_id == CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_ACTIVE:
            need_accept = True
        else:
            need_accept = False
        if ticket_obj.in_add_node:
            in_add_node = True
        else:
            in_add_node = False

        return True, dict(need_accept=need_accept, in_add_node=in_add_node)

    @classmethod
    @auto_log
    def ticket_view_permission_check(cls, ticket_id, username):
        """
        校验用户是否有工单的查看权限:先查询对应的工作流是否校验查看权限， 如果不校验直接允许，如果校验需要判断用户是否属于工单的关系人
        :param ticket_id:
        :param username:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        workflow_obj, msg = WorkflowBaseService.get_by_id(ticket_obj.workflow_id)
        if not workflow_obj:
            return False, msg
        if not workflow_obj.view_permission_check:
            return True, '该工作流不限制查看权限'
        else:
            if username in ticket_obj.relation.split(','):
                return True, '用户是该工单的关系人，有查看权限'
            else:
                return False, '用户不是该工单的关系人，且该工作流开启了查看权限校验'

    @classmethod
    @auto_log
    def get_ticket_transition(cls, ticket_id, username):
        """
        获取用户针对工单当前可以做的操作:处理权限校验、可以做的操作
        :param ticket_id:
        :param username:
        :return:
        """
        handle_permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if handle_permission is False:
            return False, msg
        if not handle_permission:
            return [], '用户当前无处理权限'
        ticket_obj = TicketRecord.objects.filter(id=ticket_id).first()

        if ticket_obj.in_add_node:
            # 加签状态下，只允许"完成"操作, 完成后工单处理人设为add_node_man
            transition_dict_list = [dict(transition_id=0, transition_name='完成', field_require_check=False,
                                         is_accept=False, in_add_node=True, alert_enable=False, alert_text='',
                                         attribute_type_id=CONSTANT_SERVICE.TRANSITION_ATTRIBUTE_TYPE_OTHER)]
            return transition_dict_list, ''
        if msg['need_accept']:
            transition_dict_list = [dict(transition_id=0, transition_name='接单', field_require_check=False,
                                         is_accept=True, in_add_node=False, alert_enable=False, alert_text='',
                                         attribute_type_id=CONSTANT_SERVICE.TRANSITION_ATTRIBUTE_TYPE_OTHER)]
            return transition_dict_list, ''

        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(ticket_obj.state_id)
        transition_dict_list = []
        for transition in transition_queryset:
            transition_dict = dict(transition_id=transition.id, transition_name=transition.name,
                                   field_require_check=transition.field_require_check, is_accept=False,
                                   in_add_node=False, alert_enable=transition.alert_enable,
                                   alert_text=transition.alert_text, attribute_type_id=transition.attribute_type_id)
            transition_dict_list.append(transition_dict)
        return transition_dict_list, ''

    @classmethod
    @auto_log
    def handle_ticket(cls, ticket_id, request_data_dict, by_timer=False, by_task=False, by_hook=False):
        """
        处理工单:校验必填参数,获取当前状态必填字段，更新工单基础字段，更新工单自定义字段， 更新工单流转记录，执行必要的脚本，通知消息
        此处逻辑和新建工单有较多重复，下个版本会拆出来
        :param ticket_id:
        :param request_data_dict:
        :param by_timer: 是否通过定时器触发的流转
        :param by_task: 是否通过脚本执行完成后触发的流转
        :param by_hook: 是否hook回调用触发流转
        :return:
        """
        transition_id = request_data_dict.get('transition_id', '')
        username = request_data_dict.get('username', '')
        suggestion = request_data_dict.get('suggestion', '')

        if not (transition_id and username):
            return False, '参数不合法,请提供username，transition_id'
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
        source_ticket_state_id = ticket_obj.state_id
        if not ticket_obj:
            return False, '工单不存在或已被删除'

        # 判断用户是否有权限处理该工单
        has_permission, msg = cls.ticket_handle_permission_check(ticket_id, username, by_timer, by_task, by_hook)
        if not has_permission:
            return False, msg
        if msg['need_accept']:
            return False, '需要先接单再处理'
        if msg['in_add_node']:
            return False, '工单当前处于加签中，只允许加签完成操作'

        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_obj.state_id)
        if not state_obj:
            return False, msg

        # 获取初始状态必填字段 及允许更新的字段
        flag, state_info_dict = cls.get_state_field_info(state_obj.id)
        require_field_list = state_info_dict.get('require_field_list', [])
        update_field_list = state_info_dict.get('update_field_list', [])

        # 校验是否所有必填字段都有提供，如果transition_id对应设置为不校验必填则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:

            request_field_arg_list = [key for key, value in request_data_dict.items() if (key not in ['workflow_id', 'suggestion', 'username'])]
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))

        flag, msg = cls.get_next_state_id_by_transition_and_ticket_info(ticket_id, request_data_dict)
        if flag:
            destination_state_id = msg.get('destination_state_id')
        else:
            return False, msg

        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(destination_state_id)

        # 判断当前处理人类似是否为全部处理，如果处理类型为全部处理（根据json.loads(ticket_obj.multi_all_person)来判断），且有人未处理，则工单状态不变，只记录处理过程
        if json.loads(ticket_obj.multi_all_person):
            multi_all_person = ticket_obj.multi_all_person
            multi_all_person_dict = json.loads(multi_all_person)
            blank_or_false_value_key_list, msg = CommonService.get_dict_blank_or_false_value_key_list(multi_all_person_dict)
            if blank_or_false_value_key_list:
                multi_all_person_dict[username] = dict(transition_id=transition_id, transition_name=req_transition_obj.name)
                has_all_same_value, msg = CommonService.check_dict_has_all_same_value(multi_all_person_dict)
                if has_all_same_value:
                    # 所有人处理的transition都一致,则工单进入下个状态
                    flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id,
                                                                                   ticket_req_dict=request_data_dict)
                    if not flag:
                        return False, participant_info
                    destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
                    destination_participant = participant_info.get('destination_participant', '')
                else:
                    # 处理人没有没有全部处理完成或者处理动作不一致
                    destination_participant_type_id = ticket_obj.participant_type_id
                    next_blank_or_false_value_key_list, msg = CommonService.get_dict_blank_or_false_value_key_list(multi_all_person_dict)
                    destination_participant = ','.join(next_blank_or_false_value_key_list)

        else:
            # 当前处理人类型非全部处理
            destination_state, msg = WorkflowStateService.get_workflow_state_by_id(destination_state_id)
            if not destination_state:
                return False, msg
            # 获取目标状态的信息
            flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id, ticket_id,
                                                                           ticket_req_dict=request_data_dict)
            if not flag:
                return False, participant_info
            destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
            destination_participant = participant_info.get('destination_participant', '')
            multi_all_person_dict = {}
            if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL:
                for key in destination_participant.split(','):
                    multi_all_person_dict[key] = {}
            multi_all_person = json.dumps(multi_all_person_dict)
            # 如果开启了了记忆最后处理人，那么处理人为之前的处理人
            if destination_state.remember_last_man_enable and ticket_obj.participant_type_id != CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL:
                ## 获取此状态的最后处理人
                state_last_man, msg = cls.get_ticket_state_last_man(ticket_id, destination_state.id)
                if state_last_man:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                    destination_participant = state_last_man

        # 更新工单信息：基础字段及自定义字段， add_relation字段 需要下个处理人是部门、角色等的情况
        ticket_obj.state_id = destination_state_id
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.participant = destination_participant
        ticket_obj.multi_all_person = multi_all_person
        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END:
            ticket_obj.is_end = True
        if req_transition_obj.attribute_type_id == CONSTANT_SERVICE.TRANSITION_ATTRIBUTE_TYPE_REFUSE:
            # 如果操作为拒绝操作，则工单状态为被拒绝，否则更新为否
            ticket_obj.is_rejected = True
        else:
            ticket_obj.is_rejected = False
        ticket_obj.save()
        # 更新工单信息：基础字段及自定义字段， add_relation字段 需要考虑下个处理人是部门、角色等的情况
        add_relation, msg = cls.get_ticket_dest_relation(destination_participant_type_id, destination_participant)
        if add_relation:
            new_relation, msg = cls.add_ticket_relation(ticket_id, add_relation)  # 更新关系人信息

        # 只更新需要更新的字段
        update_field_dict = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                update_field_dict[key] = value

        update_ticket_custom_field_result, msg = cls.update_ticket_field_value(ticket_id, update_field_dict)
        # 更新工单流转记录，执行必要的脚本，通知消息
        ticket_all_data, msg = cls.get_ticket_all_field_value(ticket_id)
        for key, value in ticket_all_data.items():
            if type(value) not in [int, str, bool, float]:
                ticket_all_data[key] = str(ticket_all_data[key])
        if not by_task:
            # 脚本执行完自动触发的流转，因为在run_flow_task已经有记录操作日志，所以此次不再记录
            cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=transition_id, suggestion=suggestion,
                                     participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, participant=username,
                                     state_id=source_ticket_state_id, creator=username, ticket_data=json.dumps(ticket_all_data)))

        # 通知消息
        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')

        # 定时器逻辑
        cls.handle_timer_transition(ticket_id, destination_state_id)

        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END and ticket_obj.parent_ticket_id and ticket_obj.parent_ticket_state_id:
            # 如果存在父工单，判断是否该父工单的下属子工单都已经结束状态，如果都是结束状态则自动流转父工单到下个状态
            other_sub_ticket_queryset = TicketRecord.objects.filter(parent_ticket_id=ticket_obj.parent_ticket_id, parent_ticket_state_id=ticket_obj.parent_ticket_state_id,
                                                                    is_deleted=0).all()
            # 所有子工单使用相同的工作流,所以state都一样，检测是否都是ticket_obj.state_id即可判断是否都是结束状态
            other_sub_ticket_state_id_list = [other_sub_ticket.state_id for other_sub_ticket in other_sub_ticket_queryset]
            if set(other_sub_ticket_state_id_list) == set([ticket_obj.state_id]):
                parent_ticket_obj = TicketRecord.objects.filter(id=ticket_obj.parent_ticket_id, is_deleted=0).first()
                parent_ticket_state_id = parent_ticket_obj.state_id
                parent_ticket_transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(parent_ticket_state_id)
                # 含有子工单的工单状态只支持单路径流转到下个状态
                parent_ticket_transition_id = parent_ticket_transition_queryset[0].id
                cls.handle_ticket(parent_ticket_obj.id, dict(transition_id=parent_ticket_transition_id,
                                                             username='loonrobot', suggestion='所有子工单处理完毕，自动流转'))
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            from tasks import run_flow_task  # 放在文件开头会存在循环引用
            run_flow_task.apply_async(args=[ticket_id, destination_participant, destination_state_id], queue='loonflow')

        # 如果下个状态是hook，开始触发hook
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_HOOK:
            from tasks import flow_hook_task  # 放在文件开头会存在循环引用
            flow_hook_task.apply_async(args=[ticket_id], queue='loonflow')

        return True, ''

    @classmethod
    @auto_log
    def add_ticket_relation(cls, ticket_id, user_str):
        """
        新增工单关系人
        :param ticket_id:
        :param user_str: 逗号隔开的
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()

        new_relation_set = set(ticket_obj.relation.split(',') + user_str.split(','))  # 去重， 但是可能存在空元素
        new_relation_list = [new_relation0 for new_relation0 in new_relation_set if new_relation0]  # 去掉空元素
        new_relation = ','.join(new_relation_list)  # 去重
        ticket_obj.relation = new_relation
        ticket_obj.save()
        return new_relation, ''

    @classmethod
    @auto_log
    def get_ticket_dest_relation(cls, destination_participant_type_id, destination_participant):
        """
        获取目标处理人相应的工单关系人
        :param destination_participant_type_id:
        :param destination_participant:
        :return:
        """
        if destination_participant_type_id in (CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI):
            add_relation = destination_participant
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            username_list, msg = AccountBaseService.get_dept_username_list(int(destination_participant))
            add_relation = ','.join(username_list)
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            username_list, msg = AccountBaseService.get_role_username_list(int(destination_participant))
            add_relation = ','.join(username_list)
        else:
            add_relation = ''
        return add_relation, ''

    @classmethod
    @auto_log
    def get_ticket_flow_log(cls, ticket_id, username, per_page=10, page=1):
        """
        获取工单流转记录
        :param ticket_id:
        :param username:
        :param per_page:
        :param page:
        :return:
        """
        ticket_flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, is_deleted=0).all().order_by('-id')
        paginator = Paginator(ticket_flow_log_queryset, per_page)

        try:
            ticket_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            ticket_result_paginator = paginator.page(paginator.num_pages)

        ticket_flow_log_restful_list = []
        for ticket_flow_log in ticket_result_paginator.object_list:
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_flow_log.state_id)
            if ticket_flow_log.transition_id:
                transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(ticket_flow_log.transition_id)
                transition_name = transition_obj.name
                attribute_type_id = transition_obj.attribute_type_id
            else:
                # 考虑到人工干预修改工单状态， transition_id为0
                if ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER:
                    transition_name = '转交操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE:
                    transition_name = '加签操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END:
                    transition_name = '加签完成操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT:
                    transition_name = '接单操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_COMMENT:
                    transition_name = '新增评论'
                else:
                    transition_name = '未知操作'
                attribute_type_id = CONSTANT_SERVICE.TRANSITION_ATTRIBUTE_TYPE_OTHER

            state_info_dict = dict(state_id=state_obj.id, state_name=state_obj.name)
            transition_info_dict = dict(transition_id=ticket_flow_log.transition_id, transition_name=transition_name,
                                        attribute_type_id=attribute_type_id)
            participant_info = dict(participant_type_id=ticket_flow_log.participant_type_id,
                                    participant=ticket_flow_log.participant,
                                    participant_alias=ticket_flow_log.participant,
                                    participant_email='', participant_phone=''
                                    )
            if ticket_flow_log.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
                participant_query_obj, msg = AccountBaseService.get_user_by_username(ticket_flow_log.participant)
                if participant_query_obj:
                    participant_info.update(participant_alias=participant_query_obj.alias,
                                            participant_email=participant_query_obj.email,
                                            participant_phone=participant_query_obj.phone
                                            )

            ticket_flow_log_restful_list.append(dict(id=ticket_flow_log.id, ticket_id=ticket_id, state=state_info_dict,
                                                     transition=transition_info_dict,
                                                     intervene_type_id=ticket_flow_log.intervene_type_id,
                                                     participant_type_id=ticket_flow_log.participant_type_id,
                                                     participant=ticket_flow_log.participant,
                                                     participant_info=participant_info,
                                                     suggestion=ticket_flow_log.suggestion,
                                                     gmt_created=str(ticket_flow_log.gmt_created)[:19]
                                                     ))

        return ticket_flow_log_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def get_ticket_flow_step(cls, ticket_id, username):
        """
        工单的流转步骤，路径。直线流转, 步骤不会很多(因为同个状态只显示一次，隐藏的状态只有当前处于才显示，否则不显示)，默认先不分页
        :param ticket_id:
        :param username:
        :return:
        """
        # 先获取工单对应工作流的信息
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        workflow_id = ticket_obj.workflow_id
        state_objs, msg = WorkflowStateService.get_workflow_states(workflow_id)
        ticket_flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, is_deleted=0).all()

        state_step_dict_list = []
        for state_obj in state_objs:
            if state_obj.id == ticket_obj.state_id or (not state_obj.is_hidden):
                ticket_state_step_dict = dict(state_id=state_obj.id, state_name=state_obj.name, order_id=state_obj.order_id)
                state_flow_log_list = []
                for ticket_flow_log in ticket_flow_log_queryset:
                    if ticket_flow_log.state_id == state_obj.id:
                        # 此部分和get_ticket_flow_log代码冗余，后续会简化下
                        if ticket_flow_log.transition_id:
                            transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(ticket_flow_log.transition_id)
                            transition_name = transition_obj.name
                        else:
                            if ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER:
                                transition_name = '转交操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE:
                                transition_name = '加签操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END:
                                transition_name = '加签完成操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT:
                                transition_name = '接单操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_COMMENT:
                                transition_name = '新增评论'
                            else:
                                transition_name = '未知操作'
                        participant_info = dict(participant_type_id=ticket_flow_log.participant_type_id,
                                                participant=ticket_flow_log.participant,
                                                participant_alias=ticket_flow_log.participant,
                                                participant_email='', participant_phone=''
                                                )
                        if ticket_flow_log.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
                            participant_query_obj, msg = AccountBaseService.get_user_by_username(
                                ticket_flow_log.participant)
                            if participant_query_obj:
                                participant_info.update(participant_alias=participant_query_obj.alias,
                                                        participant_email=participant_query_obj.email,
                                                        participant_phone=participant_query_obj.phone
                                                        )

                        state_flow_log_list.append(dict(id=ticket_flow_log.id, transition=dict(transition_name=transition_name, transition_id=ticket_flow_log.transition_id), participant_type_id=ticket_flow_log.participant_type_id,
                                                        participant=ticket_flow_log.participant, participant_info=participant_info, intervene_type_id=ticket_flow_log.intervene_type_id, suggestion=ticket_flow_log.suggestion, state_id=ticket_flow_log.state_id, gmt_created=str(ticket_flow_log.gmt_created)[:19]))
                ticket_state_step_dict['state_flow_log_list'] = state_flow_log_list
                state_step_dict_list.append(ticket_state_step_dict)
        return state_step_dict_list, ''

    @classmethod
    @auto_log
    def update_ticket_state(cls, ticket_id, state_id, username):
        """
        更新状态id,暂时只变更工单状态及工单当前处理人，不考虑目标状态状态处理人类型为脚本、变量、工单字段等等逻辑
        :param ticket_id:
        :param state_id:
        :param username:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在'
        source_state_id = ticket_obj.state_id
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(state_id)
        if not state_obj:
            return False, msg
        if state_obj.workflow_id == ticket_obj.workflow_id:
            # 获取目标状态的处理人信息
            flag, destination_participant_info = cls.get_ticket_state_participant_info(state_id, ticket_id=ticket_id)
            ticket_obj.state_id = state_id
            ticket_obj.participant_type_id = destination_participant_info.get('destination_participant_type_id', 0)
            ticket_obj.participant = destination_participant_info.get('destination_participant', '')
            ticket_obj.save()

            # 新增流转记录
            ## 获取工单所有字段的值
            all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
            # date等格式需要转换为str
            for key, value in all_ticket_data.items():
                if type(value) not in [int, str, bool, float]:
                    all_ticket_data[key] = str(all_ticket_data[key])

            all_ticket_data_json = json.dumps(all_ticket_data)

            cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=0, suggestion='强制修改工单状态', participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                         participant=username, state_id=source_state_id, ticket_data=all_ticket_data_json))

            # 如果目标状态是脚本处理中，需要触发脚本处理
            if ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
                from tasks import run_flow_task  # 放在文件开头会存在循环引用
                run_flow_task.apply_async(args=[ticket_id, ticket_obj.participant, ticket_obj.state_id],
                                          queue='loonflow')

            return True, '修改工单状态成功'

    @classmethod
    @auto_log
    def get_tickets_states_by_ticket_id_list(cls, ticket_id_list, username):
        """
        批量获取工单状态
        :param ticket_id_list:
        :param username:
        :return:
        """
        ticket_queryset = TicketRecord.objects.filter(id__in=ticket_id_list).all()
        ticket_state_id_dict = {}
        for ticket in ticket_queryset:
            ticket_state_id_dict[ticket.id] = ticket.state_id
        ticket_state_id_list = [ticket_obj.state_id for ticket_obj in ticket_queryset]
        state_info_dict, msg = WorkflowStateService.get_states_info_by_state_id_list(ticket_state_id_list)
        new_result = {}
        for key, value in ticket_state_id_dict.items():
            new_result[key] = dict(state_id=value, state_name=state_info_dict[value])
        return new_result, msg

    @classmethod
    @auto_log
    def accept_ticket(cls, ticket_id, username):
        """
        接单
        :param ticket_id:
        :param username:
        :return:
        """
        # 先判断是否有处理权限
        permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not permission:
            return False, msg
        if msg['need_accept']:
            # 更新工单关系人
            cls.add_ticket_relation(ticket_id, username)

            ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
            ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            ticket_obj.participant = username
            ticket_obj.save()
            # 记录处理日志

            all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
            # date等格式需要转换为str
            for key, value in all_ticket_data.items():
                if type(value) not in [int, str, bool, float]:
                    all_ticket_data[key] = str(all_ticket_data[key])

            all_ticket_data_json = json.dumps(all_ticket_data)

            ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion='接单处理', participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                        intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT,
                                        participant=username, state_id=ticket_obj.state_id, creator=username,
                                        ticket_data=all_ticket_data_json)
            cls.add_ticket_flow_log(ticket_flow_log_dict)
            return True, ''
        else:
            return False, '工单当前实际处理人只有一人，无需先接单'

    @classmethod
    @auto_log
    def deliver_ticket(cls, ticket_id, username, target_username, suggestion):
        """
        转交工单
        :param ticket_id:
        :param username: 操作人
        :param target_username: 转交目标人
        :param suggestion: 处理意见
        :return:
        """
        permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not permission:
            return False, msg

        cls.add_ticket_relation(ticket_id, target_username)  # 更新工单关系人
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.save()
        # 记录处理日志
        all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)

        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket(cls, ticket_id, username, target_username, suggestion):
        """
        加签工单
        :param ticket_id:
        :param username:
        :param target_username: 加签目标人
        :param suggestion: 处理意见
        :return:
        """
        permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not permission:
            return False, msg

        cls.add_ticket_relation(ticket_id, target_username)  # 更新工单关系人
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.in_add_node = True
        ticket_obj.add_node_man = username
        ticket_obj.save()
        # 记录处理日志
        all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket_end(cls, ticket_id, username, suggestion):
        """
        加签工单完成
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not permission:
            return False, msg
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = ticket_obj.add_node_man
        ticket_obj.in_add_node = False
        ticket_obj.add_node_man = ''
        ticket_obj.save()
        # 记录处理日志
        all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)

        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def handle_timer_transition(cls, ticket_id, destination_state_id):
        """
        定时器处理
        :param ticket_id:
        :param destination_state_id:
        :return:
        """
        # 定时器处理逻辑，如果新的状态所属transition有配置定时器，那么创建一个定时器流转的任务
        destination_transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(destination_state_id)
        if destination_transition_queryset:
            for destination_transition in destination_transition_queryset:
                if destination_transition.transition_type_id == CONSTANT_SERVICE.TRANSITION_TYPE_TIMER:
                    from tasks import timer_transition
                    timer_transition.apply_async(args=[ticket_id, destination_state_id, datetime.datetime.now(), destination_transition.id], countdown=destination_transition.timer, queue='loonflow')
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_all_field_value(cls, ticket_id):
        """
        工单所有字段的值
        :param ticket:
        :return:
        """
        # 工单基础字段、工单自定义字段
        ticket_obj = TicketRecord.objects.filter(id=ticket_id).first()
        if not ticket_obj:
            return False, '工单已被删除或者不存在'
        # 获取工单基础表中的字段中的字段信息
        field_info_dict = ticket_obj.get_to_dict()
        # 获取自定义字段的值
        ## 获取工单自定义字段
        ticket_custom_field_list, msg = WorkflowCustomFieldService.get_workflow_custom_field_name_list(ticket_obj.workflow_id)
        if ticket_custom_field_list is False:
            return False, msg

        for field_key in ticket_custom_field_list:
            field_value, msg = cls.get_ticket_field_value(ticket_id, field_key)
            if (field_value is False) and msg:
                # 此处hack了.msg不为空说明真的报错了,用于区分字段的值就是布尔否的情况
                return False, msg
            field_info_dict[field_key] = field_value
        return field_info_dict, ''

    @classmethod
    @auto_log
    def retry_ticket_script(cls, ticket_id, username):
        """
        重新执行工单脚本，或重新触发hook
        :param ticket_id:
        :return:
        """
        # 判断工单表记录中最后一次脚本是否执行失败了，即script_run_last_result的值
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, 'Ticket is not existed or has been deleted'
        # if ticket_obj.participant_type_id is not CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
        #     return False, "The ticket's participant_type is not robot, do not allow retry"

        if ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            # 先重置上次执行结果
            ticket_obj.script_run_last_result = True
            ticket_obj.save()
            from tasks import run_flow_task  # 放在文件开头会存在循环引用问题
            run_flow_task.apply_async(args=[ticket_id, ticket_obj.participant, ticket_obj.state_id, '{}_retry'.format(username)], queue='loonflow')
        elif ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_HOOK:
            ticket_obj.script_run_last_result = True
            ticket_obj.save()
            from tasks import flow_hook_task
            flow_hook_task.apply_async(args=[ticket_id], queue='loonflow')
        else:
            return False, "The ticket's participant_type is not robot or hook, do not allow retry"


    @classmethod
    @auto_log
    def get_ticket_state_last_man(cls, ticket_id, state_id):
        """
        获取工单状态最后一次的处理人
        :param ticket_id:
        :param state_id:
        :return:
        """
        flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, state_id=state_id, is_deleted=0).order_by('-id')
        if flow_log_queryset:
            last_flow_log = flow_log_queryset[0]
            if last_flow_log.participant_type_id == 1:
                # 为个人时才生效
                return last_flow_log.participant, ''
            else:
                return '', 'handle_man is not personal'
        return '', 'the state has not handle man before'

    @classmethod
    @auto_log
    def get_ticket_count_by_args(cls, workflow_id=0, username='', period=0):
        """
        获取工单的个数
        :param workflow_id:
        :param username:
        :param period: 周期， 单位小时,即多少小时内
        :return:
        """
        query_params = Q(is_deleted=False)
        if workflow_id:
            query_params &= Q(workflow_id=workflow_id)
        if username:
            query_params &= Q(creator=username)
        if period:
            query_params &= Q(creator=username)
            datetime_now = datetime.datetime.now()
            datetime_start = datetime_now - datetime.timedelta(hours=period)
            query_params &= Q(gmt_created__gte=datetime_start)
        count_result = TicketRecord.objects.filter(query_params).count()
        return count_result, ''

    @classmethod
    @auto_log
    def get_ticket_state_participant_info(cls, state_id, ticket_id=0, ticket_req_dict={}):
        """
        获取工单状态实际的新处理人
        :param state_id:
        :param ticket_id: 不传ticket_id 则为新建工单
        :param ticket_req_dict:
        :return:
        """
        if ticket_id:
            ticket_obj, msg = cls.get_ticket_by_id(ticket_id)
            if not ticket_obj:
                return False, msg
            parent_ticket_id = ticket_obj.parent_ticket_id
            creator = ticket_obj.creator
            multi_all_person = json.loads(ticket_obj.multi_all_person)
        else:
            parent_ticket_id = ticket_req_dict.get('parent_ticket_id')
            creator = ticket_req_dict.get('username')
            multi_all_person = "{}"

        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(state_id)
        participant_type_id, participant = state_obj.participant_type_id, state_obj.participant
        destination_participant_type_id, destination_participant = participant_type_id, participant

        if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            if not ticket_id:
                # ticket_id 不存在，则为新建工单，从请求的数据中获取
                destination_participant = ticket_req_dict.get(participant, '')
            else:
                # 工单存在，先判断是否有修改此字段的权限，如果有且字段值有提供，则取提交的值
                flag, field_info = cls.get_state_field_info(ticket_obj.state_id)
                update_field_list = field_info.get('update_field_list')
                if participant in update_field_list and ticket_req_dict.get(participant):
                    # 请求数据中包含需要的字段则从请求数据中获取
                    destination_participant = ticket_req_dict.get(participant)
                else:
                    # 处理工单时未提供字段的值,则从工单当前字段值中获取
                    destination_participant, msg = cls.get_ticket_field_value(ticket_id, participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(parent_ticket_id, participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = creator
            elif participant == 'creator_tl':
                # 获取用户的tl或审批人(优先审批人)
                approver, msg = AccountBaseService.get_user_dept_approver(creator)
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                destination_participant = approver

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_HOOK:
            destination_participant = '***'  # 敏感数据，不保存工单基础表中

        if destination_participant_type_id in (CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI, CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT, CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE) \
                and state_obj.distribute_type_id in (CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_RANDOM, CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_ALL):
            # 处理人为角色，部门，或者角色都可能是为多个人，需要根据状态的分配方式计算实际的处理人
            if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
                destination_participant_list = destination_participant.split(',')
            elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
                destination_participant_list, msg = AccountBaseService.get_dept_username_list(int(destination_participant))
            elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
                destination_participant_list, msg = AccountBaseService.get_role_username_list(int(destination_participant))

            if state_obj.distribute_type_id == CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_RANDOM:
                # 如果是随机处理,则随机设置处理人
                destination_participant = random.sample(destination_participant_list, 1)[0]
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if state_obj.distribute_type_id == CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_ALL:
                # destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL  # 不新增类型，直接用原来的类型。这样方便待办查询
                multi_all_person_dict = {}
                for destination_participant_0 in destination_participant_list:
                    multi_all_person_dict[destination_participant_0] = {}
                multi_all_person = json.dumps(multi_all_person_dict)

        return True, dict(destination_participant_type_id=destination_participant_type_id, destination_participant=destination_participant,
                          multi_all_person=multi_all_person)

    @classmethod
    @auto_log
    def get_state_field_info(cls, state_id):
        """
        获取状态字段信息
        :param state_id:
        :return:
        """
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(state_id)
        if not state_obj:
            return False, msg

        state_field_dict = json.loads(state_obj.state_field_str)
        require_field_list, update_field_list = [], []
        for key, value in state_field_dict.items():
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
                update_field_list.append(key)
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_OPTIONAL:
                update_field_list.append(key)
        return True, dict(require_field_list=require_field_list, update_field_list=update_field_list)

    @classmethod
    @auto_log
    def get_next_state_id_by_transition_and_ticket_info(cls, ticket_id=0, ticket_req_dict={}):
        """
        获取工单的下个状态id,需要考虑条件流转的情况
        :param ticket_id:
        :param ticket_req_dict:
        :return:
        """
        transition_id = ticket_req_dict.get('transition_id', 0)
        workflow_id = ticket_req_dict.get('workflow_id', 0)
        if not transition_id:
            return False, 'transition_id can not be None'
        if not ticket_id:
            # 新建工单的情况, 获取初始状态 作为原状态
            # 获取transition_id对应的下个状态的信息:
            # 新建工单获取工单的初始状态
            if not workflow_id:
                return False, 'new ticket need arg workflow_id'
            start_state, msg = WorkflowStateService.get_workflow_start_state(workflow_id)
            if not start_state:
                return False, msg
            source_state_id = start_state.id
        else:
            # 已经存在的工单，直接获取工单当前状态
            ticket_obj, msg = cls.get_ticket_by_id(ticket_id)
            source_state_id = ticket_obj.state_id

        transition_queryset, msg = WorkflowTransitionService.get_transition_by_args(dict(source_state_id=source_state_id, id=transition_id))
        if not transition_queryset:
            return False, 'transition_id is invalid'

        transition_obj = transition_queryset[0]
        condition_expression = transition_obj.condition_expression
        destination_state_id = transition_obj.destination_state_id

        if condition_expression and json.loads(condition_expression):
            # 存在条件表达式，需要根据表达式计算下个状态
            condition_expression_list = json.loads(condition_expression)
            ticket_all_value_dict = {}
            if ticket_id:
                # 获取工单所有字段的值
                ticket_all_value_dict, msg = cls.get_ticket_all_field_value(ticket_id)
            # 更新当前更新的字段的值
            ticket_all_value_dict_copy = copy.deepcopy(ticket_all_value_dict)
            ticket_all_value_dict_copy.update(ticket_req_dict)
            for key, value in ticket_all_value_dict_copy.items():
                if isinstance(ticket_all_value_dict_copy[key], str):
                    ticket_all_value_dict_copy[key] = "'''" + ticket_all_value_dict_copy[key] + "'''"

            for condition_expression0 in condition_expression_list:
                expression = condition_expression0.get('expression')
                expression_format = expression.format(**ticket_all_value_dict_copy)
                import datetime, time  # 用于支持条件表达式中对时间的操作
                if eval(expression_format):
                    destination_state_id = condition_expression0.get('target_state_id')
                    break

        return True, dict(destination_state_id=destination_state_id)

    @classmethod
    @auto_log
    def add_comment(cls, ticket_id=0, username='', suggestion=''):
        """
        添加评论
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        if not (ticket_id and username):
            return False, 'ticket_id and username should not be null'

        all_ticket_data, msg = cls.get_ticket_all_field_value(ticket_id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)
        new_flow_log = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                            participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                            participant=username, state_id=all_ticket_data.get('state_id'), intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_COMMENT,
                            ticket_data=all_ticket_data_json, creator=username)

        flag ,msg = cls.add_ticket_flow_log(new_flow_log)
        if flag is False:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def hook_call_back(cls, ticket_id, app_name, request_data_dict):
        """
        hook回调
        :param ticket_id:
        :param app_name:
        :param request_data_dict:
        :return:
        """
        # 校验请求app_name是否有hook回调该工单权限
        flag, msg = AccountBaseService().app_ticket_permission_check(app_name, ticket_id)
        if not flag:
            return False, msg
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()

        # 检查工单处理人类型为hook中
        if ticket_obj.participant_type_id != CONSTANT_SERVICE.PARTICIPANT_TYPE_HOOK:
            return False, '工单当前处理人类型非hook，不执行回调操作'

        result = request_data_dict.get('result', True)
        msg = request_data_dict.get('msg', '')
        field_value = request_data_dict.get('field_value', {})  # 用于更新字段

        if result is False:
            # hook执行失败了，记录失败状态.以便允许下次再执行
            cls.update_ticket_field_value({'script_run_last_result': False})
            return True, ''

        state_id = ticket_obj.state_id
        transition_queryset, msg = WorkflowTransitionService().get_state_transition_queryset(state_id)
        transition_id = transition_queryset[0]  # hook状态只支持一个流转

        new_request_dict = field_value

        new_request_dict.update({'transition_id': transition_id, 'suggestion': msg, 'username': 'loonrobot'})

        # 执行流转
        flag, msg = cls.handle_ticket(ticket_id, new_request_dict, by_timer=False, by_task=False)
        if not flag:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_participant_info(cls, ticket_id):
        """
        获取工单当前详细参与人信息
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        from apps.account.models import LoonUser
        participant_username_list, participant_info_list = [], []

        if ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            participant_username_list = [ticket_obj.participant]
        elif ticket_obj.participant_type_id in (
        CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI, CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI_ALL):
            participant_username_list = ticket_obj.participant.split(',')
        elif ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            participant_username_list, msg = AccountBaseService.get_role_username_list(ticket_obj.participant)
        elif ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            participant_username_list, msg = AccountBaseService.get_dept_username_list(ticket_obj.participant)
        if participant_username_list:
            participant_queryset = LoonUser.objects.filter(username__in=participant_username_list, is_deleted=0)
            for participant_0 in participant_queryset:
                participant_info_list.append(dict(username=participant_0.username, alias=participant_0.alias,
                                                  phone=participant_0.phone, email=participant_0.email))
        return True, dict(participant_username_list=participant_username_list, participant_info_list=participant_info_list)
