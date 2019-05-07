import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Workflow
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.account.account_base_service import AccountBaseService


class WorkflowBaseService(BaseService):
    """
    流程服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_workflow_list(cls, name, page, per_page, workflow_id_list):
        """
        获取工作流列表
        :param name:
        :param page:
        :param per_page:
        :param workflow_id_list:工作流id list
        :return:
        """
        query_params = Q(is_deleted=False)
        if name:
            query_params &= Q(name__contains=name)

        query_params &= Q(id__in=workflow_id_list)

        workflow_querset = Workflow.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_querset, per_page)
        try:
            workflow_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_result_paginator = paginator.page(paginator.num_pages)
        workflow_result_object_list = workflow_result_paginator.object_list
        workflow_result_restful_list = []
        for workflow_result_object in workflow_result_object_list:
            workflow_result_restful_list.append(dict(id=workflow_result_object.id, name=workflow_result_object.name, description=workflow_result_object.description,
                                                     notices=workflow_result_object.notices, view_permission_check=workflow_result_object.view_permission_check,
                                                     limit_expression=workflow_result_object.limit_expression, display_form_str=workflow_result_object.display_form_str,
                                                     creator=workflow_result_object.creator, gmt_created=str(workflow_result_object.gmt_created)[:19]))
        return workflow_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def check_new_permission(cls, username, workflow_id):
        """
        判断用户是否有新建工单的权限
        :param username:
        :param workflow_id:
        :return:
        """
        # 获取workflow的限制表达式
        workflow_obj, msg = cls.get_by_id(workflow_id)
        if not workflow_obj:
            return False, msg
        limit_expression = workflow_obj.limit_expression
        if not limit_expression:
            return True, 'no limit_expression set'
        #'限制周期({"period":24} 24小时), 限制次数({"count":1}在限制周期内只允许提交1次), 限制级别({"level":1} 针对(1单个用户 2全局)限制周期限制次数,默认特定用户);允许特定人员提交({"allow_persons":"zhangsan,lisi"}只允许张三提交工单,{"allow_depts":"1,2"}只允许部门id为1和2的用户提交工单，{"allow_roles":"1,2"}只允许角色id为1和2的用户提交工单)
        limit_expression_dict = json.loads(limit_expression)
        limit_period = limit_expression_dict.get('period')
        limit_count = limit_expression_dict.get('limit_count')
        limit_allow_persons = limit_expression_dict.get('allow_persons')
        limit_allow_depts = limit_expression_dict.get('allow_depts')
        limit_allow_roles = limit_expression_dict.get('allow_roles')

        if limit_period:
            from service.ticket.ticket_base_service import TicketBaseService
            if limit_expression_dict.get('level'):
                if limit_expression_dict.get('level') == 1:
                    count_result, msg = TicketBaseService.get_ticket_count_by_args(workflow_id=workflow_id, username=username, period=limit_period)
                elif limit_expression_dict.get('level') == 2:
                    count_result, msg = TicketBaseService.get_ticket_count_by_args(workflow_id=workflow_id, period=limit_period)
                else:
                    return False, 'level in limit_expression is invalid'
                if count_result is False:
                    return False, msg
                if not limit_expression_dict.get('count'):
                    return False, 'count is need when level is not none'
                if count_result > limit_expression_dict.get('count'):
                    return False, '{} tickets can be created in {}hours when workflow_id is {}'.format(limit_count, limit_period, workflow_id)

        if limit_allow_persons:
            if username not in limit_allow_persons.split(','):
                return False, '{} can not create ticket base on workflow_id:{}'.format(workflow_id)
        if limit_allow_depts:
            # 获取用户所属部门，包含上级部门
            user_all_dept_id_list, msg = AccountBaseService.get_user_up_dept_id_list(username)
            if user_all_dept_id_list is False:
                return False, msg
            # 只要user_all_dept_id_list中的某个部门包含在允许范围内即可
            limit_allow_dept_str_list = limit_allow_depts.split(',')
            limit_allow_dept_id_list = [int(limit_allow_dept_str) for limit_allow_dept_str in limit_allow_dept_str_list]
            limit_allow_dept_id_list = list(set(limit_allow_dept_id_list)) #去重
            total_list = user_all_dept_id_list + limit_allow_dept_id_list
            if len(total_list) == len(set(total_list)):
                # 去重后长度相等，说明两个list完全没有重复，即用户所在部门id肯定不在允许的部门id列表内
                return False, 'user is not in allow dept'
        if limit_allow_roles:
            # 获取用户所有的角色
            user_role_list, msg = AccountBaseService.get_user_role_id_list(username)
            if user_role_list is False:
                return False, msg
            limit_allow_role_str_list = limit_allow_roles.split(',')
            limit_allow_role_id_list = [int(limit_allow_role_str) for limit_allow_role_str in limit_allow_role_str_list]
            limit_allow_role_id_list = list(set(limit_allow_role_id_list))
            total_list = limit_allow_role_id_list + user_role_list
            if len(total_list) == len(set(total_list)):
                return False, 'user is not in allow role'
        return True, ''

    @classmethod
    @auto_log
    def get_by_id(cls, workflow_id):
        """
        获取工作流 by id
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(is_deleted=0, id=workflow_id).first()
        if not workflow_obj:
            return False, '工作流不存在'
        return workflow_obj, ''

    @classmethod
    @auto_log
    def add_workflow(cls, name, description, notices, view_permission_check, limit_expression, display_form_str, creator):
        """
        新增工作流
        :param name:
        :param description:
        :param notices:
        :param view_permission_check:
        :param limit_expression:
        :param display_form_str:
        :param creator:
        :return:
        """
        workflow_obj = Workflow(name=name, description=description, notices=notices, view_permission_check=view_permission_check,
                                limit_expression=limit_expression,display_form_str=display_form_str, creator=creator)
        workflow_obj.save()

        return workflow_obj.id, ''

    @classmethod
    @auto_log
    def edit_workflow(cls, workflow_id, name, description, notices, view_permission_check, limit_expression, display_form_str):
        """
        更新工作流
        :param workflow_id:
        :param name:
        :param description:
        :param notices:
        :param view_permission_check:
        :param limit_expression:
        :param display_form_str:
        :return:
        """
        workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0)
        if workflow_obj:
            workflow_obj.update(name=name, description=description, notices=notices, view_permission_check=view_permission_check,
                                limit_expression=limit_expression, display_form_str=display_form_str)
        return workflow_id, ''

    @classmethod
    @auto_log
    def delete_workflow(cls, workflow_id):
        """
        删除工作流
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0)
        if workflow_obj:
            workflow_obj.update(is_deleted=True)
        return workflow_id, ''
