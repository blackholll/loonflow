import copy
import json
import datetime
import logging
import random

import redis
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Component, Record as WorkflowRecord, Hook as WorkflowHook
from apps.ticket.models import Record as TicketRecord, CustomField, User as TicketUser, Node as TicketNode
from service.account.account_dept_service import account_dept_service_ins
from service.account.account_role_service import account_role_service_ins
from service.account.account_user_service import account_user_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.hook.hook_base_service import hook_base_service_ins
from service.redis_pool import POOL
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.common.common_service import common_service_ins
from service.common.constant_service import constant_service_ins
from service.account.account_base_service import account_base_service_ins
from service.ticket.ticket_field_service import ticket_field_service_ins
from service.ticket.ticket_flow_history_service import ticket_flow_history_service_ins
from service.ticket.ticket_node_service import ticket_node_service_ins
from service.ticket.ticket_user_service import ticket_user_service_ins
from service.workflow.workflow_base_service import workflow_base_service_ins
from service.workflow.workflow_hook_service import workflow_hook_service_ins
from service.workflow.workflow_node_service import workflow_node_service_ins
from service.workflow.workflow_edge_service import workflow_edge_service_ins
from service.workflow.workflow_permission_service import workflow_permission_service_ins
from service.workflow.workflow_component_service import workflow_component_service_ins


class TicketBaseService(BaseService):
   
    @classmethod
    def get_ticket_by_id(cls, tenant_id:str, ticket_id: str):
        """
        get ticket record
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        return TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)


    @classmethod
    def get_ticket_list(cls, tenant_id:str='', search_value: str='', user_id: str='', creator_id: str='', create_start: str='', create_end: str='',
                        workflow_ids: str='', node_ids: str='', ticket_ids: str='', category: str='', reverse: int=1,
                        per_page: int=10, page: int=1, app_name: str='', **kwargs):
        """
        ticket list
        :param tenant_id:
        :param search_value:
        :param user_id:
        :param creator_id:
        :param create_start:
        :param create_end:
        :param workflow_ids: workflow ids, join with ','
        :param node_ids: node_ids, join with ','
        :param ticket_ids: ticket id, join with ','
        :param category:
        :param reverse:  order by create time
        :param per_page:
        :param page:
        :param app_name:
        act_state: in_draft,in_process,refused,revoked,end,closed
        :return:
        """
        category_list = ['all', 'owner', 'duty', 'relation', 'worked', 'view', 'intervene']
        if category not in category_list:
            return False, 'category value is invalid, it should be in all, owner, duty, relation'
        query_params = Q(tenant_id=tenant_id)
        # get granted workflow_id_list base by app_name
        from service.workflow.workflow_permission_service import workflow_permission_service_ins
        app_workflow_id_list = workflow_permission_service_ins.get_workflow_id_list_by_permission('api', 'app', app_name)
        if not app_workflow_id_list:
            return dict(ticket_result_restful_list=[], paginator_info=dict(per_page=per_page, page=page, total=0))
         
        if creator_id:
            query_params &= Q(creator_id=creator_id)
        if kwargs.get('act_state'):
            query_params &= Q(act_state=kwargs.get('act_state'))

        if kwargs.get('creator'):
            query_params &= Q(creator=kwargs.get('creator'))
        if kwargs.get('parent_ticket_id'):
            query_params &= Q(parent_ticket_id=kwargs.get('parent_ticket_id'))
        if kwargs.get('parent_ticket_state_id'):
            query_params &= Q(parent_ticket_state_id=kwargs.get('parent_ticket_state_id'))


        if search_value:
            query_params &= Q(title__contains=search_value)
        if create_start:
            query_params &= Q(created_at__gte=create_start)
        if create_end:
            query_params &= Q(created_at__lte=create_end)
        if workflow_ids:
            workflow_id_str_list = workflow_ids.split(',')
            query_workflow_id_list = [workflow_id_str for workflow_id_str in workflow_id_str_list]
        else:
            query_workflow_id_list = []

        if node_ids:
            node_id_list = node_ids.split(',')
            query_params &= Q(node_id__in=node_id_list)
        if ticket_ids:
            ticket_id_str_list = ticket_ids.split(',')
            ticket_id_list = [int(ticket_id_str) for ticket_id_str in ticket_id_str_list]
            query_params &= Q(id__in=ticket_id_list)

        if query_workflow_id_list:
            final_workflow_id_list = list(set(app_workflow_id_list) - (set(app_workflow_id_list) - set(query_workflow_id_list)))
        else:
            final_workflow_id_list = app_workflow_id_list

        query_params &= Q(workflow_id__in=final_workflow_id_list)

        if reverse:
            order_by_str = '-created_at'
        else:
            order_by_str = 'created_at'
        
        if category == 'owner':
            query_params &= Q(creator_id=user_id)
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'duty':
            duty_query_expression = Q(ticket_user__as_assignee=True, ticket_user__user_id=user_id)
            query_params &= duty_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'relation':
            relation_query_expression = Q(ticket_user__user_id=user_id)
            query_params &= relation_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'worked':
            worked_query_expression = Q(ticket_user__user_id=user_id, ticket_user__as_processor=True)
            query_params &= worked_query_expression
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
        elif category == 'intervene':
            category_workflow_id_list = workflow_permission_service_ins.get_workflow_id_list_by_permission('dispatcher', 'user', user_id)
            query_params &= Q(workflow_id__in=category_workflow_id_list)
            # ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str)
        elif category in ('view'):
            category_workflow_id_list = workflow_permission_service_ins.get_workflow_id_list_by_permission(category, 'user', user_id)
            if category == 'view':
                parent_department_id_list = account_user_service_ins.get_user_parent_dept_id_list(tenant_id, user_id)
                if parent_department_id_list:
                    view_department_workflow_id_list = workflow_permission_service_ins.get_workflow_id_list_by_permission(
                            category, 'department', ','.join(parent_department_id_list))
                    category_workflow_id_list = list(set(category_workflow_id_list).union(set(view_department_workflow_id_list)))
            query_params &= Q(workflow_id__in=category_workflow_id_list)
            # ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
            ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str)
        else:
            # category is all, only admin can get all tickets
            user_obj = account_user_service_ins.get_user_by_user_id(tenant_id, user_id)
            if user_obj.type != 'admin':
                raise CustomCommonException("only admin can get all tickets")
            # ticket_objects = TicketRecord.objects.filter(query_params).order_by(order_by_str).distinct()
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
        # 将模型对象转换为可序列化的字典
        ticket_result_restful_list = []
        for ticket_obj in ticket_result_object_list:
            try:
                ticket_result_restful_list.append(ticket_obj.get_dict())
            except Exception:
                # 兜底：至少返回基础字段，避免序列化失败
                ticket_result_restful_list.append(dict(id=str(getattr(ticket_obj, 'id', '')), title=getattr(ticket_obj, 'title', ''), act_state=getattr(ticket_obj, 'act_state', '')))

        return dict(ticket_result_restful_list=ticket_result_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @transaction.atomic
    def new_ticket(cls, tenant_id: str, app_name: str, operator_id: str,  request_data_dict: dict)->int:
        """
        new ticket
        :param tenant_id:
        :param app_name:
        :param operator_id:
        :param request_data_dict:
        :return:
        """
        workflow_id = request_data_dict.get('workflow_id')
        cc_to_user_id_list = request_data_dict.get('cc_to_user_id_list', [])
        # get version id
        workflow_version = request_data_dict.get('workflow_version', '')
        version_id = workflow_base_service_ins.get_workflow_version_id_by_name(workflow_id, tenant_id, workflow_version)

        # pre-create hook shoule be called synchronous
        from tasks import flow_action_hook_task
        flow_action_hook_task(tenant_id, '', "pre_create", request_data_dict.get('workflow_id', ''), version_id)

        # check whether current call source has permission to create this type ticket
        workflow_permission_service_ins.app_workflow_permission_check(tenant_id, workflow_id, version_id, app_name)
        # pre_create_hook check
        workflow_hook_service_ins.pre_create_hook(tenant_id, operator_id, workflow_id, version_id, request_data_dict)

        action_id = request_data_dict.get('action_id')
        parent_ticket_id = request_data_dict.get('parent_ticket_id', '')
        parent_ticket_node_id = request_data_dict.get('parent_ticket_node_id', '')
        


        # required field check
        edge_obj = workflow_edge_service_ins.get_workflow_edge_by_id(tenant_id, workflow_id, version_id, action_id)
        validate_fields = edge_obj.props.get('validate_fields', True)

        ## get start node id
        required_field_list, update_field_list = [], []
        start_node_obj = workflow_node_service_ins.get_init_node(tenant_id, workflow_id, version_id)

        ## startnode and action match check
        if start_node_obj.id != edge_obj.source_node_id:
            raise CustomCommonException("start node and action not match")
        


        field_permissions = start_node_obj.props.get('field_permissions', {})
        for field_key, field_permission in field_permissions.items():
            if field_permission == 'required':
                required_field_list.append(field_key)
                update_field_list.append(field_key)
            elif field_permission == 'optional':
                update_field_list.append(field_key)
        
        if validate_fields:
            for required_field in required_field_list:
                if required_field not in request_data_dict.get('fields', {}).keys():
                    raise CustomCommonException('field {} is required'.format(required_field))
        

        # get next node list. next node can be more than one
        next_node_dict_list = cls.get_action_next_node_dict_list(tenant_id, '', operator_id, workflow_id, version_id, action_id, request_data_dict)
        act_state = "on_going"
        if len(next_node_dict_list) == 1:
            act_state = cls.get_act_state_by_node_and_edge_type(next_node_dict_list[0].get("type"), edge_obj.type)
        
        # title need check whether title need auto genirate
        title = workflow_component_service_ins.get_title_from_template(tenant_id, workflow_id, version_id, request_data_dict.get('fields', {}))

        ticket_record = TicketRecord(title=title, workflow_id=workflow_id,
                                     parent_ticket_id=parent_ticket_id,
                                     parent_ticket_node_id=parent_ticket_node_id,
                                     act_state=act_state, creator_id=operator_id, tenant_id=tenant_id,
                                     workflow_version_id=version_id)
        ticket_record.save()
        ticket_id = ticket_record.id

        # add ticket cc_to user record
        ticket_user_service_ins.add_record(tenant_id, operator_id, ticket_id, True, False, False, False)
        if request_data_dict.get("cc_to_list"):
            for cc_to in request_data_dict.get("cc_to_list"):
                ticket_user_service_ins.add_record(tenant_id, cc_to, ticket_id, False, False, False, True)

        # add ticket flow history
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "create", action_id,
                                                                request_data_dict.get("action_props", {}).get("comment", ""), "user", str(operator_id),
                                                                start_node_obj.id,
                                                                request_data_dict.get('fields', {}))
        # add ticket custom field
        for_update_field = {}
        for field_key, field_value in request_data_dict.get('fields', {}).items():
            if field_key in update_field_list:
                for_update_field[field_key] = field_value
        ticket_field_service_ins.update_ticket_fields(tenant_id, ticket_id, operator_id, workflow_id, version_id, for_update_field)

        # update TicketNode
        next_ticket_node_result_list  = []
        for next_node_dict in next_node_dict_list:
            if next_node_dict.get("keep_previous"):
                # use previous ticket_node info
                next_node_record = ticket_node_service_ins.get_ticket_node_by_node_id(tenant_id, ticket_id, next_node_dict.get("id"))
                next_node_result = next_node_record.get_dict()
                next_node_result['node_id'] = next_node_record.node_id
                next_node_result['parallel_node_id'] = next_node_record.parallel_node_id
                next_ticket_node_result_list.append(next_node_result)
            else:
                next_node_result = dict()
                next_node_assignee_info = cls.get_ticket_node_assignee_info_by_node_id(tenant_id, operator_id, next_node_dict.get("id"), '', request_data_dict)
                next_node_result['ticket_id'] = ticket_id
                next_node_result['node_id'] = next_node_dict.get("id")
                next_node_result['node_type'] = next_node_dict.get("type")
                next_node_result['is_active'] = True
                next_node_result['hook_state'] = ""
                next_node_result['in_parallel'] = next_node_dict.get("in_parallel", False)
                next_node_result['parallel_node_id'] = next_node_dict.get("parallel_node_id")
                
                next_node_result['all_assignee_result'] = next_node_assignee_info.get("all_assignee_result")
                next_node_result['target_assignee_type'] = next_node_assignee_info.get("target_assignee_type")
                next_node_result['target_assignee_list'] = next_node_assignee_info.get("target_assignee_list")
                next_node_result['in_accept_wait'] = next_node_assignee_info.get("in_accept_wait", False)
                next_ticket_node_result_list.append(next_node_result)

        ticket_node_service_ins.update_ticket_node_record(tenant_id, operator_id, next_ticket_node_result_list)

        # update relate user for next node
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, cc_to_user_id_list, next_ticket_node_result_list)



        # send notice
        from tasks import flow_notification_task
        for next_ticket_node_result0 in next_ticket_node_result_list:
            if not next_ticket_node_result0.get('keep_previous', False):
                transaction.on_commit(lambda: flow_notification_task.apply_async(args=[tenant_id, ticket_id, next_ticket_node_result0.get("id")], queue='loonflow'))

        # flow hook
        for next_ticket_node_result in next_ticket_node_result_list:
            if next_ticket_node_result.get("type") == "hook":
                from tasks import flow_hook_task
                transaction.on_commit(lambda: flow_hook_task.apply_async(args=[tenant_id, ticket_id, next_ticket_node_result.get("id")], queue='loonflow'))

        # event hook
        from tasks import flow_action_hook_task
        transaction.on_commit(lambda: flow_action_hook_task.apply_async(args=[tenant_id, ticket_id, "create"], queue='loonflow'))
        
        # todo:parent_ticket handle
        return str(ticket_id)


    @classmethod
    def get_act_state_by_node_and_edge_type(cls, node_type, edge_type):
        if edge_type == "reject":
            return "rejected"
        if node_type == "start":
            return "in_draft"
        elif node_type == "end":
            return "finished"
        else:
            return "on-going"

    @classmethod
    def get_action_next_node_dict_list(cls, tenant_id: str, ticket_id: str, operator_id: str, workflow_id: str, version_id: str, action_id: str, request_data_dict: dict) -> list:
        """
        get next node
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param workflow_id:
        :param version_id:
        :param action_id:
        :return:
        """
        # if ticket_id is '', which means now is creating ticket, so get start node and with transition id to calculate next nodes
        # if ticket_id is not '', get ticket's current node, then with transition id to calculate next nodes
        # todo: need consider in_parallel, if node in parallel, and not current source node, then also return them
        # todo: add in-parallel node, then remove current node

        result_node_list = []
        edge_obj = workflow_edge_service_ins.get_workflow_edge_by_id(tenant_id, workflow_id, version_id, action_id)

        if not ticket_id:
            previous_ticket_node_list = []
            
        else:
            source_node_id = request_data_dict.get('action_props', {}).get('node_id')
            previous_ticket_node_list = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
        
            if str(edge_obj.source_node_id) != source_node_id:
                raise CustomCommonException("current node has no permission to run this transition")
            # whole assignment strategy need consider all previous node
            all_assignee_finished = True
            for previous_ticket_node in previous_ticket_node_list:
                if str(previous_ticket_node.node_id) == source_node_id:
                    now_all_assignee_result = previous_ticket_node.all_assignee_result
                    if now_all_assignee_result:
                        now_all_assignee_result[operator_id] = {"action_id": action_id}
                    for key, value in now_all_assignee_result.items():
                        if not value:
                            all_assignee_finished = False
                            break
            if not all_assignee_finished:
                for previous_ticket_node in previous_ticket_node_list:
                    if str(previous_ticket_node.node_id) != source_node_id:
                        previous_node_dict = workflow_node_service_ins.get_node_by_id(tenant_id, previous_ticket_node.node_id).get_dict()
                        previous_node_dict['keep_previous'] = True
                        result_node_list.append(previous_node_dict)
                    else:
                        workflow_node_obj = workflow_node_service_ins.get_node_by_id(tenant_id, source_node_id)
                        current_node_dict = workflow_node_obj.get_dict()
                        current_node_dict['all_assignee_result'] = now_all_assignee_result
                        current_node_dict['assignee_type'] = "users"
                        next_assignee_list = []
                        for key, value in now_all_assignee_result.items():
                            if not value:
                                next_assignee_list.append(key)
                        current_node_dict['assignee'] = ','.join(next_assignee_list)
                        current_node_dict['assignee_list'] = next_assignee_list
                        result_node_list.append(current_node_dict)
                return result_node_list
        
        target_node_id = edge_obj.target_node_id
        target_node_obj = workflow_node_service_ins.get_node_by_id(tenant_id, target_node_id)
        
        if target_node_obj.type in ("start", "normal", "end", "timer"):
            target_node_result = target_node_obj.get_dict()
            # 如果ticket_node记录中对应的原节点in_parallel, 且target_node不是汇聚节点，则in_parallel=True需要保留
            for source_ticket_node_record in previous_ticket_node_list:
                if source_ticket_node_record.node_id == source_node_id:
                    if source_ticket_node_record.in_parallel:
                        merge_node_obj = workflow_node_service_ins.get_parallel_merge_node(tenant_id, workflow_id, version_id, source_ticket_node_record.parallel_node_id)
                        if target_node_id != merge_node_obj.id:
                            target_node_result['in_parallel'] = True
                            target_node_result['parallel_node_id'] = source_ticket_node_record.parallel_node_id
                        else:
                            target_node_result['in_parallel'] = False
                            target_node_result['parallel_node_id'] = None
            result_node_list.append(target_node_result)
            
        if target_node_obj.type == "parallel": # 并行网关
            node_id_list =  workflow_edge_service_ins.get_parallel_next_node_list(tenant_id, workflow_id, version_id, target_node_obj.id)
            workflow_node_queryset = workflow_node_service_ins.get_node_queryset_by_id_list(tenant_id, workflow_id, version_id, node_id_list)
            for node in workflow_node_queryset:
                s_node = node.get_dict()
                s_node['in_parallel'] = True
                s_node['parallel_node_id'] = target_node_obj.id
                result_node_list.append(s_node)
        
        elif target_node_obj.type == "exclusive": # 排他网关
            # request_data and current field data
            next_edge_list = workflow_edge_service_ins.get_workflow_edges_by_source_node_id(tenant_id, workflow_id, version_id, target_node_obj.id)
            if ticket_id:
                ticket_all_value_dict = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
            else:
                ticket_all_value_dict = request_data_dict.get('fields', {})
            # todo: need merge request data and ticket_all_value_dict
            
            # 合并请求中的字段值，优先使用本次请求的字段
            ticket_all_value_dict_copy = copy.deepcopy(ticket_all_value_dict)
            # request_data_dict 在新建时为完整请求字典，在处理节点时可能直接传 fields
            req_fields = {}
            if isinstance(request_data_dict, dict):
                # 兼容两种调用方式：传入完整请求字典或仅传入 fields 字典
                req_fields = request_data_dict.get('fields', request_data_dict)
                if not isinstance(req_fields, dict):
                    req_fields = {}
            ticket_all_value_dict_copy.update(req_fields)
            for key, value in list(ticket_all_value_dict_copy.items()):
                if isinstance(value, str):
                    ticket_all_value_dict_copy[key] = value

            def _convert_value_by_type(raw_value, field_type):
                if field_type == 'number':
                    try:
                        return float(raw_value)
                    except Exception:
                        return None
                return raw_value

            def _compare(lhs, operator_str, rhs):
                if lhs is None:
                    return False
                if operator_str == '==':
                    return lhs == rhs
                if operator_str == '!=':
                    return lhs != rhs
                if operator_str == '<':
                    return lhs < rhs
                if operator_str == '<=':
                    return lhs <= rhs
                if operator_str == '>':
                    return lhs > rhs
                if operator_str == '>=':
                    return lhs >= rhs
                return False

            for next_edge_obj in next_edge_list:
                props = getattr(next_edge_obj, 'props', {}) or {}
                condition_groups = props.get('condition_groups')
                matched = False
                if condition_groups:
                    # 组间 OR，组内 AND
                    for group in condition_groups:
                        conditions = group.get('conditions', []) if isinstance(group, dict) else []
                        if not conditions:
                            continue
                        all_pass = True
                        for cond in conditions:
                            field_name = cond.get('field_name')
                            operator_str = cond.get('operator')
                            target_value_raw = cond.get('value')
                            field_type = cond.get('field_type')
                            current_value_raw = ticket_all_value_dict_copy.get(field_name)
                            current_value = _convert_value_by_type(current_value_raw, field_type)
                            target_value = _convert_value_by_type(target_value_raw, field_type)
                            if not _compare(current_value, operator_str, target_value):
                                all_pass = False
                                break
                        if all_pass:
                            matched = True
                            break
                else:
                    # 兼容旧版 condition_expression 字符串表达式
                    condition_expression = props.get('condition_expression', '')
                    if condition_expression:
                        try:
                            # 将变量以安全方式提供给格式化与 eval
                            fmt_expr = condition_expression.format(**{
                                k: (f"'''{v}'''" if isinstance(v, str) else v)
                                for k, v in ticket_all_value_dict_copy.items()
                            })
                            import datetime, time  # for security， only support datetime, time, abs operation
                            matched = bool(eval(fmt_expr, {"__builtins__": None}, {"datetime": datetime, "time": time, "abs": abs}))
                        except Exception:
                            matched = False

                if matched:
                    next_node_id = next_edge_obj.target_node_id
                    next_node_obj = workflow_node_service_ins.get_node_by_id(tenant_id, next_node_id)
                    result_node_list.append(next_node_obj.get_dict())
                    # 仅支持命中一个条件分支
                    break
        
        # add in-parallel node, but not current node
        for previous_ticket_node in previous_ticket_node_list:
            if previous_ticket_node.in_parallel and previous_ticket_node.node_id != edge_obj.source_node_id:
                
                previous_node_dict = workflow_node_service_ins.get_node_by_id(tenant_id, previous_ticket_node.node_id).get_dict()
                previous_node_dict['keep_previous'] = True
                result_node_list.append(previous_node_dict)
        return result_node_list


    @classmethod
    def get_ticket_node_assignee_info_by_node_id(cls, tenant_id: str, operator_id: str, node_id: str, ticket_id: str = '',
                                         ticket_req_dict: dict = {}) -> dict:
        """
        get ticket node's participant info
        :param operator_id:
        :param node_dict:
        :param ticket_id:
        :param ticket_req_dict:
        :return:
        """
        node_record = workflow_node_service_ins.get_node_by_id(tenant_id, node_id)

        if ticket_id:
            ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
            if node_record.type == "start":
                return dict(target_assignee_type="users", target_assignee_list=[str(ticket_obj.creator_id)],
                            all_assignee_result={})
            elif node_record.type == "end":
                return dict(target_assignee_type="none", target_assignee_list=[],
                            all_assignee_result={})
            
            parent_ticket_id = ticket_obj.parent_ticket_id
            creator_id = ticket_obj.creator_id
            ticket_node_queryset = TicketNode.objects.filter(ticket_id=ticket_id, tenant_id=tenant_id, node_id=node_id)
            if ticket_node_queryset:
                all_assignee_result = ticket_node_queryset[0].all_assignee_result
            else:
                all_assignee_result = {}

            node_field = node_record.props.get('field_permissions', {})

            edit_field_list = []
            for key, value in node_field.items():
                if value in ["optional", "required"]:
                    edit_field_list.append(key)

            ticket_value_info = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
            for edit_field in edit_field_list:
                ticket_value_info[edit_field] = ticket_req_dict.get('fields', {}).get(edit_field, '')

        else:
            # ticket_id is '', means this is new ticket
            all_assignee_result = {}
            if node_record.type == "start":
                return dict(target_assignee_type="users", target_assignee_list=[str(operator_id)],
                            all_assignee_result={})
            elif node_record.type == "end":
                return dict(target_assignee_type="none", target_assignee_list=[],
                            all_assignee_result={})
            parent_ticket_id = ticket_req_dict.get("parent_ticket_id")
            creator_id = operator_id
            ticket_value_info = ticket_req_dict.get('fields', {})

        target_assignee_type, target_assignee, target_assignee_list = node_record.props.get('assignee_type'), node_record.props.get('assignee'), []
        in_accept_wait = False
        if target_assignee_type == "users":
            target_assignee_list = target_assignee.split(',')
        elif target_assignee_type == "ticket_field":
            target_assignee_source_list = target_assignee.split(",")

            for target_assignee_source in target_assignee_source_list:
                target_assignee_list.append(ticket_value_info.get(target_assignee_source))

        elif target_assignee_type == "parent_ticket_field":
            ticket_value_info = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, parent_ticket_id)

            target_assignee_source_list = target_assignee.split(",")
            for target_assignee_source in target_assignee_source_list:
                target_assignee_list.append(ticket_value_info.get(target_assignee_source))
            target_assignee = ",".join(target_assignee_list)
        elif target_assignee_type == "variables":
            target_assignee_source_list = target_assignee.split(",")
            for target_assignee_source in target_assignee_source_list:
                if target_assignee_source == "creator":
                    target_assignee_list.append(creator_id)
                elif target_assignee_source == "creator_dept_approver":
                    target_assignee_list += account_user_service_ins.get_user_dept_approver_id_list(tenant_id, creator_id)
            target_assignee = ",".join(target_assignee_list)
        elif target_assignee_type == "depts":
            target_assignee_source_list = target_assignee.split(",")
            for target_assignee_source in target_assignee_source_list:
                target_assignee_list += account_dept_service_ins.get_dept_user_id_list(tenant_id, target_assignee_source)
            target_assignee = ",".join(target_assignee_list)
        elif target_assignee_type == "roles":
            target_assignee_source_list = target_assignee.split(",")
            for target_assignee_source in target_assignee_source_list:
                target_assignee_list += account_role_service_ins.get_role_user_id_list(tenant_id, target_assignee_source)
            target_assignee = ",".join(target_assignee_list)
            
        elif target_assignee_type == "hook":
            target_assignee_list = ["*"]  # hook participant may contain sensitive information
        elif target_assignee_type == "external":
            external_url = target_assignee
            external_token = node_record.props.get('external_token')
            
            # extra_info = external_config.get('extra_info', {})  # should be a dict
            # ticket_req_dict.update(extra_info=extra_info)
            result = hook_base_service_ins.call_hook(external_url, external_token, ticket_req_dict)
            if result.get("code") == 0:
                target_assignee_email_list = result.get("data", {}).get("assignee_email_list", [])
                target_assignee_list = account_user_service_ins.get_user_id_list_by_email_list(tenant_id, target_assignee_email_list)
                target_assignee = ",".join(target_assignee_list)
                target_assignee_type = "users"

        if len(target_assignee_list) > 1:
            if node_record.props.get('assignment_strategy') == "random":
                target_assignee_list = [random.choice(target_assignee_list)]
                target_assignee_type = "users"
            elif node_record.props.get('assignment_strategy') == "whole":
                if not all_assignee_result:
                    for target_assignee0 in target_assignee_list:
                        all_assignee_result[target_assignee0] = {}
            elif node_record.props.get('assignment_strategy') == "voluntary":
                target_assignee_type = "users"
                in_accept_wait = True
                
        return dict(target_assignee_type=target_assignee_type,
                    target_assignee_list=target_assignee_list,
                    all_assignee_result=all_assignee_result,
                    in_accept_wait=in_accept_wait)


    @classmethod
    def get_ticket_current_node_list(cls, tenant_id: str, ticket_id: str) -> list:
        """
        get ticket's current node list
        :param ticket_id:
        :return:
        """
        ticket_node_queryset = TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).all()
        return list(ticket_node_queryset)

    
    @classmethod
    def get_ticket_detail_form(cls, tenant_id: str, operator_id: str, ticket_id: str) -> tuple:
        """
        get ticket detail form
        :param tenant_id:
        :param operator_id:
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        workflow_id = ticket_obj.workflow_id
        workflow_version_id = ticket_obj.workflow_version_id

        # todo： get all ticket fields' value
        ticket_field_value_dict = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        
        if ticket_obj.act_state in("finished", "closed"):
            # ticket end, only view ticket
            component_result_list = workflow_base_service_ins.get_workflow_view_form(tenant_id, workflow_id, workflow_version_id)
        else:
            # todo: check whether user is current assignee
            current_assignee_info = ticket_user_service_ins.get_ticket_current_assignee_info(tenant_id, ticket_id)
            if operator_id not in current_assignee_info.keys():
                # user has view permission, since in view.py checked user view permission
                component_result_list = workflow_base_service_ins.get_workflow_view_form(tenant_id, workflow_id, workflow_version_id)
            else:
                # if has in_parallel node, and current node is not in_parallel node
                assignee_node_ids = current_assignee_info.get(operator_id)
                assignee_node_ids_list = assignee_node_ids.split(',')
                current_nodes = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
                parallel_node_id_list = []
                for current_node in current_nodes:
                    if current_node.in_parallel:
                        parallel_node_id_list.append(current_node.node_id)
                if len(parallel_node_id_list) > 0:
                    base_node_id = ''
                    for assignee_node_id in assignee_node_ids_list:
                        if assignee_node_id in parallel_node_id_list:
                            base_node_id = assignee_node_id
                            component_result_list = workflow_base_service_ins.get_workflow_node_form(tenant_id, workflow_id, workflow_version_id, base_node_id)
                            break
                    if not base_node_id:
                        component_result_list = workflow_base_service_ins.get_workflow_view_form(tenant_id, workflow_id, workflow_version_id)
                else: 
                    component_result_list = workflow_base_service_ins.get_workflow_node_form(tenant_id, workflow_id, workflow_version_id, assignee_node_ids.split(',')[0])

        # todo: set field value
        new_component_result_list = []
        for component in component_result_list:
            # new_component = copy.deepcopy(component)
            
            if component.get('type') == 'row':
                for field_component in component.get('children'):
                    # new_field_component = copy.deepcopy(field_component)
                    field_key = field_component.get('component_key')
                    field_value = ticket_field_value_dict.get(field_key)
                    field_component['props']['value'] = field_value
                    # component.get('children').append(field_component)
            new_component_result_list.append(component)
        workflow_basic_obj = workflow_base_service_ins.get_workflow_basic_info_by_id(tenant_id, workflow_id, workflow_version_id)

        version_obj = workflow_base_service_ins.get_workflow_version_info_by_id(tenant_id, workflow_id, workflow_version_id)

        workflow_metadata = dict(
            id=str(workflow_id),
            name=workflow_basic_obj.get('name'),
            version_id=str(workflow_version_id),
            version_name=version_obj.get('name'),
            description=workflow_basic_obj.get('description')
        )  
        return new_component_result_list, workflow_metadata
                
    @classmethod
    def ticket_view_permission_check(cls, tenant_id:str, ticket_id: str, user_id: str)-> bool:
        """
        check user whether have view permission,  if open permission check in workflow config, otherwise decide by ticket releationship
        :param tenant_id:
        :param ticket_id:
        :param user_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(tenant_id=tenant_id, id=ticket_id).first()
        if not ticket_obj:
            return CustomCommonException("ticket is not existed or has been deleted")
        
        user_obj = account_user_service_ins.get_user_by_user_id(tenant_id, user_id)
        if user_obj.type == 'admin':
            return True
        workflow_ticket_view_permission = workflow_permission_service_ins.user_workflow_permission_check(tenant_id, ticket_obj.workflow_id, ticket_obj.workflow_version_id, user_id, 'view')
        if workflow_base_service_ins:
            return True
        
        # check relation permission
        related_user_id_list = ticket_user_service_ins.get_ticket_relation_user_id_list(tenant_id, ticket_id)
        if user_id in related_user_id_list:
            return True
        else:
            return False

    @classmethod
    def ticket_action_permission_check(cls, tenant_id: str, ticket_id: str, user_id: str, action_type:str, action_id:str) -> bool:
        """
        check user whether have handle permission
        :param tenant_id:
        :param ticket_id:
        :param user_id:
        :return:
        """
        if action_type == "add_comment":
            return cls.ticket_view_permission_check(tenant_id, ticket_id, user_id)
        if action_type == "withdraw":
            return True
        elif action_type in ("forward", "consult", "consult_submit", "accept", "agree", "reject", "other"):
            return cls.ticket_assignee_permission_check(tenant_id,ticket_id, user_id)
        elif action_type in ("force_forward", "force_close", "force_alter_node"):
            return cls.ticket_admin_permission_check(tenant_id, ticket_id, user_id)
        return False




    @classmethod
    def ticket_assignee_permission_check(cls, tenant_id: str, ticket_id: str, user_id: str) -> bool:
        """
        check user whether have handle permission
        :param ticket_id:
        :param user_id:
        :return:
        """
        current_assignee_info = ticket_user_service_ins.get_ticket_current_assignee_info(tenant_id, ticket_id)
        if user_id in current_assignee_info.keys():
            return True
        return False

    @classmethod
    def get_ticket_detail_actions(cls, tenant_id: str, ticket_id: str, user_id: str) -> tuple:
        """
        get ticket detail actions
        :param tenant_id:
        :param ticket_id:
        :param user_id:
        :return:
        """
        # need consider in_add_node status

        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        workflow_id = ticket_obj.workflow_id
        workflow_version_id = ticket_obj.workflow_version_id
        # check handle permission
        current_assignee_info = ticket_user_service_ins.get_ticket_current_assignee_info(tenant_id, ticket_id)
        action_result_list = []
        

        if user_id in current_assignee_info.keys():
            # has hendle permission, get edge list, base first node
            # 两个并行节点，其中一个到达汇聚节点， 另外一个没有到，那么汇聚节点应该无法操作，而需要等待其他并行节点也到达汇聚节点
            ticket_current_nodes = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
            has_parallel_node = False
            paraller_node_id_list = []
            for ticket_current_node in ticket_current_nodes:
                if ticket_current_node.in_parallel:
                    has_parallel_node = True
                    paraller_node_id_list.append(str(ticket_current_node.node_id))
            if has_parallel_node:
                current_assignee_info_nodes = current_assignee_info.get(user_id).split(',')
                has_parallel_permission = False
                for current_assignee_info_node in current_assignee_info_nodes:
                    if current_assignee_info_node in paraller_node_id_list:
                        action_base_node_id = current_assignee_info_node
                        has_parallel_permission = True
                        break
                if not has_parallel_permission:
                    return [dict(id='add_comment',name='add comment',type='add_comment',props= {})], current_assignee_info_nodes[0]
            
            action_base_node_id = current_assignee_info.get(user_id).split(',')[0]
            # in consult status, only show consult action
            if ticket_node_service_ins.get_ticket_node_by_node_id(tenant_id, ticket_id, action_base_node_id).in_consult:
                action_result_list.append(dict(
                    id='consult_submit',
                    name='consult submit',
                    type='consult_submit',
                    props= {}
                ))
                return action_result_list, str(action_base_node_id)
            
            if ticket_node_service_ins.get_ticket_node_by_node_id(tenant_id, ticket_id, action_base_node_id).in_accept_wait:
                action_result_list.append(dict(
                    id='accept',
                    name='accept',
                    type='accept',
                    props= {}
                ))
                return action_result_list, str(action_base_node_id)
            edge_info_list = workflow_edge_service_ins.get_workflow_edges_by_source_node_id(tenant_id, workflow_id, workflow_version_id, current_assignee_info.get(user_id).split(',')[0])
            
            for edge_info in edge_info_list:
                action_result_list.append(dict(
                    id=str(edge_info.id),
                    name=edge_info.name,
                    type=edge_info.type,
                    props=edge_info.props
                ))
        else:
            action_base_node_id = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)[0].node_id
        if ticket_base_service_ins.ticket_view_permission_check(tenant_id, ticket_id, user_id):
            action_result_list.append(dict(
                id='add_comment',
                name='add comment',
                type='add_comment',
                props= {}
            ))
        if ticket_base_service_ins.ticket_assignee_permission_check(tenant_id, ticket_id, user_id):
            action_result_list.append(dict(
                id='forward',
                name='forward',
                type='forward',
                props= {}
            ))
            
            action_result_list.append(dict(
                id='consult',
                name='consult',
                type='consult',
                props= {}
            ))
        # 撤回 allowWithdraw
        action_base_node_record = workflow_node_service_ins.get_node_by_id(tenant_id, action_base_node_id)
        allow_withdraw = action_base_node_record.props.get('allow_withdraw', False)
        if allow_withdraw and str(ticket_obj.creator_id) == user_id:
            action_result_list.append(dict(
                id='withdraw',
                name='withdraw',
                type='withdraw',
                props= {}
            ))

        
        return action_result_list, str(action_base_node_id)

    @classmethod
    def get_ticket_detail_admin_actions(cls, tenant_id: str, ticket_id: str, user_id: str) -> tuple:
        """
        get ticket detail admin actions, actions as workflow admin
        :param tenant_id:
        :param ticket_id:
        :param user_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        if ticket_obj.act_state in ("finished", "closed", "force_closed"):
            return [], ''

        workflow_id = ticket_obj.workflow_id
        workflow_version_id = ticket_obj.workflow_version_id
        action_result_list = []
        # check admin permission
        user_obj = account_user_service_ins.get_user_by_user_id(tenant_id, user_id)
        if user_obj.type == 'admin':
            has_admin_permission = True
        else:
            has_admin_permission = workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'admin')
            if not has_admin_permission:
                has_admin_permission = has_admin_permission and workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'dispatcher')
        if not has_admin_permission:
            return action_result_list, ''
        action_base_node_id = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)[0].node_id
        action_result_list.append(dict(
            id='force_forward',
            name='force forward',
            type='force_forward',
            props= {}
        ))
        action_result_list.append(dict(
            id='force_close',
            name='force close',
            type='force_close',
            props= {}
        ))
        # action_result_list.append(dict(
        #     id='force_alter_node',
        #     name='force alter node',
        #     type='force_alter_node',
        #     props= {}
        # ))
        return action_result_list, str(action_base_node_id)

    @classmethod
    @transaction.atomic
    def handle_ticket(cls, tenant_id: str, app_name: str, ticket_id:str, operator_id: str, request_data_dict: dict) -> bool:
        """
        handle ticket. include edge actions and consult(加签), consult_submit(加签提交), forward(转交), accept(接单)
        :param tenant_id:
        :param app_name:
        :param ticket_id:
        :param operator_id:
        :param ticket_id:
        :param action_type:
        :param action_id:
        :param action_props:
        :param request_data_dict:
        :return:
        """
        action_type = request_data_dict.get('action_type')
        
        ticket_record = ticket_base_service_ins.get_ticket_by_id(tenant_id, ticket_id)
        workflow_id = ticket_record.workflow_id
        workflow_version_id = ticket_record.workflow_version_id

        # check whether current call source has permission to create this type ticket
        workflow_permission_service_ins.app_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, app_name)

        if action_type == "add_comment":
            cls.add_comment(tenant_id, ticket_id, operator_id, request_data_dict)
        elif action_type == "withdraw":
            cls.withdraw_ticket(tenant_id, ticket_id, operator_id, request_data_dict)
        elif action_type in ("forward", "consult", "consult_submit", "accept", "agree", "reject", "other"):
            cls.handle_ticket_assignee_action(tenant_id, ticket_id, operator_id, request_data_dict)
        elif action_type in ("force_forward", "force_close", "force_alter_node"):
            cls.handle_ticket_admin_action(tenant_id, ticket_id, operator_id, request_data_dict)
        return True

        
    @classmethod
    def handle_ticket_assignee_action(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict: dict) -> bool:
        """
        handle ticket assignee action
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param request_data_dict:
        :return:
        """
        # todo: handle ticket assignee action,
        action_type = request_data_dict.get('action_type')
        action_id = request_data_dict.get('action_id')
        action_props = request_data_dict.get('action_props')
        node_id = request_data_dict.get('action_props', {}).get('node_id')
        if action_type == "forward":
            target_assignee_id = request_data_dict.get('action_props', {}).get('target_assignee_id')
            cls.forward_ticket(tenant_id, ticket_id, operator_id, node_id, operator_id, target_assignee_id, action_props.get('commment'))
        elif action_type == "consult":
            cls.consult_ticket(tenant_id, ticket_id, operator_id, node_id, action_props)
        elif action_type == "consult_submit":
            cls.consult_submit_ticket(tenant_id, ticket_id, operator_id, node_id, action_props)
        elif action_type == "accept":
            cls.accept_ticket(tenant_id, ticket_id, node_id, operator_id, action_props)
        elif action_type in ("agree", "reject", "other"):
            cls.handle_ticket_edge_action(tenant_id, ticket_id, operator_id, request_data_dict)
        else:
            raise CustomCommonException("action type not supported")

        return True
    
    @classmethod
    def handle_ticket_admin_action(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict: dict) -> bool:
        """
        handle ticket admin action.  include "force_forward", "force_close", "force_alter_node", force_forward need specify which node_id to forward
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param request_data_dict:
        :return:
        """
        # todo: permission check
        cls.ticket_admin_permission_check(tenant_id, ticket_id, operator_id)
        action_type = request_data_dict.get('action_type')
        if action_type == "force_forward":
            cls.force_forward_ticket(tenant_id, ticket_id, operator_id, request_data_dict)
        elif action_type == "force_close":
            cls.force_close_ticket(tenant_id, ticket_id, operator_id, request_data_dict)
        elif action_type == "force_alter_node":
            cls.force_alter_node(tenant_id, ticket_id, operator_id, request_data_dict)
        
        return True
    
    @classmethod
    def add_comment(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict: dict) -> str:
        """
        add comment to ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param comment:
        :return:
        """
        action_props = request_data_dict.get('action_props', {})
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "add_comment", None, action_props.get('comment', ''),
        "user", operator_id, action_props.get('node_id', ''), ticket_data)
    
    @classmethod
    def withdraw_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict: dict) -> bool:
        """
        withdraw ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param request_data_dict:
        :return:
        """
        # 1. ticket should only on one node, 2. current node should be allow withdraw, 3. opertor is ticket creator
        ticket_node_queryset = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
        if len(ticket_node_queryset) != 1:
            raise CustomCommonException("ticket should only on one node")

        current_node_id = ticket_node_queryset[0].node_id
        workflow_node_record = workflow_node_service_ins.get_node_by_id(tenant_id, current_node_id)
        allow_withdraw = workflow_node_record.props.get('allow_withdraw', False)
        if not allow_withdraw:
            raise CustomCommonException("current node should be allow withdraw")
        
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        if str(ticket_obj.creator_id) != operator_id:
            raise CustomCommonException("opertor is not ticket creator")
        
        init_node_record = workflow_node_service_ins.get_init_node(tenant_id, ticket_obj.workflow_id, ticket_obj.workflow_version_id)
        next_node_assignee_info = ticket_base_service_ins.get_ticket_node_assignee_info_by_node_id(tenant_id, operator_id, init_node_record.id, ticket_id, {})
        
        node_info_list = [dict(
            ticket_id=ticket_id,
            node_id = init_node_record.id,
            node_type= 'start',
            is_active = True,
            all_assignee_result= next_node_assignee_info.get("all_assignee_result"),
            target_assignee_type=next_node_assignee_info.get("target_assignee_type"),
            target_assignee_list=next_node_assignee_info.get("target_assignee_list"),
            in_accept_wait = next_node_assignee_info.get("in_accept_wait", False),
            in_parallel=False
        )]
        ticket_node_service_ins.update_ticket_node_record(tenant_id, operator_id, node_info_list)
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, [], node_info_list)  
        ticket_all_fields = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "withdraw", None, "withdraw", 'user', operator_id, current_node_id, ticket_all_fields)

        # withdraw hook
        from tasks import flow_action_hook_task
        transaction.on_commit(lambda: flow_action_hook_task.apply_async(args=[tenant_id, ticket_id, "withdraw"], queue='loonflow'))
        return True
    @classmethod
    def ticket_admin_permission_check(cls, tenant_id:str, ticket_id: str, user_id: str = '') -> bool:
        """
        check whether user has ticket's admin permission,  admin or related workflow admin or related workflow dispatcher
        :param username:
        :param ticket_id:
        :return:
        """
        # admin has all ticket's permission
        user_record = account_user_service_ins.get_user_by_user_id(tenant_id, user_id)
        if user_record.type == "admin":
            return True
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        workflow_id = ticket_obj.workflow_id
        workflow_version_id = ticket_obj.workflow_version_id
        return workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'admin') or workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'dispatcher')

    @classmethod
    def ticket_withdraw_permission_check(cls, tenant_id: str, ticket_id: str, user_id: str) -> bool:
        """
        check whether user has ticket's withdraw permission
        :param tenant_id:
        :param ticket_id:
        :param user_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.get(id=ticket_id, tenant_id=tenant_id)
        ticket_node = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)[0]
        workflow_id = ticket_obj.workflow_id
        workflow_version_id = ticket_obj.workflow_version_id
        return workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'admin') or workflow_permission_service_ins.user_workflow_permission_check(tenant_id, workflow_id, workflow_version_id, user_id, 'dispatcher')

    @classmethod
    def forward_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, node_id: str, source_assignee_id: str, target_assignee_id: str, commment:str) -> bool:
        """
        forward ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param node_id:
        :param source_assignee_id:
        :param target_assignee_id:
        :return:
        """
        # 1.get ticket assignee from ticket_user table, 2.change assignee, 3. send email
        ticket_node_service_ins.replace_node_assignee(tenant_id, ticket_id, operator_id, node_id, source_assignee_id, target_assignee_id)
        ticket_user_service_ins.replace_user_assignee(tenant_id, ticket_id, operator_id, node_id, source_assignee_id, target_assignee_id)
        # add flow history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, 'forward', '', commment,'user', operator_id, node_id, ticket_data)
        # send notification
        from tasks import flow_notification_task
        flow_notification_task.apply_async(args=[tenant_id, ticket_id, node_id], queue='loonflow')
        return True

    @classmethod
    def force_forward_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict:dict) -> bool:
        """
        force forward ticket, only for admin or workflow admin, workflow dispatcher
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param node_id:
        :param source_assignee_id:
        :param target_assignee_id:
        :return:
        """
        # 1.get ticket assignee from ticket_user table, 2.change assignee, 3. send email
        target_assignee_id = request_data_dict.get('action_props', {}).get('target_assignee_id')
        comment = request_data_dict.get('action_props', {}).get('comment', '')
        node_id = request_data_dict.get('action_props', {}).get('node_id')
        ticket_node_service_ins.replace_node_assignee(tenant_id, ticket_id, operator_id, node_id, '', target_assignee_id)
        ticket_user_service_ins.replace_user_assignee(tenant_id, ticket_id, operator_id, node_id, '', target_assignee_id)
        # add flow history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, 'force_forward', '', comment,'user', operator_id, node_id, ticket_data)
        # send notification
        from tasks import flow_notification_task
        flow_notification_task.apply_async(args=[tenant_id, ticket_id, node_id], queue='loonflow')
        return True

    @classmethod
    def force_close_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict:dict) -> bool:
        """
        force close ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :return:
        """
        # 1.get end node, 2.update ticket_node , 3.update_ticket_user, 4. send notification
        ticket_record=TicketRecord.objects.get(tenant_id=tenant_id, id=ticket_id)
        workflow_id = ticket_record.workflow_id
        workflow_version_id = ticket_record.workflow_version_id
        end_node_record = workflow_node_service_ins.get_end_node(tenant_id, workflow_id, workflow_version_id)
        node_id = end_node_record.id
        node_info_list = [dict(
            ticket_id=ticket_id,
            node_id = node_id,
            node_type= 'end',
            is_active = True,
            all_assignee_result= {},
            target_assignee_type=None,
            target_assignee_list=[],
            in_parallel=False

        )]
        ticket_node_service_ins.update_ticket_node_record(tenant_id, operator_id, node_info_list)
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, [], node_info_list)
        ticket_record.act_state = "force_closed"
        ticket_record.save()
        # add flow history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, 'force_close', '', request_data_dict.get('action_props', {}).get('comment', ''),'user', operator_id, node_id, ticket_data)
        
        # send notification
        from tasks import flow_action_hook_task
        flow_action_hook_task(tenant_id, ticket_id, "force_close")
        
        return True
    
    @classmethod
    def force_alter_node(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict: dict) -> bool:
        """
        force alter node
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param request_data_dict:
        :return:
        """
        # just change to one target node, no matter whether ticket has multiple active node now, target node must be not a parallel node
        target_node_id = request_data_dict.get('action_props', {}).get('target_node_id')
        comment = request_data_dict.get('action_props', {}).get('comment')
        # todo: 1.update ticket_node 2. update ticket_user 3. send notification
        ticket_record=TicketRecord.objects.get(tenant_id=tenant_id, id=ticket_id)
        workflow_id = ticket_record.workflow_id
        workflow_version_id = ticket_record.workflow_version_id
        current_node_queryset = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
        current_node_id_list = [node_obj.node_id for node_obj in current_node_queryset]
        
        node_record = workflow_node_service_ins.get_node_by_id(tenant_id, target_node_id)

        next_node_assignee_info = ticket_base_service_ins.get_ticket_node_assignee_info_by_node_id(tenant_id, operator_id, node_record.id, ticket_id, {})
        
        node_info_list = [dict(
            ticket_id=ticket_id,
            node_id = target_node_id,
            node_type= node_record.type,
            is_active = True,
            all_assignee_result= next_node_assignee_info.get("all_assignee_result"),
            target_assignee_type=next_node_assignee_info.get("target_assignee_type"),
            target_assignee_list=next_node_assignee_info.get("target_assignee_list"),
            in_accept_wait = next_node_assignee_info.get("in_accept_wait", False),
            in_parallel=False

        )]
        ticket_node_service_ins.update_ticket_node_record(tenant_id, operator_id, node_info_list)
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, [], node_info_list)
        # update ticket_flow_history
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "force_alter_node", None, comment, 'user', operator_id, current_node_id_list[0], {})

        # send notification
        from tasks import flow_notification_task
        flow_notification_task.apply_async(args=[tenant_id, ticket_id, target_node_id], queue='loonflow')
        
        
        return True
        
    @classmethod
    def consult_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, node_id: str, action_props: dict) -> bool:
        """
        consult ticket, 加签
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param node_id:
        :param action_props:
        :return:
        """
        # 1. update ticket_node, 2.update ticket_user, 3. send notification
        consultant_id = action_props.get('target_assignee_id')
        comment = action_props.get('comment')
        ticket_node_service_ins.update_ticket_node_consult_record(tenant_id, ticket_id, node_id, operator_id, consultant_id)
        ticket_user_service_ins.update_ticket_user_consult_record(tenant_id, ticket_id, node_id, operator_id, consultant_id)
        # update ticket_flow_history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "consult_ticket", None, comment, 'user', operator_id, node_id, ticket_data)
        # send notification
        from tasks import flow_notification_task
        flow_notification_task.apply_async(args=[tenant_id, ticket_id, node_id], queue='loonflow')

        return True
    
    @classmethod
    def consult_submit_ticket(cls, tenant_id: str, ticket_id: str, operator_id: str, node_id: str, action_props: dict) -> bool:
        """
        consult submit ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param action_id:
        :param action_props:
        :return:
        """
        # 1. update ticket_node, 2.update ticket_user, 3. send notification
        comment = action_props.get('comment')
        cc_to_user_id_list = action_props.get('cc_to_user_id_list', [])
        ticket_node_service_ins.update_ticket_node_consult_submit(tenant_id, ticket_id, node_id)

        # generate next node info list
        next_node_info_list = []
        ticket_node_queryset = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
        for ticket_node in ticket_node_queryset:
            if ticket_node.node_id != node_id:
                next_node_info_list.append(dict(
                    ticket_id=ticket_id,
                    node_id=ticket_node.node_id,
                    target_assignee_type=ticket_node.assignee_type,
                    target_assignee=ticket_node.assignee,
                    target_assignee_list=ticket_node.assignee.split(',')
                ))
            else:
                ticket_node_all_assignee_result = ticket_node.all_assignee_result
                node_assignee_list = []
                if ticket_node_all_assignee_result:
                    for key, value in ticket_node_all_assignee_result.items():
                        if not value:
                            node_assignee_list.append(key)
                else:
                    node_assignee_list.apeend(str(ticket_node.consult_from_id))
                
                next_node_info_list.append(dict(
                    ticket_id=ticket_id,
                    node_id=ticket_node.node_id,
                    target_assignee_type=ticket_node.assignee_type,
                    target_assignee=str(ticket_node.consult_from_id),
                    target_assignee_list=ticket_node.assignee.split(',')
                ))
        

        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, cc_to_user_id_list, next_node_info_list)
        

        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "consult_submit", None, comment, 'user', operator_id, node_id, ticket_data)
        # send notification
        from tasks import flow_notification_task
        flow_notification_task.apply_async(args=[tenant_id, ticket_id, node_id], queue='loonflow')

        return True

    @classmethod
    def accept_ticket(cls, tenant_id: str, ticket_id: str, node_id: str, operator_id: str, action_props: dict) -> bool:
        """
        accept ticket
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param action_id:
        :param action_props:
        :return:
        """
        # todo: 1. update ticket_node, 2.update ticket_user, 3. send notification
        ticket_node_service_ins.update_ticket_node_accept(tenant_id, ticket_id, node_id, operator_id)
        comment = action_props.get('action_props', {}).get('comment')

        # generate next node info list
        next_node_info_list = []
        ticket_node_queryset = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
        for ticket_node in ticket_node_queryset:
            if ticket_node.node_id != node_id:
                next_node_info_list.append(dict(
                    ticket_id=ticket_id,
                    node_id=ticket_node.node_id,
                    target_assignee_type=ticket_node.assignee_type,
                    target_assignee=ticket_node.assignee,
                    target_assignee_list=ticket_node.assignee.split(',')
                ))
            else:
                next_node_info_list.append(dict(
                    ticket_id=ticket_id,
                    node_id=ticket_node.node_id,
                    target_assignee_type='users',
                    target_assignee=operator_id,
                    target_assignee_list=ticket_node.assignee.split(',')
                ))
        
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, [], next_node_info_list)
        # update ticket_flow_history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, "accept", None, comment, 'user', operator_id, node_id, ticket_data)
        # todo: send notification
        
        return True


    @classmethod
    def handle_ticket_edge_action(cls, tenant_id: str, ticket_id: str, operator_id: str, request_data_dict:dict) -> bool:
        """
        handle ticket edge action
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param node_id:
        :param action_id:
        :param action_props:
        :return:
        """
        # todo: update ticket_node, update ticket_user, update ticket_flow_history, send notification
        ticket_record = ticket_base_service_ins.get_ticket_by_id(tenant_id, ticket_id)
        workflow_id = ticket_record.workflow_id
        workflow_version_id = ticket_record.workflow_version_id
        node_id = request_data_dict.get('action_props', {}).get('node_id')
        action_id = request_data_dict.get('action_id')
        fields = request_data_dict.get('fields', {})



        edge_record = workflow_edge_service_ins.get_workflow_edge_by_id(tenant_id, workflow_id, workflow_version_id, edge_id=action_id)
        if str(edge_record.source_node_id) != node_id:
            raise CustomCommonException("current node has no permission to run this transition")
        
        current_node_record = workflow_node_service_ins.get_node_by_id(tenant_id, node_id)

        validate_fields = edge_record.props.get('validate_fields', True)
        
        ## get start node id
        required_field_list, update_field_list = [], []

        ## startnode and action match check
        if current_node_record.id != edge_record.source_node_id:
            raise CustomCommonException("start node and action not match")
        


        field_permissions = current_node_record.props.get('field_permissions', {})
        for field_key, field_permission in field_permissions.items():
            if field_permission == 'required':
                required_field_list.append(field_key)
                update_field_list.append(field_key)
            elif field_permission == 'optional':
                update_field_list.append(field_key)
        if validate_fields:
            for required_field in required_field_list:
                if required_field not in fields.keys():
                    raise CustomCommonException('field {} is required'.format(required_field))



        next_node_dict_list = cls.get_action_next_node_dict_list(tenant_id, ticket_id, operator_id, workflow_id, workflow_version_id, action_id, request_data_dict)
        act_state = "on_going"
        if len(next_node_dict_list) == 1:
            act_state = cls.get_act_state_by_node_and_edge_type(next_node_dict_list[0].get("type"), edge_record.type)

        base_info_update = dict(act_state=act_state)
        if "title" in fields.keys() and "title" in update_field_list:
            base_info_update["title"] = fields.get("title")
        
        TicketRecord.objects.filter(id=ticket_id, tenant_id=tenant_id).update(**base_info_update)
        


        # add ticket flow history
        ticket_data = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
        ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, operator_id, ticket_id, edge_record.type, action_id,
                                                                request_data_dict.get("action_props", {}).get("comment"), "user", str(operator_id),
                                                                node_id, ticket_data)

        # add ticket custom field
        for_update_field = {}
        for field_key, field_value in request_data_dict.get('fields', {}).items():
            if field_key in update_field_list:
                for_update_field[field_key] = field_value

        ticket_field_service_ins.update_ticket_fields(tenant_id, ticket_id, operator_id, workflow_id, workflow_version_id, for_update_field)

        # update TicketNode
        next_ticket_node_result_list  = []
        for next_node in next_node_dict_list:
            if next_node.get("keep_previous"):
                # use previous ticket_node info
                next_node_record = ticket_node_service_ins.get_ticket_node_by_node_id(tenant_id, ticket_id, next_node.get("id"))
                next_node_result = next_node_record.get_dict()
                next_node_result['node_id'] = next_node_record.node_id
                next_node_result['parallel_node_id'] = next_node_record.parallel_node_id
                if next_node_record.assignee_type == 'users':
                    next_node_result['target_assignee_list'] = next_node_record.assignee.split(',')

            else:
                next_node_result = dict()
                next_node_assignee_info = cls.get_ticket_node_assignee_info_by_node_id(tenant_id, operator_id, next_node.get("id"), ticket_id, request_data_dict)
                next_node_result['ticket_id'] = ticket_id
                next_node_result['node_id'] = next_node.get("id")
                next_node_result['node_type'] = next_node.get("type")
                next_node_result['in_parallel'] = next_node.get("in_parallel", False)
                next_node_result['parallel_node_id'] = next_node.get("parallel_node_id")
                next_node_result['is_active'] = True
                next_node_result['in_add_node'] = False
                next_node_result['add_node_target'] = ""
                next_node_result['hook_state'] = ""
                if next_node.get("assignee_type", "") == "users":
                    next_node_result['target_assignee_list'] = next_node.get("assignee_list", [])
                    next_node_result['target_assignee'] = next_node.get("assignee", "")
                    next_node_result['all_assignee_result'] = next_node.get("all_assignee_result", {})
                else:
                    next_node_result['all_assignee_result'] = next_node_assignee_info.get("all_assignee_result")
                    next_node_result['target_assignee_type'] = next_node_assignee_info.get("target_assignee_type")
                    next_node_result['target_assignee_list'] = next_node_assignee_info.get("target_assignee_list", [])
                next_node_result['in_accept_wait'] = next_node_assignee_info.get("in_accept_wait", False)
            next_ticket_node_result_list.append(next_node_result)

        ticket_node_service_ins.update_ticket_node_record(tenant_id, operator_id, next_ticket_node_result_list)
        

        # update relate user for next node
        ticket_user_service_ins.update_ticket_user_by_all_next_node_result(tenant_id, ticket_id, operator_id, request_data_dict.get("cc_to_user_id_list", []), next_ticket_node_result_list)
        
        # send notification
        from tasks import flow_notification_task
        for next_ticket_node_result0 in next_ticket_node_result_list:
            if not next_ticket_node_result0.get('keep_previous', False):
                transaction.on_commit(lambda: flow_notification_task.apply_async(args=[tenant_id, ticket_id, next_ticket_node_result0.get("id")], queue='loonflow'))

        # flow hook
        for next_ticket_node_result in next_ticket_node_result_list:
            if next_ticket_node_result.get("type") == "hook":
                #todo: trigger hook
                from tasks import flow_hook_task
                transaction.on_commit(lambda: flow_hook_task.apply_async(args=[tenant_id, ticket_id, next_ticket_node_result.get("id")], queue='loonflow'))
        # event hook: reject, finish
        if edge_record.type == "reject":
            from tasks import flow_action_hook_task
            transaction.on_commit(lambda: flow_action_hook_task.apply_async(args=[tenant_id, ticket_id, "reject"], queue='loonflow'))
        if len(next_ticket_node_result_list) == 1 and next_ticket_node_result_list[0].get("type") == "end":
            from tasks import flow_action_hook_task
            transaction.on_commit(lambda: flow_action_hook_task.apply_async(args=[tenant_id, ticket_id, "finish"], queue='loonflow'))
        
        
        # todo: timer handle
        # todo:parent_ticket handle
        return True
    

ticket_base_service_ins = TicketBaseService()
