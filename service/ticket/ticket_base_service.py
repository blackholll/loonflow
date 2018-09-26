import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from apps.ticket.models import TicketRecord, TicketCustomField, TicketFlowLog
from apps.workflow.models import CustomField
from service.account.account_base_service import AccountBaseService
from service.base_service import BaseService
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
    def get_ticket_list(cls, sn='', title='', username='', create_start='', create_end='',workflow_ids='', state_ids='', category='', reverse=1, per_page=10, page=1):
        """
        工单列表
        :param sn:
        :param title:
        :param username:
        :param create_start: 创建时间起
        :param create_end: 创建时间止
        :param workflow_ids: 工作流id,str,逗号隔开
        :param state_ids: 状态ids,str,逗号隔开
        :param category: 查询类别(创建的，待办的，关联的:包括创建的、处理过的、曾经需要处理但是没有处理的)
        :param reverse: 按照创建时间倒序
        :param per_page:
        :param page:
        :return:
        """
        category_list = ['all', 'owner', 'duty', 'relation']
        if category not in category_list:
            return False, '查询类别错误'

        query_params = Q(is_deleted=False)
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
            ticket_query_set1 = TicketRecord.objects.filter(query_params).extra(where=['FIND_IN_SET("{}", participant)'.format(username), 'participant_type_id={}'.format(CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI)])
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
                creator_info = dict(username=creator_obj.username, alias=creator_obj.alias,
                                    is_active=creator_obj.is_active, email=creator_obj.email, phone=creator_obj.phone)
            else:
                creator_info = dict(username=creator_obj.username, alias='', is_active=False, email='', phone='')
            ticket_result_restful_list.append(dict(id=ticket_result_object.id,
                                                   title=ticket_result_object.title,
                                                   workflow=workflow_info_dict,
                                                   sn=ticket_result_object.sn,
                                                   state=dict(state_id=ticket_result_object.state_id, state_name=state_name),
                                                   parent_ticket_id=ticket_result_object.parent_ticket_id,
                                                   parent_ticket_state_id=ticket_result_object.parent_ticket_state_id,
                                                   participant_info=participant_info,
                                                   creator=ticket_result_object.creator,
                                                   creator_info=creator_info,
                                                   gmt_created=str(ticket_result_object.gmt_created)[:19],
                                                   gmt_modified=str(ticket_result_object.gmt_modified)[:19],
                                                   ))
        return ticket_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def new_ticket(cls, request_data_dict):
        """
        新建工单
        :param request_data_dict:
        :return:
        """
        transition_id = request_data_dict.get('transition_id')
        username = request_data_dict.get('username')
        workflow_id = request_data_dict.get('workflow_id')
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
        state_field_dict = json.loads(start_state.state_field_str)
        require_field_list, update_field_list = [], []
        for key, value in state_field_dict.items():
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
                update_field_list.append(key)
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_OPTIONAL:
                update_field_list.append(key)

        # 校验是否所有必填字段都有提供，如果transition_id对应设置为不校验必填则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))
        # 获取transition_id对应的下个状态的信息:
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(start_state.id)
        if transition_queryset is False:
            return False, msg
        allow_transition_id_list = [transition.id for transition in transition_queryset]
        if transition_id not in allow_transition_id_list:
            return False, 'transition_id不合法'

        for transition_obj in transition_queryset:
            if transition_obj.id == transition_id:
                destination_state_id = transition_obj.destination_state_id
                break

        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(destination_state_id)
        if not destination_state:
            return False, msg
        # 获取目标状态的信息
        destination_participant_type_id = destination_state.participant_type_id
        destination_participant = destination_state.participant

        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            # 获取工单字段的值, 因为是新建工单,记录还没实际生成，所以从请求的数据中获取
            field_value = request_data_dict.get(destination_participant, '')
            if not field_value:
                return False, '请求数据中无此字段的值,或值为空:{}'.format(destination_participant)
            destination_participant = field_value
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(field_value.split(',')) > 1:
                # 多人的情况
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI

        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(parent_ticket_id, destination_participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD

        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if destination_participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = username
            elif destination_participant == 'creator_tl':
                # 获取用户的tl或审批人(优先审批人)
                approver, msg = AccountBaseService.get_user_dept_approver(username)
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                destination_participant = approver

        # 生成流水号
        ticket_sn, msg = cls.gen_ticket_sn()
        if not ticket_sn:
            return False, msg
        # 新增工单基础表数据
        new_ticket_obj = TicketRecord(sn=ticket_sn, title=request_data_dict.get('title', ''), workflow_id=workflow_id,
                                      state_id=destination_state_id, parent_ticket_id=parent_ticket_id, parent_ticket_state_id=parent_ticket_state_id, participant=destination_participant,
                                      participant_type_id=destination_participant_type_id, relation=username, creator=username)
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
        new_ticket_flow_log_dict = dict(ticket_id=new_ticket_obj.id, transition_id=transition_id, suggestion=suggestion,
                                        participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, participant=username,
                                        state_id=start_state.id)
        add_ticket_flow_log_result, msg = cls.add_ticket_flow_log(new_ticket_flow_log_dict)
        if not add_ticket_flow_log_result:
            return False, msg
        # 如果下个状态为脚本处理，则开始执行脚本
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            from tasks import run_flow_task # 放在文件开头会存在循环引用
            run_flow_task.apply_async(args=[new_ticket_obj.id, destination_participant, destination_state_id], queue='loonflow')

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
    def gen_ticket_sn(cls):
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
        return 'loonflow_%04d%02d%02d%04d' % (now_day.year, now_day.month, now_day.day, new_ticket_day_count), ''

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
                else:
                    if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'], ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, char_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, int_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, float_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, bool_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, date_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, datetime_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, radio_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, checkbox_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, multi_select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, text_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, username_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, multi_username_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                        new_ticket_custom_field_record = TicketCustomField(name= format_custom_field_dict[key]['field_name'],ticket_id=ticket_id, field_key=key, field_type_id=field_type_id, char_value=update_dict.get(key))
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
        field_list, msg = cls.get_ticket_base_filed_list(ticket_id)

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
            creator_info = dict(username=creator_obj.username, alias=creator_obj.alias,
                                is_active=creator_obj.is_active, email=creator_obj.email, phone=creator_obj.phone)
        else:
            creator_info = dict(username=creator_obj.username, alias='', is_active=False, email='', phone='')

        return dict(id=ticket_obj.id, sn=ticket_obj.sn, title=ticket_obj.title, state_id=ticket_obj.state_id, parent_ticket_id=ticket_obj.parent_ticket_id,
                    participant=ticket_obj.participant, participant_type_id=ticket_obj.participant_type_id, workflow_id=ticket_obj.workflow_id,
                    creator=ticket_obj.creator, gmt_created=str(ticket_obj.gmt_created)[:19], gmt_modified=str(ticket_obj.gmt_modified)[:19],
                    field_list=new_field_list, creator_info=creator_info), ''

    @classmethod
    @auto_log
    def get_ticket_base_filed_list(cls, ticket_id):
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

        field_list.append(dict(field_key='sn', field_name=u'流水号', field_value=ticket_obj.sn, order_id=0, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的流水号', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='title', field_name=u'标题', field_value=ticket_obj.title, order_id=20, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的标题', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='state_id', field_name=u'状态id', field_value=ticket_obj.state_id, order_id=40, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前状态的id', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='participant_info.participant_name', field_name=u'当前处理人', field_value=participant_info_dict['participant_name'], order_id=50, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的当前处理人', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='participant_info.participant_alias', field_name=u'当前处理人', field_value=participant_info_dict['participant_alias'], order_id=55, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前处理人(alias)', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))

        field_list.append(dict(field_key='workflow.workflow_name', field_name=u'工作流名称', field_value=workflow_name, order_id=60, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单所属工作流的名称', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))

        field_list.append(dict(field_key='creator', field_name=u'创建人', field_value=ticket_obj.creator, order_id=80, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的创建人', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='gmt_created', field_name=u'创建时间', field_value=str(ticket_obj.gmt_created)[:19], order_id=100, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的创建时间', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='gmt_modified', field_name=u'更新时间', field_value=str(ticket_obj.gmt_modified)[:19], order_id=120, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单的更新时间', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))
        field_list.append(dict(field_key='state.state_name', field_name=u'状态名', field_value=state_name, order_id=41, field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR, field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO, description='工单当前状态的名称', field_choice={}, boolean_field_display={}, default_value=None, field_template=''))

        # 工单所有自定义字段
        custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(ticket_obj.workflow_id)
        for key, value in custom_field_dict.items():
            field_type_id = value['field_type_id']
            ticket_custom_field_obj = TicketCustomField.objects.filter(ticket_id=ticket_id,field_key=key, is_deleted=0).first()
            if not ticket_custom_field_obj:
                field_value = None  # 尚未赋值的情况
            else:
                # 根据字段类型 获取对应列的值
                if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                    field_value = ticket_custom_field_obj.char_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                    field_value = ticket_custom_field_obj.int_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                    field_value = ticket_custom_field_obj.float_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                    field_value = ticket_custom_field_obj.bool_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                    field_value = str(ticket_custom_field_obj.date_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                    field_value = str(ticket_custom_field_obj.datetime_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                    field_value = ticket_custom_field_obj.radio_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                    field_value = ticket_custom_field_obj.checkbox_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                    field_value = ticket_custom_field_obj.select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                    field_value = ticket_custom_field_obj.multi_select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                    field_value = ticket_custom_field_obj.text_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                    field_value = ticket_custom_field_obj.username_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                    field_value = ticket_custom_field_obj.multi_username_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_ATTACHMENT:
                    field_value = ticket_custom_field_obj.char_value

            field_list.append(dict(field_key=key, field_name=custom_field_dict[key]['field_name'], field_value=field_value, order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO,
                                   default_value=custom_field_dict[key]['default_value'],
                                   description=custom_field_dict[key]['description'],
                                   field_template=custom_field_dict[key]['field_template'],
                                   boolean_field_display=json.loads(custom_field_dict[key]['boolean_field_display']) if custom_field_dict[key]['boolean_field_display'] else {},  # 之前model允许为空了，为了兼容先这么写
                                   field_choice=json.loads(custom_field_dict[key]['field_choice']),

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
            participant_alias = participant_user_obj.alias
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
            participant_type_name = '多人'
            # 依次获取人员信息
            participant_name_list = participant_name.split(',')
            participant_alias_list = []
            for participant_name0 in participant_name_list:
                participant_user_obj, msg = AccountBaseService.get_user_by_username(participant_name0)
                participant_alias_list.append(participant_user_obj.alias)
            participant_alias = ','.join(participant_alias_list)
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
        # 工单基础表中不存在参与人为其他类型的情况
        return dict(participant=participant, participant_name=participant_name, participant_type_id=participant_type_id,
                    participant_type_name=participant_type_name, participant_alias=participant_alias), ''

    @classmethod
    @auto_log
    def ticket_handle_permission_check(cls, ticket_id, username):
        """
        处理权限校验: 获取当前状态是否需要处理， 该用户是否有权限处理
        :param ticket_id:
        :param username:
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
        participant_type_id = ticket_obj.participant_type_id
        participant = ticket_obj.participant

        current_participant_count = 1  # 当前处理人个数，用于当处理人大于1时 可能需要先接单再处理

        if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            if username != participant:
                return False, '非当前处理人，无权处理'
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
            if username not in participant.split(','):
                return False, '非当前处理人，无权处理'
            current_participant_count = len(participant.split(','))
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            dept_user_list, msg = AccountBaseService.get_dept_username_list(dept_id=int(participant))
            if username not in dept_user_list:
                return False, '非当前处理人，无权处理'
            current_participant_count = len(dept_user_list)

        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            role_user_list, msg = AccountBaseService.get_role_username_list(int(participant))
            if username not in role_user_list:
                return False, '非当前处理人，无权处理'
            current_participant_count = len(role_user_list)
        else:
            return False, '非当前处理人，无权处理'
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
            transition_dict_list = [dict(transition_id=0, transition_name='完成', field_require_check=False, is_accept=False, in_add_node=True)]
            return transition_dict_list, ''
        if msg['need_accept']:
            transition_dict_list = [dict(transition_id=0, transition_name='接单', field_require_check=False, is_accept=True, in_add_node=False)]
            return transition_dict_list, ''

        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(ticket_obj.state_id)
        transition_dict_list = []
        for transition in transition_queryset:
            transition_dict = dict(transition_id=transition.id, transition_name=transition.name, field_require_check=transition.field_require_check, is_accept=False, in_add_node=False)
            transition_dict_list.append(transition_dict)
        return transition_dict_list, ''

    @classmethod
    @auto_log
    def handle_ticket(cls, ticket_id, request_data_dict):
        """
        处理工单:校验必填参数,获取当前状态必填字段，更新工单基础字段，更新工单自定义字段， 更新工单流转记录，执行必要的脚本，通知消息
        此处逻辑和新建工单有较多重复，下个版本会拆出来
        :param ticket_id:
        :param request_data_dict:
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
        has_permission, msg = cls.ticket_handle_permission_check(ticket_id, username)
        if not has_permission:
            return False, msg
        if msg['need_accept']:
            return False, '需要先接单再处理'
        if msg['in_add_node']:
            return False, '工单当前处于加签中，只允许加签完成操作'

        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(ticket_obj.state_id)
        if not state_obj:
            return False, msg
        state_field_str = state_obj.state_field_str
        state_field_dict = json.loads(state_field_str)
        require_field_list, update_field_list = [], []
        update_field_dict = {}
        for key, value in state_field_dict.items():
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
            update_field_list.append(key)
            if request_data_dict.get(key):
                update_field_dict[key] = request_data_dict.get(key)

        # 校验是否所有必填字段都有提供，如果transition_id对应设置为不校验必填则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:

            request_field_arg_list = [key for key, value in request_data_dict.items() if (key not in ['workflow_id', 'suggestion', 'username'])]
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))

        # 获取transition_id对应的下个状态的信息:
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(ticket_obj.state_id)
        if transition_queryset is False:
            return False, msg
        allow_transition_id_list = [transition.id for transition in transition_queryset]
        if transition_id not in allow_transition_id_list:
            return False, 'transition_id不合法'

        for transition_obj in transition_queryset:
            if transition_obj.id == transition_id:
                destination_state_id = transition_obj.destination_state_id
                break

        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(destination_state_id)
        if not destination_state:
            return False, msg
        # 获取目标状态的信息
        destination_participant_type_id = destination_state.participant_type_id
        destination_participant = destination_state.participant
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            # 获取工单字段的值
            # 考虑到处理工单时 可能会编辑工单字段，所有优先从请求数据中获取，如果没有再去数据库中获取
            field_value = request_data_dict.get(destination_participant)
            if not field_value:
                field_value, msg = cls.get_ticket_field_value(ticket_id, destination_participant)
                if not field_value:
                    return False, msg
            destination_participant = field_value
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(field_value.split(',')) > 1:
                # 多人的情况
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(ticket_obj.parent_ticket_id, destination_participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD

        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if destination_participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = ticket_obj.creator
            elif destination_participant == 'creator_tl':
                # 获取用户的tl或审批人(优先审批人)
                approver, msg = AccountBaseService.get_user_dept_approver(ticket_obj.creator)
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                destination_participant = approver

        ticket_obj.state_id = destination_state_id
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.participant = destination_participant
        ticket_obj.save()
        # 更新工单信息：基础字段及自定义字段， add_relation字段 需要考虑下个处理人是部门、角色等的情况
        add_relation, msg = cls.get_ticket_dest_relation(destination_participant_type_id, destination_participant)
        if add_relation:
            new_relation, msg = cls.add_ticket_relation(ticket_id, add_relation)  # 更新关系人信息

        # 只更新需要更新的字段
        request_update_dict = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                request_update_dict[key] = value


        update_ticket_custom_field_result, msg = cls.update_ticket_field_value(ticket_id, update_field_dict)
        # 更新工单流转记录，执行必要的脚本，通知消息
        cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=transition_id, suggestion=suggestion,
                                     participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, participant=username,
                                     state_id=source_ticket_state_id, creator=username))

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

        # 通知消息
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
                else:
                    transition_name = '未知操作'

            state_info_dict = dict(state_id=state_obj.id, state_name=state_obj.name)
            transition_info_dict = dict(transition_id=ticket_flow_log.transition_id, transition_name=transition_name)
            ticket_flow_log_restful_list.append(dict(id=ticket_flow_log.id, ticket_id=ticket_id, state=state_info_dict, transition=transition_info_dict, intervene_type_id=ticket_flow_log.intervene_type_id, participant_type_id=ticket_flow_log.participant_type_id,
                                                     participant=ticket_flow_log.participant, suggestion=ticket_flow_log.suggestion, gmt_created=str(ticket_flow_log.gmt_created)[:19], gmt_modified=str(ticket_flow_log.gmt_modified)[:19]
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
                            else:
                                transition_name = '未知操作'
                        state_flow_log_list.append(dict(id=ticket_flow_log.id, transition=dict(transition_name=transition_name, transition_id=ticket_flow_log.transition_id), participant_type_id=ticket_flow_log.participant_type_id,
                                                        participant=ticket_flow_log.participant, intervene_type_id=ticket_flow_log.intervene_type_id, suggestion=ticket_flow_log.suggestion, state_id=ticket_flow_log.state_id, gmt_created=str(ticket_flow_log.gmt_created)[:19]))
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
            ticket_obj.state_id = state_id
            ticket_obj.participant_type_id = state_obj.participant_type_id
            ticket_obj.participant = state_obj.participant
            ticket_obj.save()
            # 新增流转记录

            cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=0, suggestion='强制修改工单状态', participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                         participant=username, state_id=source_state_id))
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
            ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion='接单处理', participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                        intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT,
                                        participant=username, state_id=ticket_obj.state_id, creator=username)
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
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER,
                                    participant=username, state_id=ticket_obj.state_id, creator=username)
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
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE,
                                    participant=username, state_id=ticket_obj.state_id, creator=username)
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
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END,
                                    participant=username, state_id=ticket_obj.state_id, creator=username)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''
