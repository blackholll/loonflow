import copy
import json
import datetime
import logging
import random

import redis
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import CustomField
from apps.ticket.models import TicketRecord, TicketCustomField, TicketFlowLog, TicketUser
from service.redis_pool import POOL
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.common.common_service import common_service_ins
from service.common.constant_service import constant_service_ins
from service.account.account_base_service import account_base_service_ins
from service.workflow.workflow_base_service import workflow_base_service_ins
from service.workflow.workflow_state_service import workflow_state_service_ins
from service.workflow.workflow_transition_service import workflow_transition_service_ins
from service.workflow.workflow_custom_field_service import workflow_custom_field_service_ins


class TicketBaseService(BaseService):
    """
    工单基础服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_ticket_by_id(cls, ticket_id: int)->tuple:
        """
        获取工单对象
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if ticket_obj:
            return True, ticket_obj
        else:
            return False, 'ticket is not existed or has been deleted'

    @classmethod
    @auto_log
    def get_ticket_list(cls, sn: str='', title: str='', username: str='', create_start: str='', create_end: str='',
                        workflow_ids: str='', state_ids: str='', ticket_ids: str='', category: str='', reverse: int=1,
                        per_page: int=10, page: int=1, app_name: str='', **kwargs):
        """
        工单列表
        :param sn:
        :param title:
        :param username:
        :param create_start: 创建时间起
        :param create_end: 创建时间止
        :param workflow_ids: 工作流id,str,逗号隔开
        :param state_ids: 状态id,str,逗号隔开
        :param ticket_ids: 工单id,str,逗号隔开
        :param category: 查询类别(创建的，待办的，关联的:包括创建的、处理过的、曾经需要处理但是没有处理的, 我处理过的)
        :param reverse: 按照创建时间倒序
        :param per_page:
        :param page:
        :param app_name:
        act_state_id: int=0 进行状态, 0 草稿中、1.进行中 2.被退回 3.被撤回 4.已完成 5.已关闭
        :return:
        """
        category_list = ['all', 'owner', 'duty', 'relation', 'worked', 'view', 'intervene']
        if category not in category_list:
            return False, 'category value is invalid, it should be in all, owner, duty, relation'
        query_params = Q(is_deleted=False)

        # 获取调用方app_name 有权限的workflow_id_list

        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        flag, result = workflow_permission_service_ins.get_workflow_id_list_by_permission('api', 'app', app_name)

        if not flag or not result.get('workflow_id_list'):
            return True, dict(ticket_result_restful_list=[], paginator_info=dict(per_page=per_page, page=page, total=0))
        else:
            app_workflow_id_list = result.get('workflow_id_list')
            # query_params &= Q(workflow_id__in=result.get('workflow_id_list'))

        if kwargs.get('act_state_id') != '':
            query_params &= Q(act_state_id=int(kwargs.get('act_state_id')))

        if kwargs.get('from_admin') != '':
            # 管理员查看， 获取其有权限的工作流列表
            flag, result = workflow_base_service_ins.get_workflow_manage_list(username
                                                                              )
            if flag is False:
                return False, result
            workflow_list = result.get('workflow_list')
            workflow_admin_id_list = [workflow['id'] for workflow in workflow_list]
            # query_params &= Q(workflow_id__in=workflow_admin_id_list)

        if kwargs.get('creator') != '':
            query_params &= Q(creator=kwargs.get('creator'))
        if kwargs.get('parent_ticket_id'):
            query_params &= Q(parent_ticket_id=kwargs.get('parent_ticket_id'))
        if kwargs.get('parent_ticket_state_id'):
            query_params &= Q(parent_ticket_state_id=kwargs.get('parent_ticket_state_id'))

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
            query_workflow_id_list = [int(workflow_id_str) for workflow_id_str in workflow_id_str_list]
        else:
            query_workflow_id_list = []

            # query_params &= Q(workflow_id__in=workflow_id_list)
        if state_ids:
            state_id_str_list = state_ids.split(',')
            state_id_list = [int(state_id_str) for state_id_str in state_id_str_list]
            query_params &= Q(state_id__in=state_id_list)
        if ticket_ids:
            ticket_id_str_list = ticket_ids.split(',')
            ticket_id_list = [int(ticket_id_str) for ticket_id_str in ticket_id_str_list]
            query_params &= Q(id__in=ticket_id_list)

        if kwargs.get('from_admin'):
            permission_workflow_id_set = set(workflow_admin_id_list) - (set(workflow_admin_id_list) - set(app_workflow_id_list))
            if query_workflow_id_list:
                ending_workflow_id_list = list(permission_workflow_id_set - (permission_workflow_id_set - set(query_workflow_id_list)))
            else:
                ending_workflow_id_list = list(permission_workflow_id_set)
        else:
            if query_workflow_id_list:
                ending_workflow_id_list = list(set(app_workflow_id_list) - (set(app_workflow_id_list) - set(query_workflow_id_list)))
            else:
                ending_workflow_id_list = app_workflow_id_list

        query_params &= Q(workflow_id__in=ending_workflow_id_list)

        if reverse:
            order_by_str = '-gmt_created'
        else:
            order_by_str = 'gmt_created'

        if category == 'owner':
            query_params &= Q(creator=username)
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'duty':
            # 为了加快查询速度，该结果从ticket_usr表中获取。 对于部门、角色、这种处理人类型的，工单流转后 修改了部门或角色对应的人员会存在这些人无法在待办列表中查询到工单
            duty_query_expression = Q(ticketuser__in_process=True, ticketuser__username=username)
            query_params &= duty_query_expression
            act_state_expression = ~Q(act_state_id__in=[
                constant_service_ins.TICKET_ACT_STATE_FINISH,
                constant_service_ins.TICKET_ACT_STATE_CLOSED
            ])
            query_params &= act_state_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'relation':
            relation_query_expression = Q(ticketuser__username=username)
            query_params &= relation_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'worked':
            worked_query_expression = Q(ticketuser__username=username, ticketuser__worked=True)
            query_params &= worked_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category in ('view', 'intervene'):
            flag, result = workflow_permission_service_ins.get_workflow_id_list_by_permission(category, 'user', username)
            if not flag:
                view_workflow_ids = []
            else:
                view_workflow_ids = result.get('workflow_id_list', [])
            view_department_workflow_id_list = []
            if category == 'view':
                # view 还需要考虑查看权限部门,先查询用户所在部门，然后查询
                flag, result = account_base_service_ins.get_user_up_dept_id_list(username)
                if flag:
                    department_id_str_list = [str(result0) for result0 in result]
                    flag, result = workflow_permission_service_ins.get_workflow_id_list_by_permission(
                        category, 'department', ','.join(department_id_str_list))
                    view_department_workflow_id_list = result.get('workflow_id_list', []) if flag else []

            category_workflow_ids = list(set(view_workflow_ids).union(set(view_department_workflow_id_list)))

            view_query_expression = Q(workflow_id__in=category_workflow_ids)
            query_params &= view_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        else:
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()

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
            state_obj_flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_result_object.state_id)
            state_name = state_obj.name if state_obj_flag else '未知状态'
            flag, participant_info = cls.get_ticket_format_participant_info(ticket_result_object.id)

            flag, workflow_obj = workflow_base_service_ins.get_by_id(ticket_result_object.workflow_id)
            workflow_info_dict = dict(workflow_id=workflow_obj.id, workflow_name=workflow_obj.name)

            flag, creator_obj = account_base_service_ins.get_user_by_username(ticket_result_object.creator)
            if flag:
                flag, dept_dict_info = account_base_service_ins.get_user_dept_info(user_id=creator_obj.id)

                creator_info = dict(username=creator_obj.username, alias=creator_obj.alias,
                                    is_active=creator_obj.is_active, email=creator_obj.email, phone=creator_obj.phone,
                                    dept_info=dept_dict_info)
            else:
                creator_info = dict(username=ticket_result_object.creator, alias='', is_active=False, email='',
                                    phone='', dept_info={})
            ticket_format_obj = ticket_result_object.get_dict()

            state_obj_label = '{}'
            if state_obj_flag:
                state_obj_label = json.loads(state_obj.label)
            ticket_format_obj.update(dict(state=dict(state_id=ticket_result_object.state_id, state_name=state_name,
                                                     state_label=state_obj_label),
                                          participant_info=participant_info, creator_info=creator_info,
                                          workflow_info=workflow_info_dict))

            ticket_result_restful_list.append(ticket_format_obj)
        return True, dict(ticket_result_restful_list=ticket_result_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def new_ticket(cls, request_data_dict: dict, app_name: str='')->tuple:
        """
        新建工单
        :param request_data_dict:
        :param app_name: 调用源app_name
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

        request_field_arg_list = [key for key, value in request_data_dict.items()
                                  if (key not in ['workflow_id', 'suggestion', 'username'])]

        # 判断用户是否有权限新建该工单
        has_permission, msg = workflow_base_service_ins.check_new_permission(username, workflow_id)
        if not has_permission:
            return False, msg

        # 获取新建工单必填信息(根据工作流初始状态确定)
        flag, start_state = workflow_state_service_ins.get_workflow_start_state(workflow_id)
        if flag is False:
            return False, start_state
        flag, state_info_dict = cls.get_state_field_info(start_state.id)
        require_field_list = state_info_dict.get('require_field_list', [])  # 必填字段
        update_field_list = state_info_dict.get('update_field_list', [])  # 必填+可选字段，即需要保存值的字段

        # 校验是否所有必填字段都有提供，如果transition对应设置为不校验必填则直接通过
        flag, req_transition_obj = workflow_transition_service_ins.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))

        flag, msg = cls.get_next_state_id_by_transition_and_ticket_info(0, request_data_dict)
        if flag:
            destination_state_id = msg.get('destination_state_id')
        else:
            return False, msg

        flag, destination_state = workflow_state_service_ins.get_workflow_state_by_id(destination_state_id)

        # 获取目标状态的信息
        flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id,
                                                                       ticket_req_dict=request_data_dict)
        if not flag:
            return False, participant_info
        destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
        destination_participant = participant_info.get('destination_participant', '')
        multi_all_person = participant_info.get('multi_all_person', '{}')  # 多人需要全部处理情况

        # 生成流水号
        flag, result = cls.gen_ticket_sn(app_name)
        if not flag:
            return False, result
        ticket_sn = result.get('ticket_sn')

        # 新增工单基础表数据
        if destination_state.type_id == constant_service_ins.STATE_TYPE_END:
            act_state_id = constant_service_ins.TICKET_ACT_STATE_FINISH
        elif destination_state.type_id == constant_service_ins.STATE_TYPE_START:
            act_state_id = constant_service_ins.TICKET_ACT_STATE_DRAFT
        else:
            act_state_id = constant_service_ins.TICKET_ACT_STATE_ONGOING
        flag, workflow_base_obj = workflow_base_service_ins.get_by_id(workflow_id)
        title_template = workflow_base_obj.title_template
        title = request_data_dict.get('title', '')
        import copy
        title_render_data = copy.deepcopy(request_data_dict)
        now_time = str(datetime.datetime.now())[:19]
        flag, user_info = account_base_service_ins.get_user_by_username(username)
        if flag:
            user_alias = user_info.alias
        else:
            user_alias = username
        title_render_data.update({'title': title, 'sn': ticket_sn, 'state_id': start_state.id, 'participant_info.participant_name': username,
                                  'participant_info.alias': user_alias, 'workflow.workflow_name': workflow_base_obj.name,
                                  'creator': username, 'gmt_created': now_time, 'gmt_modified': now_time, 'state.state_name': start_state.name})

        if title_template:
            title = title_template.format(**title_render_data)

        new_ticket_obj = TicketRecord(sn=ticket_sn, title=title, workflow_id=workflow_id,
                                      state_id=destination_state_id, parent_ticket_id=parent_ticket_id,
                                      parent_ticket_state_id=parent_ticket_state_id,
                                      participant=destination_participant,
                                      participant_type_id=destination_participant_type_id, relation=username,
                                      creator=username, act_state_id=act_state_id, multi_all_person=multi_all_person)
        new_ticket_obj.save()

        # 更新工单关系人
        flag, result = cls.get_ticket_dest_relation(destination_participant_type_id, destination_participant)
        if flag is True:
            cls.update_ticket_relation(new_ticket_obj.id, result.get('add_relation'), ticket_creator=username)

        # 新增自定义字段，只保存required_field
        request_data_dict_allow = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                request_data_dict_allow[key] = value

        update_ticket_custom_field_result, msg = cls.update_ticket_custom_field(new_ticket_obj.id,
                                                                                request_data_dict_allow)
        if not update_ticket_custom_field_result:
            return False, msg
        # 新增流转记录,记录流转时工单所有字段的值
        flag, result = cls.get_ticket_all_field_value_json(new_ticket_obj.id)
        if flag is False:
            return False, result

        all_ticket_data_json = result.get('all_field_value_json')
        new_ticket_flow_log_dict = dict(ticket_id=new_ticket_obj.id, transition_id=transition_id,
                                        suggestion=suggestion,
                                        participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                        participant=username, state_id=start_state.id, ticket_data=all_ticket_data_json)
        add_ticket_flow_log_result, msg = cls.add_ticket_flow_log(new_ticket_flow_log_dict)
        if not add_ticket_flow_log_result:
            return False, msg
        # 通知消息
        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[new_ticket_obj.id], queue='loonflow')

        # 如果下个状态为脚本处理，则开始执行脚本
        if destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
            from tasks import run_flow_task  # 放在文件开头会存在循环引用
            run_flow_task.apply_async(args=[new_ticket_obj.id, destination_participant, destination_state_id],
                                      queue='loonflow')

        # 如果下个状态是hook，开始触发hook
        if destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
            from tasks import flow_hook_task  # 放在文件开头会存在循环引用
            flow_hook_task.apply_async(args=[new_ticket_obj.id], queue='loonflow')

        # 定时器处理逻辑
        cls.handle_timer_transition(new_ticket_obj.id, destination_state_id)

        # 父工单逻辑处理
        if destination_state.type_id == constant_service_ins.STATE_TYPE_END and new_ticket_obj.parent_ticket_id \
                and new_ticket_obj.parent_ticket_state_id:
                # 如果存在父工单，判断是否该父工单的下属子工单都已经结束状态，如果都是结束状态则自动流转父工单到下个状态
            filter_params = dict(
                parent_ticket_id=new_ticket_obj.parent_ticket_id,
                parent_ticket_state_id=new_ticket_obj.parent_ticket_state_id,
                is_deleted=0
            )
            other_sub_ticket_queryset = TicketRecord.objects.filter(**filter_params).all()
            # 所有子工单使用相同的工作流,所以state都一样，检测是否都是ticket_obj.state_id即可判断是否都是结束状态
            other_sub_ticket_state_id_list = [other_sub_ticket.state_id
                                              for other_sub_ticket in other_sub_ticket_queryset]
            flag, result = workflow_state_service_ins.get_states_info_by_state_id_list(other_sub_ticket_state_id_list)
            if flag:
                sub_ticket_state_type_list = []
                for key, value in result.items():
                    sub_ticket_state_type_list.append(value.get('type_id'))
                list_set = set(sub_ticket_state_type_list)
                if list_set == {constant_service_ins.STATE_TYPE_END}:
                    parent_ticket_obj = TicketRecord.objects.filter(id=new_ticket_obj.parent_ticket_id, is_deleted=0) \
                        .first()
                    parent_ticket_state_id = parent_ticket_obj.state_id
                    flag, parent_ticket_transition_queryset = workflow_transition_service_ins \
                        .get_state_transition_queryset(parent_ticket_state_id)
                    # 含有子工单的工单状态只支持单路径流转到下个状态
                    parent_ticket_transition_id = parent_ticket_transition_queryset[0].id
                    cls.handle_ticket(parent_ticket_obj.id, dict(transition_id=parent_ticket_transition_id,
                                                                 username='loonrobot',
                                                                 suggestion='所有子工单处理完毕，自动流转'))
        return True, dict(new_ticket_id=new_ticket_obj.id)

    @classmethod
    @auto_log
    def gen_ticket_sn(cls, app_name: str='')->tuple:
        redis_conn = redis.Redis(connection_pool=POOL)
        ticket_day_count_key = 'ticket_day_count_{}'.format(str(datetime.datetime.now())[:10])
        try:
            ticket_day_count = redis_conn.get(ticket_day_count_key)
        except redis.exceptions.ConnectionError:
            return False, 'Redis连接失败，请确认Redis已启动并配置正确'
        except Exception as e:
            raise Exception(e.__str__())

        if ticket_day_count is not None:
            new_ticket_day_count = redis_conn.incr(ticket_day_count_key)
        else:
            # 查询数据库中个数
            # 今天和明天
            today = str(datetime.datetime.now())[:10] + " 00:00:00"
            next_day = str(datetime.datetime.now() + datetime.timedelta(days=1))[:10] + " 00:00:00"
            # 包括is_deleted=1的数据
            ticket_day_count = TicketRecord.objects.filter(gmt_created__gte=today, gmt_created__lt=next_day).count()
            new_ticket_day_count = int(ticket_day_count) + 1
            redis_conn.set(ticket_day_count_key, new_ticket_day_count, 86400)
        now_day = datetime.datetime.now()
        if not app_name:
            sn_prefix = 'loonflow'
        else:
            if app_name == 'loonflow':
                sn_prefix = 'loonflow'
            else:
                flag, result = account_base_service_ins.get_token_by_app_name(app_name)
                if flag is False:
                    return False, result
                sn_prefix = result.ticket_sn_prefix

        zone_info = ''
        if settings.DEPLOY_ZONE:
            # for multi computer room deploy and use separate redis server
            zone_info = '{}_'.format(settings.DEPLOY_ZONE)

        return True, dict(ticket_sn='%s_%s%04d%02d%02d%04d' % (sn_prefix, zone_info, now_day.year, now_day.month,
                                                               now_day.day, new_ticket_day_count))

    @classmethod
    @auto_log
    def get_ticket_field_value(cls, ticket_id: int, field_key: str)->tuple:
        """
        get ticket field's value, include base filed and custom field
        :param ticket_id:
        :param field_key:
        :return:
        """
        if field_key in constant_service_ins.TICKET_BASE_FIELD_LIST:
            ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
            ticket_obj_dict = ticket_obj.get_dict()
            value = ticket_obj_dict.get(field_key)
        else:
            flag, result = cls.get_ticket_custom_field_value(ticket_id, field_key)
            if flag is False:
                return False, result
            value = result.get('value')

        return True, dict(value=value)

    @classmethod
    @auto_log
    def get_ticket_format_custom_field_key_dict(cls, ticket_id: int)->tuple:
        """
        get ticket custom field attribute to dict format
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        custom_field_queryset = CustomField.objects.filter(is_deleted=0, workflow_id=ticket_obj.workflow_id).all()
        format_field_key_dict = {}
        for custom_field in custom_field_queryset:
            format_field_key_dict[custom_field.field_key] = dict(field_type_id=custom_field.field_type_id,
                                                                 name=custom_field.field_name,
                                                                 bool_field_display=custom_field.boolean_field_display,
                                                                 field_choice=custom_field.field_choice,
                                                                 field_from='custom')

        return True, format_field_key_dict

    @classmethod
    @auto_log
    def get_ticket_custom_field_value(cls, ticket_id: int, field_key: str)->tuple:
        """
        get ticket custom field value
        :param ticket_id:
        :param field_key:
        :return:
        """
        flag, result = cls.get_ticket_format_custom_field_key_dict(ticket_id)
        if flag is False:
            return False, result

        field_type_id = result[field_key]['field_type_id']
        ticket_custom_field_obj = TicketCustomField.objects.filter(field_key=field_key, ticket_id=ticket_id,
                                                                   is_deleted=0).first()

        if not ticket_custom_field_obj:
            # has not been assignment
            value = None
        else:
            value_dict = ticket_custom_field_obj.get_dict()
            value_enum = constant_service_ins.FIELD_VALUE_ENUM
            value = value_dict.get(value_enum[field_type_id])
        return True, dict(value=value)

    @classmethod
    @auto_log
    def get_ticket_field_name(cls, ticket_id: int, field_key: str)->tuple:
        """
        get ticket field's name by field_key
        :param ticket_id:
        :param field_key:
        :return:
        """
        if field_key in constant_service_ins.TICKET_BASE_FIELD_LIST:
            return True, dict(field_name=field_key)
        else:
            flag, result = cls.get_ticket_custom_field_name(ticket_id, field_key)
            if flag is False:
                return False, result

        return True, dict(field_name=result.get('field_name'))

    @classmethod
    @auto_log
    def get_ticket_custom_field_name(cls, ticket_id: int, field_key: str)->tuple:
        """
        get ticket custom field's field_name
        :param ticket_id:
        :param field_key:
        :return:
        """
        flag, result = cls.get_ticket_format_custom_field_key_dict(ticket_id)
        if flag is False:
            return False, result

        field_name = result[field_key]['field_name']

        return True, dict(field_name=field_name)

    @classmethod
    @auto_log
    def update_ticket_custom_field(cls, ticket_id: int, update_dict: dict)->tuple:
        """
        update ticket's custom fields's value(create or update)
        :param ticket_id:
        :param update_dict:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        flag, format_custom_field_dict = workflow_custom_field_service_ins\
            .get_workflow_custom_field(ticket_obj.workflow_id)
        if flag is False:
            return False, format_custom_field_dict
        format_custom_field_dict = format_custom_field_dict
        custom_field_key_list = [key for key, value in format_custom_field_dict.items()]

        # 因为工单的自定义字段不会太多，且有可能是新增有可能是更新， 所以直接遍历处理
        for key, value in update_dict.items():
            if key in custom_field_key_list:
                # 判断是否存在，如果存在则更新，如果不存在则新增
                ticket_custom_field_queryset = TicketCustomField.objects.filter(
                    ticket_id=ticket_id, field_key=key, is_deleted=0)
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
                    value_enum = constant_service_ins.FIELD_VALUE_ENUM

                    if ticket_custom_field_queryset:
                        ticket_custom_field_queryset.update(**{value_enum.get(field_type_id): update_dict.get(key)})

                    elif not ticket_custom_field_queryset:
                        new_dict = {
                            'name': format_custom_field_dict[key]['field_name'],
                            'ticket_id': ticket_id,
                            'field_key': key,
                            'field_type_id': field_type_id,
                            value_enum[field_type_id]: update_dict.get(key)
                        }
                        new_ticket_custom_field_record = TicketCustomField(**new_dict)
                        new_ticket_custom_field_record.save()
        return True, ''

    @classmethod
    @auto_log
    def update_ticket_field_value(cls, ticket_id: int, update_dict: dict)-> tuple:
        """
        update ticket field's value
        :param ticket_id:
        :param update_dict:
        :return:
        """
        base_field_dict = {}
        for key, value in update_dict.items():
            if key in constant_service_ins.TICKET_BASE_FIELD_LIST:
                base_field_dict[key] = value
        # ticket base field
        if base_field_dict:
            TicketRecord.objects.filter(id=ticket_id, is_deleted=0).update(**base_field_dict)
        # custom field
        cls.update_ticket_custom_field(ticket_id, update_dict)

        return True, ''

    @classmethod
    @auto_log
    def add_ticket_flow_log(cls, kwargs: dict)->tuple:
        """
        add ticket flow record
        :param kwargs:
        :return:
        """
        # in some mysql version's default config, string while be structure if the length is greater than defined
        suggestion = kwargs.get('suggestion', '') if kwargs.get('suggestion', '') else ''
        if len(suggestion) > 1000:
            kwargs['suggestion'] = '{}...(be truncated because More than 1000)'\
                .format(kwargs.get('suggestion', '')[:960])
        kwargs['suggestion'] = suggestion

        if not kwargs.get('creator'):
            kwargs['creator'] = kwargs.get('participant', '')
        new_ticket_flow_log = TicketFlowLog(**kwargs)
        new_ticket_flow_log.save()
        return True, dict(new_ticket_flow_log_id=new_ticket_flow_log.id)

    @classmethod
    @auto_log
    def get_ticket_detail(cls, ticket_id: int, username: str)-> tuple:
        """
        get ticket's detail info, According to the current state and username.
        if user only has reade permission, the response field accord to workflow config, otherwise state config
        :param ticket_id:
        :param username:
        :return:
        """
        flag, result = cls.ticket_handle_permission_check(ticket_id, username)

        if flag is False or not result.get('permission'):
            view_permission, msg = cls.ticket_view_permission_check(ticket_id, username)
            if not view_permission:
                return False, msg
            handle_permission = False
        else:
            handle_permission = True

        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        flag, result = cls.get_ticket_base_field_list(ticket_id)

        field_list = result.get('field_list') if flag else []

        new_field_list = []

        if handle_permission:
            flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_obj.state_id)
            if flag:
                state_field_str = state_obj.state_field_str
                state_field_dict = json.loads(state_field_str)
                state_field_key_list = state_field_dict.keys()
                for field in field_list:
                    if field['field_key'] in state_field_key_list:
                        field['field_attribute'] = state_field_dict[field['field_key']]
                        new_field_list.append(field)
        else:
            # only read permission
            flag, workflow_obj = workflow_base_service_ins.get_by_id(workflow_id=ticket_obj.workflow_id)
            display_form_field_list = json.loads(workflow_obj.display_form_str) if workflow_obj.display_form_str else []
            for field in field_list:
                if field['field_key'] in display_form_field_list:
                    new_field_list.append(field)
        # order by field's order id
        new_field_list = sorted(new_field_list, key=lambda r: r['order_id'])
        flag, creator_obj = account_base_service_ins.get_user_by_username(ticket_obj.creator)
        if flag:

            flag, dept_dict_info = account_base_service_ins.get_user_dept_info(user_id=creator_obj.id)
            creator_info = dict(username=creator_obj.username, alias=creator_obj.alias,
                                is_active=creator_obj.is_active, email=creator_obj.email,
                                phone=creator_obj.phone, dept_info=dept_dict_info)
        else:
            creator_info = dict(username=ticket_obj.creator, alias='', is_active=False, email='', phone='',
                                dept_info={})
        # 当前状态信息
        flag, result = workflow_state_service_ins.get_workflow_state_by_id(ticket_obj.state_id)
        if flag:
            state_info = result.get_dict()
            if state_info['participant_type_id'] == constant_service_ins.PARTICIPANT_TYPE_HOOK:
                state_info['participant'] = 'hook'
            state_info['state_field_str'] = json.loads(state_info['state_field_str'])
            state_info['label'] = json.loads(state_info['label'])
        else:
            state_info = dict(id=ticket_obj.state_id, name='--状态已被删除--')
        ticket_result_dict = ticket_obj.get_dict()
        ticket_result_dict.update(dict(field_list=new_field_list, creator_info=creator_info, state_info=state_info))
        return True, ticket_result_dict

    @classmethod
    @auto_log
    def get_ticket_base_field_list(cls, ticket_id: int)->tuple:
        """
        get ticket base field info list
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_obj.state_id)
        if flag is False:
            return False, state_obj
        state_name = state_obj.name

        # base field and attribute
        field_list = []
        flag, participant_info_dict = cls.get_ticket_format_participant_info(ticket_id)
        if flag is False:
            return False, participant_info_dict
        flag, workflow_obj = workflow_base_service_ins.get_by_id(ticket_obj.workflow_id)
        if flag is False:
            return False, workflow_obj
        workflow_name = workflow_obj.name

        field_list.append(dict(field_key='sn', field_name=u'流水号', field_value=ticket_obj.sn, order_id=10,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,
                               description='', field_choice={}, boolean_field_display={}, default_value=None,
                               field_template='', label={}, placeholder=''))
        field_list.append(dict(field_key='title', field_name=u'标题', field_value=ticket_obj.title, order_id=20,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='state_id', field_name=u'状态id', field_value=ticket_obj.state_id, order_id=40,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='participant_info.participant_name', field_name=u'当前处理人',
                               field_value=participant_info_dict['participant_name'], order_id=50,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='participant_info.participant_alias', field_name=u'当前处理人',
                               field_value=participant_info_dict['participant_alias'], order_id=55,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,
                               description='', field_choice={}, boolean_field_display={},
                               default_value=None, field_template='', label={}, placeholder=''))

        field_list.append(dict(field_key='workflow.workflow_name', field_name=u'工作流名称', field_value=workflow_name,
                               order_id=60, field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))

        field_list.append(dict(field_key='creator', field_name=u'创建人', field_value=ticket_obj.creator, order_id=80,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='gmt_created', field_name=u'创建时间',
                               field_value=str(ticket_obj.gmt_created)[:19], order_id=100,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='gmt_modified', field_name=u'更新时间',
                               field_value=str(ticket_obj.gmt_modified)[:19], order_id=120,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))
        field_list.append(dict(field_key='state.state_name', field_name=u'状态名', field_value=state_name, order_id=41,
                               field_type_id=constant_service_ins.FIELD_TYPE_STR,
                               field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO, description='',
                               field_choice={}, boolean_field_display={}, default_value=None, field_template='',
                               label={}, placeholder=''))

        # ticket's all custom field
        flag, custom_field_dict = workflow_custom_field_service_ins.get_workflow_custom_field(ticket_obj.workflow_id)
        custom_field_key_list = [key for key, value in custom_field_dict.items()]
        ticket_custom_field_objs = TicketCustomField.objects.filter(ticket_id=ticket_id,
                                                                    field_key__in=custom_field_key_list,
                                                                    is_deleted=0).all()
        key_value_dict = {}
        for ticket_custom_field_obj in ticket_custom_field_objs:
            key_value_dict[ticket_custom_field_obj.field_key] = ticket_custom_field_obj
        for key, value in custom_field_dict.items():
            field_type_id = value['field_type_id']
            field_value_obj = key_value_dict.get(key)
            if not field_value_obj:
                field_value = None
            else:
                value_enum = constant_service_ins.FIELD_VALUE_ENUM
                field_value = field_value_obj.get_dict().get(value_enum.get(field_type_id))
            boolean_field_display = json.loads(
                custom_field_dict[key]['boolean_field_display']) if custom_field_dict[key]['boolean_field_display'] \
                else {}  # 之前model允许为空了，为了兼容先这么写

            field_list.append(dict(field_key=key, field_name=custom_field_dict[key]['field_name'],
                                   field_value=field_value, order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=constant_service_ins.FIELD_ATTRIBUTE_RO,
                                   default_value=custom_field_dict[key]['default_value'],
                                   description=custom_field_dict[key]['description'],
                                   field_template=custom_field_dict[key]['field_template'],
                                   boolean_field_display=boolean_field_display,
                                   field_choice=json.loads(custom_field_dict[key]['field_choice']),
                                   label=json.loads(custom_field_dict[key]['label']),
                                   placeholder=custom_field_dict[key]['placeholder']

                                   ))
        return True, dict(field_list=field_list)

    @classmethod
    @auto_log
    def get_ticket_format_participant_info(cls, ticket_id: int)->tuple:
        """
        get ticket's format participant_info(include role_name, department_name and so on )
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        participant = ticket_obj.participant
        participant_name = ticket_obj.participant
        participant_type_id = ticket_obj.participant_type_id
        participant_type_name = ''
        participant_alias = ''
        if participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
            participant_type_name = '个人'
            # participant_user_obj, msg = AccountBaseService.get_user_by_username(participant)
            flag, participant_user_obj = account_base_service_ins.get_user_by_username(participant)
            if flag:
                participant_alias = participant_user_obj.alias
            else:
                participant_alias = participant
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            participant_type_name = '多人'
            participant_name_list = participant_name.split(',')
            participant_map = {"name": set(), "alias": set()}
            flag, participant_user_objs = account_base_service_ins.get_user_list_by_usernames(participant_name_list)
            if flag:
                for participant_user in participant_user_objs:
                    participant_map["name"].add(participant_user.username)
                    participant_map["alias"].add(participant_user.alias)

                participant_map["alias"].update(
                    set(participant_name_list) - participant_map["name"]
                )

            participant_alias = ','.join(participant_map["alias"])

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            participant_type_name = '部门'
            flag, dept_obj = account_base_service_ins.get_dept_by_id(int(ticket_obj.participant))
            if flag is False:
                return False, dept_obj
            if not dept_obj:
                return False, 'dept_id:{} is not existed or has been deleted'.format(ticket_obj.participant)
            participant_name = dept_obj.name
            participant_alias = participant_name
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            participant_type_name = '角色'
            flag, role_obj = account_base_service_ins.get_role_by_id(int(ticket_obj.participant))

            if flag is False or (not role_obj):
                return False, 'role is not existed or has been deleted'
            participant_name = role_obj.name
            participant_alias = participant_name
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
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
                flag, participant_user_obj = account_base_service_ins.get_user_by_username(key)
                if not flag:
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
        return True, dict(participant=participant, participant_name=participant_name,
                          participant_type_id=participant_type_id, participant_type_name=participant_type_name,
                          participant_alias=participant_alias)

    @classmethod
    @auto_log
    def ticket_handle_permission_check(cls, ticket_id: int, username: str, by_timer: bool=False, by_task: bool=False,
                                       by_hook: bool=False)->tuple:
        """
        handle permission check
        :param ticket_id:
        :param username:
        :param by_timer: is timer or not
        :param by_task: is by script or not
        :param by_hook: is by hook or not
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        ticket_state_id = ticket_obj.state_id

        flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_state_id)
        if not flag:
            return True, dict(permission=False, msg='工单当前状态id不存在或已被删除')

        flag, transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(ticket_state_id)
        if flag is False:
            return False, transition_queryset

        if not transition_queryset:
            return True, dict(permission=False, msg='工单当前状态无需操作')

        if by_timer and username == 'loonrobot':
            # by time
            return True, dict(permission=True, need_accept=False, in_add_node=False, msg='by timer,release permissions')
        if by_task and username == 'loonrobot':
            # by script
            return True, dict(permission=True, need_accept=False, in_add_node=False,
                              msg='by script,release permissions')
        if by_hook and username == 'loonrobot':
            # by hook
            return True, dict(permission=True, need_accept=False, in_add_node=False, msg='by hook,release permissions')

        participant_type_id = ticket_obj.participant_type_id
        participant = ticket_obj.participant

        current_participant_count = 1  # 当前处理人个数，用于当处理人大于1时 可能需要先接单再处理

        if participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
            if username != participant:
                return True, dict(permission=False, need_accept=False, in_add_node=False,
                                  msg='not current participant, no permission')
                # return None, '非当前处理人，无权处理'
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            if username not in participant.split(','):
                return True, dict(permission=False, need_accept=False, in_add_node=False,
                                  msg='not crrent participant, no permission')
                # return None, '非当前处理人，无权处理'
            current_participant_count = len(participant.split(','))
        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            flag, dept_user_list = account_base_service_ins.get_dept_username_list(participant)
            if flag is False:
                return flag, dept_user_list
            if username not in dept_user_list:
                # return None, '非当前处理人，无权处理'
                return True, dict(permission=False, need_accept=False, in_add_node=False,
                                  msg='not current participant, no permission')
            current_participant_count = len(dept_user_list)

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            flag, role_user_list = account_base_service_ins.get_role_username_list(int(participant))
            if not flag:
                return False, role_user_list
            if username not in role_user_list:
                return True, dict(permission=False, need_accept=False, in_add_node=False,
                                  msg='not crrent participant, no permission')
                # return None, '非当前处理人，无权处理'
            current_participant_count = len(role_user_list)
        else:
            return True, dict(permission=False, need_accept=False, in_add_node=False,
                              msg='not crrent participant, no permission')
            # return None, '非当前处理人，无权处理'
        # PARTICIPANT_TYPE_VARIABLE, PARTICIPANT_TYPE_FIELD, PARTICIPANT_TYPE_PARENT_FIELD类型会在流转时保存为实际的处理人

        if current_participant_count > 1 and \
                state_obj.distribute_type_id == constant_service_ins.STATE_DISTRIBUTE_TYPE_ACTIVE:
            need_accept = True
        else:
            need_accept = False
        if ticket_obj.in_add_node:
            in_add_node = True
        else:
            in_add_node = False

        return True, dict(permission=True, need_accept=need_accept, in_add_node=in_add_node)

    @classmethod
    @auto_log
    def ticket_view_permission_check(cls, ticket_id: int, username: str)-> tuple:
        """
        check user whether have view permission if open permission check in workflow config, otherwise decide by ticket releation
        校验用户是否有工单的查看权限:先查询对应的工作流是否校验查看权限， 如果不校验直接允许，如果校验需要判断用户是否属于工单的关系人
        :param ticket_id:
        :param username:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, 'ticket is not existed or has been deleted'
        flag, workflow_obj = workflow_base_service_ins.get_by_id(ticket_obj.workflow_id)
        if flag is False:
            return False, workflow_obj
        if not workflow_obj.view_permission_check:
            return True, "this ticket's workflow config did not open view permission check"
        else:
            flag, user_obj = account_base_service_ins.get_user_by_username(username)
            if flag is False:
                return False, 'user is not existed or has been deleted'
            else:
                if user_obj.type_id == constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN:
                    return True, 'admin has all ticket view permission'
            if username in ticket_obj.relation.split(','):
                return True, 'user is relation about this ticket, has view permission'
            else:
                return False, 'user is not relation about this ticket and the workflow open view permission check'

    @classmethod
    @auto_log
    def get_ticket_transition(cls, ticket_id: int, username: str)->tuple:
        """
        获取用户针对工单当前可以做的操作:处理权限校验、可以做的操作
        get ticket's action about some one
        :param ticket_id:
        :param username:
        :return:
        """
        flag, result = cls.ticket_handle_permission_check(ticket_id, username)
        if flag is False:
            return False, result

        if not result.get('permission'):
            return True, dict(transition_dict_list=[], msg=result.get('msg'))

        ticket_obj = TicketRecord.objects.filter(id=ticket_id).first()

        if ticket_obj.in_add_node:
            # add node state, just allow 'finish' action, after finish the ticket's participant will be set add_node_man
            transition_dict_list = [dict(transition_id=0, transition_name='完成', field_require_check=False,
                                         is_accept=False, in_add_node=True, alert_enable=False, alert_text='',
                                         attribute_type_id=constant_service_ins.TRANSITION_ATTRIBUTE_TYPE_OTHER)]
            return True, dict(transition_dict_list=transition_dict_list)

        if result.get('need_accept'):
            transition_dict_list = [dict(transition_id=0, transition_name='接单', field_require_check=False,
                                         is_accept=True, in_add_node=False, alert_enable=False, alert_text='',
                                         attribute_type_id=constant_service_ins.TRANSITION_ATTRIBUTE_TYPE_OTHER)]
            return True, dict(transition_dict_list=transition_dict_list)

        flag, transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(ticket_obj.state_id)
        transition_dict_list = []
        for transition in transition_queryset:
            transition_dict = dict(transition_id=transition.id, transition_name=transition.name,
                                   field_require_check=transition.field_require_check, is_accept=False,
                                   in_add_node=False, alert_enable=transition.alert_enable,
                                   alert_text=transition.alert_text, attribute_type_id=transition.attribute_type_id)
            transition_dict_list.append(transition_dict)
        return True, dict(transition_dict_list=transition_dict_list)

    @classmethod
    @auto_log
    def handle_ticket(cls, ticket_id: int, request_data_dict: dict, by_timer: bool=False, by_task: bool=False,
                      by_hook: bool=False):
        """
        处理工单:校验必填参数,获取当前状态必填字段，更新工单基础字段，更新工单自定义字段， 更新工单流转记录，执行必要的脚本，通知消息
        此处逻辑和新建工单有较多重复，下个版本会拆出来
        handle ticket, include params check,update base field, update custom field, update ticket flowlog,
        run script, send notice...
        :param ticket_id:
        :param request_data_dict:
        :param by_timer:  by timer transition
        :param by_task: by script task transition
        :param by_hook: by hook transition
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
        flag, result = cls.ticket_handle_permission_check(ticket_id, username, by_timer, by_task, by_hook)
        if flag is False:
            return False, result
        if result.get('permission') is False:
            return False, result.get('msg')
        if result.get('need_accept'):
            return False, '需要先接单再处理'
        if result.get('in_add_node'):
            return False, '工单当前处于加签中，只允许加签完成操作'

        flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_obj.state_id)
        if flag is False:
            return False, state_obj

        # 获取初始状态必填字段 及允许更新的字段
        flag, state_info_dict = cls.get_state_field_info(state_obj.id)
        require_field_list = state_info_dict.get('require_field_list', [])
        update_field_list = state_info_dict.get('update_field_list', [])

        # 校验是否所有必填字段都有提供，如果transition_id对应设置为不校验必填则直接通过
        flag, req_transition_obj = workflow_transition_service_ins.get_workflow_transition_by_id(transition_id)
        if req_transition_obj.field_require_check:

            request_field_arg_list = [key for key, value in request_data_dict.items()
                                      if (key not in ['workflow_id', 'suggestion', 'username'])]
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, '此工单的必填字段为:{}'.format(','.join(require_field_list))

        flag, msg = cls.get_next_state_id_by_transition_and_ticket_info(ticket_id, request_data_dict)
        if flag:
            destination_state_id = msg.get('destination_state_id')
        else:
            return False, msg

        flag, destination_state = workflow_state_service_ins.get_workflow_state_by_id(destination_state_id)

        # 判断当前处理人类型是否为全部处理，如果处理类型为全部处理（根据json.loads(ticket_obj.multi_all_person)来判断），且有人未处理，则工单状态不变，只记录处理过程
        if json.loads(ticket_obj.multi_all_person):
            multi_all_person = ticket_obj.multi_all_person
            multi_all_person_dict = json.loads(multi_all_person)
            flag, result = common_service_ins.get_dict_blank_or_false_value_key_list(multi_all_person_dict)
            if flag and result.get('result_list'):
                multi_all_person_dict[username] = dict(transition_id=transition_id,
                                                       transition_name=req_transition_obj.name)
                has_all_same_value, msg = common_service_ins.check_dict_has_all_same_value(multi_all_person_dict)
                if has_all_same_value:
                    # 所有人处理的transition都一致,则工单进入下个状态
                    flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id, ticket_id,
                                                                                   ticket_req_dict=request_data_dict)
                    if not flag:
                        return False, participant_info
                    destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
                    destination_participant = participant_info.get('destination_participant', '')
                    multi_all_person = '{}'
                else:
                    # 处理人没有没有全部处理完成或者处理动作不一致
                    destination_participant_type_id = ticket_obj.participant_type_id
                    flag, result = common_service_ins.get_dict_blank_or_false_value_key_list(multi_all_person_dict)
                    destination_participant = ','.join(result.get('result_list'))
                    destination_state_id = ticket_obj.state_id  # 保持原状态
                    flag, destination_state = workflow_state_service_ins.get_workflow_state_by_id(destination_state_id)
                    multi_all_person = json.dumps(multi_all_person_dict)

        else:
            # 当前处理人类型非全部处理
            # flag, destination_state = workflow_state_service_ins.get_workflow_state_by_id(destination_state_id)
            # if not destination_state:
            #     return False, msg
            # 获取目标状态的信息
            flag, participant_info = cls.get_ticket_state_participant_info(destination_state_id, ticket_id,
                                                                           ticket_req_dict=request_data_dict)
            if not flag:
                return False, participant_info
            destination_participant_type_id = participant_info.get('destination_participant_type_id', 0)
            destination_participant = participant_info.get('destination_participant', '')
            multi_all_person = participant_info.get('multi_all_person', '')
            # 如果开启了了记忆最后处理人,且当前状态非全部处理中，那么处理人为之前的处理人
            if destination_state.remember_last_man_enable and multi_all_person == '{}':
                # 获取此状态的最后处理人
                flag, result = cls.get_ticket_state_last_man(ticket_id, destination_state.id)
                if flag and result.get('last_man'):
                    destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
                    destination_participant = result.get('last_man')

        # 更新工单信息：基础字段及自定义字段， add_relation字段 需要下个处理人是部门、角色等的情况
        ticket_obj.state_id = destination_state_id
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.participant = destination_participant
        ticket_obj.multi_all_person = multi_all_person
        if destination_state.type_id == constant_service_ins.STATE_TYPE_END:
            ticket_obj.act_state_id = constant_service_ins.TICKET_ACT_STATE_FINISH
        elif destination_state.type_id == constant_service_ins.STATE_TYPE_START:
            ticket_obj.act_state_id = constant_service_ins.TICKET_ACT_STATE_DRAFT
        else:
            ticket_obj.act_state_id = constant_service_ins.TICKET_ACT_STATE_ONGOING

        if req_transition_obj.attribute_type_id == constant_service_ins.TRANSITION_ATTRIBUTE_TYPE_REFUSE:
            ticket_obj.act_state_id = constant_service_ins.TICKET_ACT_STATE_BACK

        ticket_obj.save()

        # 记录处理过的人
        if not (by_timer or by_task or by_hook):
            cls.update_ticket_worked(ticket_id, username)

        # 更新工单信息：基础字段及自定义字段， add_relation字段 需要考虑下个处理人是部门、角色等的情况
        flag, result = cls.get_ticket_dest_relation(destination_participant_type_id, destination_participant)

        if flag and result.get('add_relation'):
            cls.update_ticket_relation(ticket_id, result.get('add_relation'))  # 更新关系人信息

        # 只更新需要更新的字段
        update_field_dict = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                update_field_dict[key] = value

        cls.update_ticket_field_value(ticket_id, update_field_dict)
        # 更新工单流转记录，执行必要的脚本，通知消息
        flag, result = cls.get_ticket_all_field_value_json(ticket_id)
        if flag is False:
            return False, result
        ticket_all_data = result.get('all_field_value_json')

        if not by_task:
            # 脚本执行完自动触发的流转，因为在run_flow_task已经有记录操作日志，所以此次不再记录
            cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=transition_id, suggestion=suggestion,
                                         participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                         participant=username, state_id=source_ticket_state_id, creator=username,
                                         ticket_data=ticket_all_data))

        # 通知消息
        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')

        # 定时器逻辑
        cls.handle_timer_transition(ticket_id, destination_state_id)

        # 父工单逻辑处理
        if destination_state.type_id == constant_service_ins.STATE_TYPE_END and ticket_obj.parent_ticket_id \
                and ticket_obj.parent_ticket_state_id:
            # 如果存在父工单，判断是否该父工单的下属子工单都已经结束状态，如果都是结束状态则自动流转父工单到下个状态
            filter_params = dict(
                parent_ticket_id=ticket_obj.parent_ticket_id,
                parent_ticket_state_id=ticket_obj.parent_ticket_state_id,
                is_deleted=0
            )
            other_sub_ticket_queryset = TicketRecord.objects.filter(**filter_params).all()
            # 所有子工单使用相同的工作流,所以state都一样，检测是否都是ticket_obj.state_id即可判断是否都是结束状态
            other_sub_ticket_state_id_list = [other_sub_ticket.state_id
                                              for other_sub_ticket in other_sub_ticket_queryset]
            flag, result = workflow_state_service_ins.get_states_info_by_state_id_list(
                other_sub_ticket_state_id_list)
            if flag:
                sub_ticket_state_type_list = []
                for key, value in result.items():
                    sub_ticket_state_type_list.append(value.get('type_id'))
                list_set = set(sub_ticket_state_type_list)
                if list_set == {constant_service_ins.STATE_TYPE_END}:
                    parent_ticket_obj = TicketRecord.objects.filter(id=ticket_obj.parent_ticket_id,
                                                                    is_deleted=0).first()
                    parent_ticket_state_id = parent_ticket_obj.state_id
                    flag, parent_ticket_transition_queryset = workflow_transition_service_ins \
                        .get_state_transition_queryset(parent_ticket_state_id)
                    # 含有子工单的工单状态只支持单路径流转到下个状态
                    parent_ticket_transition_id = parent_ticket_transition_queryset[0].id
                    cls.handle_ticket(parent_ticket_obj.id, dict(transition_id=parent_ticket_transition_id,
                                                                 username='loonrobot',
                                                                 suggestion='所有子工单处理完毕，自动流转'))

        if destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
            from tasks import run_flow_task  # 放在文件开头会存在循环引用
            run_flow_task.apply_async(args=[ticket_id, destination_participant, destination_state_id], queue='loonflow')

        # 如果下个状态是hook，开始触发hook
        if destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
            from tasks import flow_hook_task  # 放在文件开头会存在循环引用
            flow_hook_task.apply_async(args=[ticket_id], queue='loonflow')

        return True, ''

    @classmethod
    @auto_log
    def add_ticket_relation(cls, ticket_id: int, user_str: str)->tuple:
        """
        新增工单关系人
        add ticket's relation
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
        return True, dict(new_relation=new_relation)

    @classmethod
    @auto_log
    def update_ticket_relation(cls, ticket_id: int, user_str: str, ticket_creator: str='')->tuple:
        """
        更新工单关系人
        :param ticket_id:
        :param user_str:
        :param ticket_creator:
        :return:
        """
        # ticket record table, for display ticket detail
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
        new_relation_set = set(ticket_obj.relation.split(',') + user_str.split(',') + [ticket_creator])  # 去重， 但是可能存在空元素
        new_relation_list = [new_relation0 for new_relation0 in new_relation_set if new_relation0]  # 去掉空元素
        new_relation = ','.join(new_relation_list)  # 去重
        ticket_obj.relation = new_relation
        ticket_obj.save()

        # ticket user table, for ticket list query
        if ticket_creator:
            # if ticket_creator is not null, is mean new ticket, should add creator
            new_record = TicketUser(ticket_id=ticket_id, username=ticket_creator)
            new_record.save()

        user_str_list = user_str.split(',')

        existed_record_queryset = TicketUser.objects.filter(ticket_id=ticket_id, username__in=user_str_list).all()
        user_need_update_list = [existed_record.username for existed_record in existed_record_queryset]
        user_need_add_list = [user_str for user_str in user_str_list if user_str not in user_need_update_list]

        TicketUser.objects.filter(ticket_id=ticket_id, username__in=user_need_update_list).update(in_process=True)
        insert_list = []
        for user_need_add in user_need_add_list:
            insert_list.append(TicketUser(ticket_id=ticket_id, username=user_need_add, in_process=True))
        TicketUser.objects.bulk_create(insert_list)

        # 非在user_str中的 更新为in_process=False
        TicketUser.objects.filter(ticket_id=ticket_id).exclude(username__in=user_str_list).all().update(in_process=False)

        return True, ''

    @classmethod
    @auto_log
    def update_ticket_worked(cls, ticket_id: int, username: str)-> tuple:
        """
        更新工单处理过的人
        :param ticket_id:
        :param username:
        :return:
        """
        worked_queryset = TicketUser.objects.filter(ticket_id=ticket_id, is_deleted=0, username=username).all()
        if worked_queryset:
            worked_queryset.update(worked=True, in_process=False)
        else:
            new_worked_record = TicketUser(ticket_id=ticket_id, username=username, in_process=False, worked=True)
            new_worked_record.save()
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_dest_relation(cls, destination_participant_type_id: int, destination_participant: str)->tuple:
        """
        获取目标处理人相应的工单关系人
        get ticket target participant's relation
        :param destination_participant_type_id:
        :param destination_participant:
        :return:
        """
        if destination_participant_type_id in (constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                               constant_service_ins.PARTICIPANT_TYPE_MULTI):
            add_relation = destination_participant
        elif destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            flag, username_list = account_base_service_ins.get_dept_username_list(destination_participant)
            if flag is False:
                return False, username_list
            add_relation = ','.join(username_list)
        elif destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            flag, username_list = account_base_service_ins.get_role_username_list(int(destination_participant))
            if flag is False:
                return False, username_list
            add_relation = ','.join(username_list)
        else:
            add_relation = ''
        return True, dict(add_relation=add_relation)

    @classmethod
    @auto_log
    def get_ticket_flow_log(cls, ticket_id: int, username: str, per_page: int=10, page: int=1, ticket_data=0, desc=1)->tuple:
        """
        获取工单流转记录
        get ticket's flow log
        :param ticket_id:
        :param username:
        :param per_page:
        :param page:
        :param ticket_data: 是否返回当前工单所有字段信息
        :param desc: 是否降序
        :return:
        """
        if desc == 0:
            ticket_flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, is_deleted=0).all().order_by('id')
        else:
            ticket_flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, is_deleted=0).all().order_by(
                '-id')
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
            flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(ticket_flow_log.state_id)

            flag, result = cls.get_flow_log_transition_name(ticket_flow_log.transition_id,
                                                            ticket_flow_log.intervene_type_id)
            if flag is False:
                return False, result
            transition_name = result.get('transition_name')
            attribute_type_id = result.get('attribute_type_id')

            state_info_dict = dict(state_id=state_obj.id, state_name=state_obj.name)
            transition_info_dict = dict(transition_id=ticket_flow_log.transition_id, transition_name=transition_name,
                                        attribute_type_id=attribute_type_id)
            participant_info = dict(participant_type_id=ticket_flow_log.participant_type_id,
                                    participant=ticket_flow_log.participant,
                                    participant_alias=ticket_flow_log.participant,
                                    participant_email='', participant_phone=''
                                    )
            if ticket_flow_log.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
                flag, participant_query_obj = account_base_service_ins.get_user_by_username(ticket_flow_log.participant)
                if flag:
                    participant_info.update(participant_alias=participant_query_obj.alias,
                                            participant_email=participant_query_obj.email,
                                            participant_phone=participant_query_obj.phone
                                            )

            ticket_flow_log_restful = dict(id=ticket_flow_log.id, ticket_id=ticket_id, state=state_info_dict,
                                           transition=transition_info_dict,
                                           intervene_type_id=ticket_flow_log.intervene_type_id,
                                           participant_type_id=ticket_flow_log.participant_type_id,
                                           participant=ticket_flow_log.participant,
                                           participant_info=participant_info,
                                           suggestion=ticket_flow_log.suggestion,
                                           gmt_created=str(ticket_flow_log.gmt_created)[:19]
                                           )
            if ticket_data:
                ticket_flow_log_restful.update(ticket_data=json.loads(ticket_flow_log.ticket_data))

            ticket_flow_log_restful_list.append(dict(ticket_flow_log_restful))

        return True, dict(ticket_flow_log_restful_list=ticket_flow_log_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def get_ticket_flow_step(cls, ticket_id: int, username: str)->tuple:
        """
        工单的流转步骤，路径。直线流转, 步骤不会很多(因为同个状态只显示一次，隐藏的状态只有当前处于才显示，否则不显示)，默认先不分页
        get ticket flow step info
        :param ticket_id:
        :param username:
        :return:
        """
        # 先获取工单对应工作流的信息
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        workflow_id = ticket_obj.workflow_id
        flag, state_objs = workflow_state_service_ins.get_workflow_states(workflow_id)
        ticket_flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, is_deleted=0).all()

        state_step_dict_list = []
        for state_obj in state_objs:
            if state_obj.id == ticket_obj.state_id or (not state_obj.is_hidden):
                ticket_state_step_dict = dict(state_id=state_obj.id, state_name=state_obj.name, order_id=state_obj.order_id)
                state_flow_log_list = []
                for ticket_flow_log in ticket_flow_log_queryset:
                    if ticket_flow_log.state_id == state_obj.id:
                        # 此部分和get_ticket_flow_log代码冗余，后续会简化下
                        flag, result = cls.get_flow_log_transition_name(ticket_flow_log.transition_id, ticket_flow_log.intervene_type_id)
                        if flag is False:
                            return False, result
                        transition_name = result.get('transition_name')
                        attribute_type_id = result.get('attribute_type_id')

                        participant_info = dict(participant_type_id=ticket_flow_log.participant_type_id,
                                                participant=ticket_flow_log.participant,
                                                participant_alias=ticket_flow_log.participant,
                                                participant_email='', participant_phone=''
                                                )
                        if ticket_flow_log.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
                            flag, participant_query_obj = account_base_service_ins.get_user_by_username(
                                ticket_flow_log.participant)
                            if flag:
                                participant_info.update(participant_alias=participant_query_obj.alias,
                                                        participant_email=participant_query_obj.email,
                                                        participant_phone=participant_query_obj.phone
                                                        )

                        state_flow_log_list.append(dict(id=ticket_flow_log.id, transition=dict(
                            transition_name=transition_name, transition_id=ticket_flow_log.transition_id),
                                                        participant_type_id=ticket_flow_log.participant_type_id,
                                                        participant=ticket_flow_log.participant,
                                                        participant_info=participant_info,
                                                        intervene_type_id=ticket_flow_log.intervene_type_id,
                                                        suggestion=ticket_flow_log.suggestion,
                                                        state_id=ticket_flow_log.state_id,
                                                        attribute_type_id=attribute_type_id,
                                                        gmt_created=str(ticket_flow_log.gmt_created)[:19]))
                state_flow_log_list = sorted(state_flow_log_list, key=lambda keys: keys['id'],reverse=True)
                ticket_state_step_dict['state_flow_log_list'] = state_flow_log_list
                state_step_dict_list.append(ticket_state_step_dict)
                state_step_dict_list = sorted(state_step_dict_list, key=lambda keys: keys['order_id'])
        return True, dict(state_step_dict_list=state_step_dict_list, current_state_id=ticket_obj.state_id)

    @classmethod
    @auto_log
    def get_flow_log_transition_name(cls, transition_id, intervene_type_id):
        """
        获取流转日志中流转名称
        :param transition_id:
        :param intervene_type_id:
        :return:
        """
        if transition_id:
            flag, transition_obj = workflow_transition_service_ins.get_workflow_transition_by_id(transition_id)
            if not transition_obj:
                transition_name = '未知操作'
                attribute_type_id = constant_service_ins.TRANSITION_ATTRIBUTE_TYPE_OTHER
            else:
                transition_name = transition_obj.name
                attribute_type_id = transition_obj.attribute_type_id
        else:
            if intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_DELIVER:
                transition_name = '转交操作'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_ADD_NODE:
                transition_name = '加签操作'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_ADD_NODE_END:
                transition_name = '加签完成操作'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_ACCEPT:
                transition_name = '接单操作'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_COMMENT:
                transition_name = '新增评论'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_CLOSE:
                transition_name = '强制关闭'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_ALTER_STATE:
                transition_name = '强制修改状态'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_HOOK:
                transition_name = 'hook操作'
            elif intervene_type_id == constant_service_ins.TRANSITION_INTERVENE_TYPE_RETREAT:
                transition_name = '撤回操作'
            else:
                transition_name = '未知操作'
            attribute_type_id = constant_service_ins.TRANSITION_ATTRIBUTE_TYPE_OTHER
        return True, dict(transition_name=transition_name, attribute_type_id=attribute_type_id)

    @classmethod
    @auto_log
    def update_ticket_state(cls, ticket_id: int, state_id: int, username: str, suggestion: str)->tuple:
        """
        更新状态id
        update ticket's state by ticket_id, state_id, username
        :param ticket_id:
        :param state_id:
        :param username:
        :param suggestion:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在'
        source_state_id = ticket_obj.state_id
        flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(state_id)
        if not state_obj:
            return False, state_obj
        if state_obj.workflow_id == ticket_obj.workflow_id:
            # 获取目标状态的处理人信息
            flag, destination_participant_info = cls.get_ticket_state_participant_info(state_id, ticket_id=ticket_id)
            ticket_obj.state_id = state_id
            ticket_obj.participant_type_id = destination_participant_info.get('destination_participant_type_id', 0)
            ticket_obj.participant = destination_participant_info.get('destination_participant', '')
            ticket_obj.multi_all_person = '{}'
            ticket_obj.save()

            if destination_participant_info.get('destination_participant_type_id', 0) in (
                    constant_service_ins.PARTICIPANT_TYPE_PERSONAL, constant_service_ins.PARTICIPANT_TYPE_MULTI):
                cls.update_ticket_relation(ticket_id, destination_participant_info.get('destination_participant', ''))

            # 新增流转记录
            # 获取工单所有字段的值
            flag, result = cls.get_ticket_all_field_value_json(ticket_id)
            if flag is False:
                return False, result

            all_ticket_data_json = result.get('all_field_value_json')

            cls.add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                                         participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                         intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_ALTER_STATE,
                                         participant=username, state_id=source_state_id,
                                         ticket_data=all_ticket_data_json))


            # 如果目标状态是脚本处理中，需要触发脚本处理
            if ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
                from tasks import run_flow_task  # 放在文件开头会存在循环引用
                run_flow_task.apply_async(args=[ticket_id, ticket_obj.participant, ticket_obj.state_id],
                                          queue='loonflow')
            # 目标状态处理人类型是hook，需要触发hook
            elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
                from tasks import flow_hook_task  # 放在文件开头会存在循环引用
                flow_hook_task.apply_async(args=[ticket_id], queue='loonflow')
            else:
                # 通知消息
                from tasks import send_ticket_notice
                send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')

            return True, '修改工单状态成功'

    @classmethod
    @auto_log
    def get_tickets_states_by_ticket_id_list(cls, ticket_id_list: list, username: str)->tuple:
        """
        批量获取工单状态
        get ticket's state by ticket_id_list
        :param ticket_id_list:
        :param username:
        :return:
        """
        ticket_queryset = TicketRecord.objects.filter(id__in=ticket_id_list).all()
        ticket_state_id_dict = {}
        for ticket in ticket_queryset:
            ticket_state_id_dict[ticket.id] = ticket.state_id
        ticket_state_id_list = [ticket_obj.state_id for ticket_obj in ticket_queryset]
        flag, state_info_dict = workflow_state_service_ins.get_states_info_by_state_id_list(ticket_state_id_list)
        new_result = {}
        for key, value in ticket_state_id_dict.items():
            new_result[key] = dict(state_id=value, state_name=state_info_dict[value]['name'])
        return True, new_result

    @classmethod
    @auto_log
    def accept_ticket(cls, ticket_id: int, username: str)->tuple:
        """
        accept ticket
        :param ticket_id:
        :param username:
        :return:
        """
        # check handle permission
        flag, result = cls.ticket_handle_permission_check(ticket_id, username)
        if not flag:
            return False, result
        if not result.get('permission'):
            return False, result.get('msg')

        if result.get('need_accept'):
            # update ticket relation people
            cls.update_ticket_relation(ticket_id, username)

            ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
            ticket_obj.participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
            ticket_obj.participant = username
            ticket_obj.save()

            # add ticket flow log
            flag, result = cls.get_ticket_all_field_value_json(ticket_id)
            if flag is False:
                return False, result
            all_ticket_data_json = result.get('all_field_value_json')
            ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion='接单处理',
                                        participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                        intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_ACCEPT,
                                        participant=username, state_id=ticket_obj.state_id, creator=username,
                                        ticket_data=all_ticket_data_json)
            cls.add_ticket_flow_log(ticket_flow_log_dict)
            return True, ''
        else:
            return False, 'participant is one people, do not accept ticket first'

    @classmethod
    @auto_log
    def deliver_ticket(cls, ticket_id: int, username: str, target_username: str, suggestion: str)->tuple:
        """
        deliver ticket to other
        :param ticket_id:
        :param username: operator username
        :param target_username: deliver to username
        :param suggestion: suggestion for deliver
        :return:
        """
        cls.update_ticket_relation(ticket_id, target_username)
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.save()
        # add flow log
        flag, result = cls.get_ticket_all_field_value_json(ticket_id)
        if flag is False:
            return False, result

        all_ticket_data_json = result.get('all_field_value_json')

        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                                    participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_DELIVER,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)

        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')

        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket(cls, ticket_id: int, username: str, target_username: str, suggestion: str):
        """
        add node to other (加签工单)
        :param ticket_id:
        :param username:
        :param target_username: add node to(加签目标人)
        :param suggestion: add node suggestion(加签处理意见)
        :return:
        """
        flag, result = cls.ticket_handle_permission_check(ticket_id, username)
        if flag is False:
            return False, result
        if result.get('permission') is False:
            return False, result.get('msg')

        cls.update_ticket_relation(ticket_id, target_username)
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.in_add_node = True
        ticket_obj.add_node_man = username
        ticket_obj.save()
        # add flow log

        flag, result = cls.get_ticket_all_field_value_json(ticket_id)

        all_ticket_data_json = result.get('all_field_value_json')
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                                    participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_ADD_NODE,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')
        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket_end(cls, ticket_id: int, username: str, suggestion: str):
        """
        add node finish(加签工单完成)
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        flag, result = cls.ticket_handle_permission_check(ticket_id, username)
        if flag is False:
            return False, result
        if result.get('permission') is False:
            return False, result.get('msg')

        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = ticket_obj.add_node_man
        ticket_obj.in_add_node = False
        ticket_obj.add_node_man = ''
        ticket_obj.save()
        # 更新关系人表
        cls.update_ticket_relation(ticket_id, ticket_obj.participant)

        # add flow log
        flag, result = cls.get_ticket_all_field_value_json(ticket_id)
        if flag is False:
            return False, result
        all_ticket_data_json = result.get('all_field_value_json')
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                                    participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_ADD_NODE_END,
                                    participant=username, state_id=ticket_obj.state_id, creator=username,
                                    ticket_data=all_ticket_data_json)
        cls.add_ticket_flow_log(ticket_flow_log_dict)

        from tasks import send_ticket_notice
        send_ticket_notice.apply_async(args=[ticket_id], queue='loonflow')
        return True, ''

    @classmethod
    @auto_log
    def handle_timer_transition(cls, ticket_id: int, destination_state_id: int)->tuple:
        """
        定时器处理
        :param ticket_id:
        :param destination_state_id:
        :return:
        """
        # 定时器处理逻辑，如果新的状态所属transition有配置定时器，那么创建一个定时器流转的任务
        flag, destination_transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(
            destination_state_id)
        if destination_transition_queryset:
            for destination_transition in destination_transition_queryset:
                if destination_transition.timer:
                    from tasks import timer_transition
                    timer_transition.apply_async(args=[ticket_id, destination_state_id, datetime.datetime.now(),
                                                       destination_transition.id],
                                                 countdown=destination_transition.timer, queue='loonflow')
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_all_field_value(cls, ticket_id: int)->tuple:
        """
        工单所有字段的值
        get ticket's all field value
        :param ticket_id:
        :return:
        """
        # 工单基础字段、工单自定义字段
        ticket_obj = TicketRecord.objects.filter(id=ticket_id).first()
        if not ticket_obj:
            return False, '工单已被删除或者不存在'
        # 获取工单基础表中的字段中的字段信息
        field_info_dict = ticket_obj.get_dict()
        # 获取自定义字段的值
        flag, result = workflow_custom_field_service_ins.get_workflow_custom_field_name_list(ticket_obj.workflow_id)
        if flag is False:
            return False, result
        ticket_custom_field_key_list = result.get('ticket_custom_field_key_list')

        for field_key in ticket_custom_field_key_list:
            flag, result = cls.get_ticket_field_value(ticket_id, field_key)
            if flag is False:
                return False, result
            field_info_dict[field_key] = result.get('value')
        return True, field_info_dict

    @classmethod
    @auto_log
    def get_ticket_all_field_value_json(cls, ticket_id: int) -> tuple:
        """
        get ticket all field value to json
        :param ticket_id:
        :return:
        """
        flag, result = cls.get_ticket_all_field_value(ticket_id)
        if flag is False:
            return False, result

        for key, value in result.items():
            if type(value) not in [int, str, bool, float]:
                result[key] = str(result[key])
        return True, dict(all_field_value_json=json.dumps(result))

    @classmethod
    @auto_log
    def retry_ticket_script(cls, ticket_id: int, username: str)->tuple:
        """
        重新执行工单脚本，或重新触发hook
        retry ticket script or hook
        :param ticket_id:
        :param username:
        :return:
        """
        # 判断工单表记录中最后一次脚本是否执行失败了，即script_run_last_result的值
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, 'Ticket is not existed or has been deleted'
        # if ticket_obj.participant_type_id is not CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
        #     return False, "The ticket's participant_type is not robot, do not allow retry"

        if ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
            # 先重置上次执行结果
            ticket_obj.script_run_last_result = True
            ticket_obj.save()
            from tasks import run_flow_task  # 放在文件开头会存在循环引用问题
            run_flow_task.apply_async(args=[ticket_id, ticket_obj.participant, ticket_obj.state_id,
                                            '{}_retry'.format(username)], queue='loonflow')
            return True, ''
        elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
            ticket_obj.script_run_last_result = True
            ticket_obj.save()
            from tasks import flow_hook_task
            flow_hook_task.apply_async(args=[ticket_id], queue='loonflow')
            return True, ''
        else:
            return False, "The ticket's participant_type is not robot or hook, do not allow retry"

    @classmethod
    @auto_log
    def get_ticket_state_last_man(cls, ticket_id: int, state_id: int)->tuple:
        """
        获取工单状态最后一次的处理人
        get the last handler to ticket's state
        :param ticket_id:
        :param state_id:
        :return:
        """
        flow_log_queryset = TicketFlowLog.objects.filter(ticket_id=ticket_id, state_id=state_id,
                                                         is_deleted=0).order_by('-id')
        if flow_log_queryset:
            last_flow_log = flow_log_queryset[0]
            if last_flow_log.participant_type_id == 1:
                # 为个人时才生效
                return True, dict(last_man=last_flow_log.participant)
            else:
                return True, dict(last_man='', msg='handle_man is not personal')
        return True, dict(last_man='', msg='the state has not handle man before')

    @classmethod
    @auto_log
    def get_ticket_count_by_args(cls, workflow_id: int=0, username: str='', period: int=0)->tuple:
        """
        获取工单的个数
        get ticket's count by hour period
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
        return True, dict(count_result=count_result)

    @classmethod
    @auto_log
    def get_ticket_state_participant_info(cls, state_id: int, ticket_id: int=0, ticket_req_dict: dict={})->tuple:
        """
        获取工单状态实际的新处理人
        get ticket's new participant by state_id
        :param state_id:
        :param ticket_id: new ticket if no ticket id
        :param ticket_req_dict:
        :return:
        """
        if ticket_id:
            flag, ticket_obj = cls.get_ticket_by_id(ticket_id)
            if not flag:
                return False, ticket_obj
            # 初始状态判断
            flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(state_id)
            if state_obj.type_id == constant_service_ins.STATE_TYPE_START:
                # 回到初始状态，目标处理人应该为工单的发起人
                return True, dict(destination_participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                  destination_participant=ticket_obj.creator,
                                  multi_all_person="{}")
            elif state_obj.type_id == constant_service_ins.STATE_TYPE_END:
                # 回到结束状态，目标处理人应该为空
                return True, dict(destination_participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                  destination_participant='',
                                  multi_all_person="{}")
            parent_ticket_id = ticket_obj.parent_ticket_id
            creator = ticket_obj.creator
            multi_all_person = json.loads(ticket_obj.multi_all_person)
        else:
            # 新建工单
            flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(state_id)
            if state_obj.type_id == constant_service_ins.STATE_TYPE_START:
                # 回到初始状态，目标处理人应该为工单的发起人
                return True, dict(destination_participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                  destination_participant=ticket_req_dict.get('username'),
                                  multi_all_person="{}")
            elif state_obj.type_id == constant_service_ins.STATE_TYPE_END:
                # 回到结束状态，目标处理人应该为空
                return True, dict(destination_participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                  destination_participant='',
                                  multi_all_person="{}")
            parent_ticket_id = ticket_req_dict.get('parent_ticket_id')
            creator = ticket_req_dict.get('username')
            multi_all_person = "{}"

        participant_type_id, participant = state_obj.participant_type_id, state_obj.participant
        destination_participant_type_id, destination_participant = participant_type_id, participant

        if participant_type_id == constant_service_ins.PARTICIPANT_TYPE_FIELD:
            if not ticket_id:
                # ticket_id 不存在，则为新建工单，从请求的数据中获取
                participant_list = participant.split(',')
                destination_participant_list = []
                for participant0 in participant_list:
                    destination_participant_list.append(ticket_req_dict.get(participant0, ''))

                destination_participant = ','.join(destination_participant_list)
            else:
                # 工单存在，先判断是否有修改此字段的权限，如果有且字段值有提供，则取提交的值
                flag, field_info = cls.get_state_field_info(ticket_obj.state_id)
                update_field_list = field_info.get('update_field_list')

                flag, ticket_value_info = cls.get_ticket_all_field_value(ticket_id)

                participant_list = participant.split(',')
                destination_participant_list = []
                for participant0 in participant_list:

                    if participant0 in update_field_list and ticket_req_dict.get(participant0):
                        # 请求数据中包含需要的字段则从请求数据中获取
                        destination_participant_list.append(ticket_req_dict.get(participant0))
                    else:
                        # 处理工单时未提供字段的值,则从工单当前字段值中获取
                        destination_participant_list.append(ticket_value_info.get(participant0))
                destination_participant = ','.join(destination_participant_list)

            destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PARENT_FIELD:

            flag, ticket_value_info = cls.get_ticket_all_field_value(parent_ticket_id)

            participant_list = participant.split(',')
            destination_participant_list = []
            for participant0 in participant_list:
                destination_participant_list.append(ticket_value_info.get(participant0))
            destination_participant = ','.join(destination_participant_list)
            destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_VARIABLE:
            participant_list = participant.split(',')
            destination_participant_list = []
            for participant0 in participant_list:
                if participant0 == 'creator':
                    destination_participant_list.append(creator)
                elif participant0 == 'creator_tl':
                    flag, approver = account_base_service_ins.get_user_dept_approver(creator)
                    if flag is False:
                        return False, approver
                    destination_participant_list.append(approver)
            destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
            destination_participant = ','.join(destination_participant_list)

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            # 支持多部门
            flag, destination_participant_list = account_base_service_ins.get_dept_username_list(
                destination_participant)
            destination_participant = ','.join(destination_participant_list)
            destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
            if flag is False:
                return False, destination_participant_list
        elif destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            flag, destination_participant_list = account_base_service_ins.get_role_username_list(
                int(destination_participant))
            destination_participant = ','.join(destination_participant_list)
            destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
            if flag is False:
                return False, destination_participant_list

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_HOOK:
            destination_participant = '***'  # 敏感数据，不保存工单基础表中

        elif participant_type_id == constant_service_ins.PARTICIPANT_TYPE_FROM_EXTERNAL:
            import requests
            external_config = json.loads(participant)
            external_url = external_config.get('external_url')
            external_token = external_config.get('external_token')
            extra_info = external_config.get('extra_info')

            flag, msg = common_service_ins.gen_hook_signature(external_token)
            if not flag:
                return False, msg
            if not ticket_id:
                all_ticket_data = ticket_req_dict
            else:
                flag, all_ticket_data = ticket_base_service_ins.get_ticket_all_field_value(ticket_id)
            if extra_info is not None:
                all_ticket_data.update(dict(extra_info=extra_info))
            try:
                r = requests.post(external_url, headers=msg, json=all_ticket_data, timeout=10)
                result = r.json()  # {code:0, msg:'', data:'zhangsan,lisi'}
                if len(result.get('data').split(',')) > 1:
                    destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_MULTI
                else:
                    destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
                destination_participant = result.get('data')
            except Exception as e:
                import logging
                import traceback
                logger = logging.getLogger('django')
                logger.error('get external participant error:')
                logger.error(traceback.format_exc())
                destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONA
                destination_participant = 'admin'

        # 参与人去重复+类型修正
        if destination_participant_type_id in (constant_service_ins.PARTICIPANT_TYPE_PERSONAL, constant_service_ins.PARTICIPANT_TYPE_MULTI):
            destination_participant_list = destination_participant.split(',')
            destination_participant_list = list(set(destination_participant_list))
            if len(destination_participant_list) > 1:
                destination_participant_type_id = constant_service_ins.PARTICIPANT_TYPE_MULTI
            destination_participant = ','.join(destination_participant_list)

        if destination_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            if state_obj.distribute_type_id == constant_service_ins.STATE_DISTRIBUTE_TYPE_RANDOM:
                destination_participant = random.sample(destination_participant, 1)[0]
            elif state_obj.distribute_type_id == constant_service_ins.STATE_DISTRIBUTE_TYPE_ALL:
                multi_all_person_dict = {}
                for destination_participant_0 in destination_participant.split(','):
                    multi_all_person_dict[destination_participant_0] = {}
                multi_all_person = json.dumps(multi_all_person_dict)

        return True, dict(destination_participant_type_id=destination_participant_type_id,
                          destination_participant=destination_participant,
                          multi_all_person=multi_all_person)

    @classmethod
    @auto_log
    def get_state_field_info(cls, state_id: int)->tuple:
        """
        获取状态字段信息
        get state's field config
        :param state_id:
        :return:
        """
        flag, state_obj = workflow_state_service_ins.get_workflow_state_by_id(state_id)
        if flag is False:
            return False, state_obj

        state_field_dict = json.loads(state_obj.state_field_str)
        require_field_list, update_field_list = [], []
        for key, value in state_field_dict.items():
            if value == constant_service_ins.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
                update_field_list.append(key)
            if value == constant_service_ins.FIELD_ATTRIBUTE_OPTIONAL:
                update_field_list.append(key)
        return True, dict(require_field_list=require_field_list, update_field_list=update_field_list)

    @classmethod
    @auto_log
    def get_next_state_id_by_transition_and_ticket_info(cls, ticket_id: int=0, ticket_req_dict: dict={})->tuple:
        """
        获取工单的下个状态id,需要考虑条件流转的情况
        get ticket's next state_id by transition
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
            flag, start_state = workflow_state_service_ins.get_workflow_start_state(workflow_id)
            if flag is False:
                return False, start_state
            source_state_id = start_state.id
        else:
            # 已经存在的工单，直接获取工单当前状态
            flag, ticket_obj = cls.get_ticket_by_id(ticket_id)
            source_state_id = ticket_obj.state_id

        flag, transition_queryset = workflow_transition_service_ins.get_transition_by_args(
            dict(source_state_id=source_state_id, id=transition_id))
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
                flag, ticket_all_value_dict = cls.get_ticket_all_field_value(ticket_id)
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
                # 为了安全考虑，仅支持datetime, time, abs. 如果你需要其他库函数，可参考datetime、abs这些自行添加
                if eval(expression_format, {'__builtins__': None}, {'datetime': datetime, 'time': time, 'abs': abs}):
                    destination_state_id = condition_expression0.get('target_state_id')
                    break

        return True, dict(destination_state_id=destination_state_id)

    @classmethod
    @auto_log
    def add_comment(cls, ticket_id: int=0, username: str='', suggestion: str='')->tuple:
        """
        添加评论
        add comment to ticket
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        if not (ticket_id and username):
            return False, 'ticket_id and username should not be null'

        flag, all_ticket_data = cls.get_ticket_all_field_value(ticket_id)
        # date等格式需要转换为str
        for key, value in all_ticket_data.items():
            if type(value) not in [int, str, bool, float]:
                all_ticket_data[key] = str(all_ticket_data[key])

        all_ticket_data_json = json.dumps(all_ticket_data)
        new_flow_log = dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                            participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                            participant=username, state_id=all_ticket_data.get('state_id'),
                            intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_COMMENT,
                            ticket_data=all_ticket_data_json, creator=username)

        flag, msg = cls.add_ticket_flow_log(new_flow_log)
        if flag is False:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def hook_call_back(cls, ticket_id: int, app_name: str, request_data_dict: dict)->tuple:
        """
        hook回调
        :param ticket_id:
        :param app_name:
        :param request_data_dict:
        :return:
        """
        # 校验请求app_name是否有hook回调该工单权限
        flag, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not flag:
            return False, msg
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()

        # 检查工单处理人类型为hook中
        if ticket_obj.participant_type_id != constant_service_ins.PARTICIPANT_TYPE_HOOK:
            return False, '工单当前处理人类型非hook，不执行回调操作'

        result = request_data_dict.get('result', True)
        msg = request_data_dict.get('msg', '')
        field_value = request_data_dict.get('field_value', {})  # 用于更新字段

        if not result:
            # hook执行失败了，记录失败状态.以便允许下次再执行
            cls.update_ticket_field_value(ticket_id,{'script_run_last_result': False})
            # 记录错误信息
            flag, result_data = ticket_base_service_ins.get_ticket_all_field_value_json(ticket_id)
            all_ticket_data_json = result_data.get('all_field_value_json')

            ticket_base_service_ins.add_ticket_flow_log(
                dict(ticket_id=ticket_id, transition_id=0, suggestion=msg,
                     intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_HOOK,
                     participant_type_id=constant_service_ins.PARTICIPANT_TYPE_HOOK,
                     participant='hook', state_id=ticket_obj.state_id, ticket_data=all_ticket_data_json,
                     creator='hook'))
            return True, ''

        state_id = ticket_obj.state_id
        flag, transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(state_id)
        transition_id = transition_queryset[0].id  # hook状态只支持一个流转

        new_request_dict = field_value

        new_request_dict.update({'transition_id': transition_id, 'suggestion': msg, 'username': 'loonrobot'})

        # 执行流转
        flag, msg = cls.handle_ticket(ticket_id, new_request_dict, by_timer=False, by_task=False, by_hook=True)
        if not flag:
            return False, msg
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_participant_info(cls, ticket_id: int)->tuple:
        """
        获取工单当前详细参与人信息
        get ticket's now participant info
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        from apps.account.models import LoonUser
        participant_username_list, participant_info_list = [], []

        if ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
            participant_username_list = [ticket_obj.participant]
        elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            participant_username_list = ticket_obj.participant.split(',')
        elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
            flag, participant_username_list = account_base_service_ins.get_role_username_list(ticket_obj.participant)
            if flag is False:
                return False, participant_username_list

        elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
            flag, participant_username_list = account_base_service_ins.get_dept_username_list(ticket_obj.participant)
            if flag is False:
                return False, participant_username_list

        if participant_username_list:
            participant_queryset = LoonUser.objects.filter(username__in=participant_username_list, is_deleted=0)
            for participant_0 in participant_queryset:
                participant_info_list.append(dict(username=participant_0.username, alias=participant_0.alias,
                                                  phone=participant_0.phone, email=participant_0.email))
        return True, dict(participant_username_list=participant_username_list,
                          participant_info_list=participant_info_list)

    @classmethod
    @auto_log
    def close_ticket(cls, ticket_id: int, username: str, suggestion: str)->tuple:
        """
        关闭工单
        close ticket: set state to end state
        :param ticket_id:
        :param username:
        :param suggestion:处理意见
        :return:
        """
        # 获取工单详细信息
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, '工单不存在或已被删除'
        workflow_id = ticket_obj.workflow_id
        # 查询工作流的结束状态
        flag, state_obj = workflow_state_service_ins.get_workflow_end_state(workflow_id)
        if flag is False:
            return False, state_obj

        # 新增流转记录
        # 获取工单所有字段的值
        flag, result = cls.get_ticket_all_field_value_json(ticket_id)
        if flag is False:
            return False, result
        all_ticket_data_json = result.get('all_field_value_json')
        ticket_flow_log_dict = dict(ticket_id=ticket_id, transition_id=0, suggestion='强制关闭工单:{}'.format(suggestion),
                                    participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                    intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_CLOSE,
                                    participant=username, state_id=state_obj.id, ticket_data=all_ticket_data_json,
                                    )

        new_state_id = state_obj.id
        ticket_obj.state_id = new_state_id
        ticket_obj.participant_type_id = 0
        ticket_obj.participant = ''
        ticket_obj.act_state_id = constant_service_ins.TICKET_ACT_STATE_CLOSED
        ticket_obj.save()
        # 更新ticketuser中in_process状态
        TicketUser.objects.filter(ticket_id=ticket_id, is_deleted=0).update(in_process=False)

        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def delete_ticket(cls, ticket_id: int, username: str, suggestion: str)->tuple:
        """
        删除工单，建议仅用于管理干预删除工单
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        flag, result = cls.get_ticket_by_id(ticket_id)
        if flag is False:
            return False, result

        flag, result_data = ticket_base_service_ins.get_ticket_all_field_value_json(ticket_id)
        all_ticket_data_json = result_data.get('all_field_value_json')

        ticket_base_service_ins.add_ticket_flow_log(
            dict(ticket_id=ticket_id, transition_id=0, suggestion=suggestion,
                 intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_DELETE,
                 participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                 participant=username, state_id=result.state_id, ticket_data=all_ticket_data_json, creator=username))

        result.is_deleted = True
        result.save()
        return True, ''

    @classmethod
    @auto_log
    def ticket_admin_permission_check(cls, ticket_id: int = 0, username: str = '') -> tuple:
        """
        校验用户是否是该工单的工作流管理员,以判断是否有权限对该工单干预处理
        :param username:
        :param ticket_id:
        :return:
        """
        # 超级管理员拥有所有工作流管理权限
        flag, result = account_base_service_ins.get_user_by_username(username)
        if flag is False:
            return False, result
        if result.type_id == constant_service_ins.ACCOUNT_TYPE_WORKFLOW_ADMIN:
            return True, "admin user has all ticket's intervention manage permission"

        flag, result = cls.get_ticket_by_id(ticket_id)
        if flag is False:
            return False, result
        workflow_id = result.workflow_id
        flag, result = workflow_base_service_ins.get_workflow_manage_list(username)
        if flag is False:
            return False, result
        workflow_list = result.get('workflow_list')
        workflow_id_list = [workflow['id'] for workflow in workflow_list]
        if workflow_id in workflow_id_list:
            return True, ''
        else:
            return False, 'user has no permission to manage this ticket'

    @classmethod
    @auto_log
    def get_ticket_num_statistics(cls, start_date: str='', end_date: str='', username: str='') ->tuple:
        """
        工单统计
        :param start_date:
        :param end_date:
        :param username:
        :return:
        """
        # 获取用户有权限的工作流
        flag, result = workflow_base_service_ins.get_workflow_manage_list(username)
        if flag is False:
            return False, result
        workflow_list = result.get('workflow_list')
        workflow_id_list = [workflow.get('id') for workflow in workflow_list]
        from django.db.models import Count
        query_params = {'is_deleted': 0, 'workflow_id__in': workflow_id_list}
        if start_date:
            query_params['gmt_gte'] = start_date
        if end_date:
            query_params['gmt_gte'] = end_date

        queryset_result = TicketRecord.objects.filter(**query_params).extra(
            select={'year': 'year(gmt_created)', 'month': 'month(gmt_created)', 'day': 'day(gmt_created)',
                    'workflow_id': 'workflow_id'}).values('year', 'month', 'day', 'workflow_id').annotate(
            count_len=Count('gmt_created')).order_by()

        workflow_id_dict = {}
        for workflow in workflow_list:
            workflow_id_dict[workflow.get('id')] = workflow

        result_list = []
        for queryset in queryset_result:
            date_str = '%d-%02d-%02d' % (queryset['year'], queryset['month'], queryset['day'])
            workflow_name = workflow_id_dict[queryset['workflow_id']]['name']
            result_list.append(dict(day=date_str, type=workflow_name, count=queryset['count_len']))
        # 按日期排序
        result_list = sorted(result_list, key=lambda r: r['day'])

        return True, dict(result_list=result_list)

    @classmethod
    @auto_log
    def retreat_ticket(cls, ticket_id: int, username: str='', suggestion: str='')->tuple:
        """
        撤回工单
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        # 判断用户是否有撤回权限，工单的创建人，且当前状态允许撤回
        flag, ticket_result = cls.get_ticket_by_id(ticket_id)
        if flag is False:
            return False, ticket_result
        if ticket_result.creator != username:
            return False, "just ticket's creator can retreat ticket in specific state that enable retreat"
        workflow_id = ticket_result.workflow_id
        flag, result = workflow_state_service_ins.get_workflow_state_by_id(ticket_result.state_id)
        if flag is False:
            return False, result
        if result.enable_retreat is False:
            return False, 'now state can not be retreat'
        flag, result = workflow_state_service_ins.get_workflow_start_state(workflow_id)
        if flag is False:
            return False, result

        ticket_result.state_id = result.id
        ticket_result.participant_type_id = constant_service_ins.PARTICIPANT_TYPE_PERSONAL
        ticket_result.participant = ticket_result.creator
        ticket_result.act_state_id = constant_service_ins.TICKET_ACT_STATE_RETREAT
        ticket_result.save()

        cls.update_ticket_relation(ticket_id, ticket_result.creator)

        # 新增操作记录
        flag, result = cls.get_ticket_all_field_value_json(ticket_result.id)
        if flag is False:
            return False, result

        all_ticket_data_json = result.get('all_field_value_json')
        new_ticket_flow_log_dict = dict(ticket_id=ticket_result.id, transition_id=0, suggestion=suggestion,
                                        intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_RETREAT,
                                        participant_type_id=constant_service_ins.PARTICIPANT_TYPE_PERSONAL,
                                        participant=username, state_id=ticket_result.state_id,
                                        ticket_data=all_ticket_data_json
                                        )
        cls.add_ticket_flow_log(new_ticket_flow_log_dict)
        return True, ''

    def close_ticket_permission_check(cls, ticket_id: int, username: str)->tuple:
        """
        用户是否有强制关闭工单的权限
        :param ticket_id:
        :param username:
        :return:
        """
        # 强制关闭工单需要对应工作流的管理员或者超级管理员 或者处于初始状态的工单由创建人直接关闭
        flag, result = ticket_base_service_ins.ticket_admin_permission_check(ticket_id, username)
        if flag is False:
            # 判断是否属于初始状态 且用户为工单创建人
            flag, ticket_result = cls.get_ticket_by_id(ticket_id)
            if flag is False:
                return False, ticket_result
            workflow_id = ticket_result.workflow_id
            flag, start_state_result = workflow_state_service_ins.get_workflow_start_state(workflow_id)
            if flag is False:
                return False,  start_state_result
            if ticket_result.creator == username and ticket_result.state_id == start_state_result.id:
                return True, "ticket's creator can close ticket in start state"
            else:
                return False, "just ticket's creator can close ticket in start state or workflow_admin can close ticket in any state"
        else:
            return True, "ticket's workflow admin casn close ticket in any state"

    @classmethod
    def upload_file(cls, request: any)->tuple:
        import os, uuid
        file_obj = request.FILES.get('file')
        source_file_name = file_obj.name
        source_file_type = source_file_name.split('.')[-1]
        file_name = str(uuid.uuid1()) + '.' + source_file_type

        f = open(os.path.join(settings.MEDIA_ROOT, 'ticket_file/{}'.format(file_name)), 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return True, dict(file_name=file_name, file_path='/media/ticket_file/{}'.format(file_name), source_file_name=source_file_name)


ticket_base_service_ins = TicketBaseService()
