import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Workflow, WorkflowAdmin
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.account.account_base_service import AccountBaseService, account_base_service_ins


class WorkflowBaseService(BaseService):
    """
    流程服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_workflow_list(cls, name: str, page: int, per_page: int, workflow_id_list: list, username: str, from_admin:int =1)->tuple:
        """
        获取工作流列表
        get workflow list by params
        :param name:
        :param page:
        :param per_page:
        :param workflow_id_list:workflow id list
        :param username
        :param from_admin 管理后台
        :return:
        """
        query_params = Q(is_deleted=False)
        if name:
            query_params &= Q(name__contains=name)

        if from_admin:
            # 获取有管理权限的工作流列表
            flag, result = cls.get_workflow_manage_list(username)
            if flag is False:
                workflow_id_list = []

            workflow_manage_list = result.get('workflow_list')
            workflow_manage_id_list = [workflow_manage.get('id') for workflow_manage in workflow_manage_list]
            workflow_id_list = list(set(workflow_manage_id_list) - (set(workflow_manage_id_list) - set(workflow_id_list)))

        query_params &= Q(id__in=workflow_id_list)

        workflow_queryset = Workflow.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_queryset, per_page)
        try:
            workflow_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_result_paginator = paginator.page(paginator.num_pages)
        workflow_result_object_list = workflow_result_paginator.object_list
        workflow_result_restful_list = []
        workflow_result_id_list = []
        for workflow_result_object in workflow_result_object_list:
            workflow_result_id_list.append(workflow_result_object.id)
            workflow_result_restful_list.append(
                dict(id=workflow_result_object.id, name=workflow_result_object.name,
                     description=workflow_result_object.description, notices=workflow_result_object.notices,
                     view_permission_check=workflow_result_object.view_permission_check,
                     limit_expression=workflow_result_object.limit_expression,
                     display_form_str=workflow_result_object.display_form_str,
                     creator=workflow_result_object.creator, gmt_created=str(workflow_result_object.gmt_created)[:19],
                     title_template=workflow_result_object.title_template,
                     content_template=workflow_result_object.content_template
                     )
            )
        # 获取工作流管理员信息
        workflow_admin_queryset = WorkflowAdmin.objects.filter(
            workflow_id__in=workflow_result_id_list, is_deleted=0).all()
        for workflow_result_restful in workflow_result_restful_list:
            workflow_admin_list = []
            for workflow_admin_object in workflow_admin_queryset:
                if workflow_admin_object.workflow_id == workflow_result_restful['id']:
                    workflow_admin_list.append(workflow_admin_object.username)

            workflow_result_restful['workflow_admin'] = ','.join(workflow_admin_list)

        return True, dict(workflow_result_restful_list=workflow_result_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def get_workflow_manage_list(cls, username: str)->tuple:
        """
        获取有管理权限的工作流列表
        :param username:
        :return:
        """
        # 如果是admin,拥有所有工作流的权限
        flag, result = account_base_service_ins.admin_permission_check(username=username)
        if flag:
            workflow_queryset = Workflow.objects.filter(is_deleted=0).all()
        else:
            # 作为工作流创建人+工作流管理员的工作流
            workflow_admin_queryset = WorkflowAdmin.objects.filter(username=username, is_deleted=0).all()
            workflow_admin_id_list = [workflow_admin.workflow_id for workflow_admin in workflow_admin_queryset]

            workflow_queryset = Workflow.objects.filter(
                Q(creator=username, is_deleted=0) | Q(id__in=workflow_admin_id_list, is_deleted=0)).all()

        workflow_restful_list = [workflow.get_dict() for workflow in workflow_queryset]

        return True, dict(workflow_list=workflow_restful_list)

    @classmethod
    @auto_log
    def check_new_permission(cls, username: str, workflow_id: int)->tuple:
        """
        判断用户是否有新建工单的权限
        check whether user can create ticket
        :param username:
        :param workflow_id:
        :return:
        """
        # 获取workflow的限制表达式
        flag, workflow_obj = cls.get_by_id(workflow_id)
        if not workflow_obj:
            return False, workflow_obj
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

        from service.ticket.ticket_base_service import ticket_base_service_ins

        if limit_period:
            if limit_expression_dict.get('level'):
                if limit_expression_dict.get('level') == 1:
                    flag, result = ticket_base_service_ins.get_ticket_count_by_args(
                        workflow_id=workflow_id, username=username, period=limit_period)
                    count_result = result.get('count_result')
                elif limit_expression_dict.get('level') == 2:
                    flag, result = ticket_base_service_ins.get_ticket_count_by_args(
                        workflow_id=workflow_id, period=limit_period)
                    count_result = result.get('count_result')
                else:
                    return False, 'level in limit_expression is invalid'
                if count_result is False:
                    return False, result
                if not limit_expression_dict.get('count'):
                    return False, 'count is need when level is not none'
                if count_result > limit_expression_dict.get('count'):
                    return False, '{} tickets can be created in {}hours when workflow_id is {}'\
                        .format(limit_count, limit_period, workflow_id)

        if limit_allow_persons:
            if username not in limit_allow_persons.split(','):
                return False, '{} can not create ticket base on workflow_id:{}'.format(workflow_id)
        if limit_allow_depts:
            # 获取用户所属部门，包含上级部门
            flag, user_all_dept_id_list = AccountBaseService.get_user_up_dept_id_list(username)
            if flag is False:
                return False, user_all_dept_id_list
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
            flag, user_role_list = account_base_service_ins.get_user_role_id_list(username)
            if flag is False:
                return False, user_role_list
            limit_allow_role_str_list = limit_allow_roles.split(',')
            limit_allow_role_id_list = [int(limit_allow_role_str) for limit_allow_role_str in limit_allow_role_str_list]
            limit_allow_role_id_list = list(set(limit_allow_role_id_list))
            total_list = limit_allow_role_id_list + user_role_list
            if len(total_list) == len(set(total_list)):
                return False, 'user is not in allow role'
        return True, ''

    @classmethod
    @auto_log
    def get_by_id(cls, workflow_id: int)->tuple:
        """
        获取工作流 by id
        get workflow object by workflow id
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(is_deleted=0, id=workflow_id).first()
        if not workflow_obj:
            return False, 'workflow is not existed or has been deleted'
        return True, workflow_obj

    @classmethod
    @auto_log
    def add_workflow(cls, name: str, description: str, notices: str, view_permission_check: int, limit_expression: str,
                     display_form_str: str, creator: str, workflow_admin: str, title_template: str,
                     content_template: str)->tuple:
        """
        新增工作流
        add workflow
        :param name:
        :param description:
        :param notices:
        :param view_permission_check:
        :param limit_expression:
        :param display_form_str:
        :param creator:
        :param workflow_admin:
        :param title_template:
        :param content_template:
        :return:
        """
        workflow_obj = Workflow(name=name, description=description, notices=notices,
                                view_permission_check=view_permission_check, limit_expression=limit_expression,
                                display_form_str=display_form_str, creator=creator, title_template=title_template,
                                content_template=content_template)
        workflow_obj.save()
        workflow_admin_insert_list = []
        if workflow_admin:
            for username in workflow_admin.split(','):
                workflow_admin_insert_list.append(WorkflowAdmin(
                    workflow_id=workflow_obj.id, username=username, creator=creator))
            WorkflowAdmin.objects.bulk_create(workflow_admin_insert_list)
        return True, dict(workflow_id=workflow_obj.id)

    @classmethod
    @auto_log
    def edit_workflow(cls, workflow_id: int, name: str, description: str, notices: str, view_permission_check: int,
                      limit_expression: str, display_form_str: str, workflow_admin: str, title_template: str,
                      content_template: str)->tuple:
        """
        更新工作流
        update workfow
        :param workflow_id:
        :param name:
        :param description:
        :param notices:
        :param view_permission_check:
        :param limit_expression:
        :param display_form_str:
        :param workflow_admin:
        :param title_template:
        :param content_template:
        :return:
        """
        workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0)
        if workflow_obj:
            workflow_obj.update(name=name, description=description, notices=notices,
                                view_permission_check=view_permission_check,
                                limit_expression=limit_expression, display_form_str=display_form_str,
                                title_template=title_template, content_template=content_template)
        # 更新工作流管理员
        if workflow_admin:
            workflow_admin_list = workflow_admin.split(',')
            # 查询已经存在的记录
            workflow_admin_existed_queryset = WorkflowAdmin.objects.filter(
                workflow_id=workflow_id, username__in=workflow_admin_list, is_deleted=0).all()
            workflow_admin_existed_list = [workflow_admin_existed.username for workflow_admin_existed
                                           in workflow_admin_existed_queryset]
            # 删除移除掉的
            WorkflowAdmin.objects.filter(workflow_id=workflow_id, is_deleted=0)\
                .exclude(username__in=workflow_admin_list).update(is_deleted=1)

            # 新增新添加的
            workflow_admin_need_add_list = list(set(workflow_admin_list) - set(workflow_admin_existed_list))
            workflow_admin_need_add_insert_list = []
            for workflow_admin_need_add in workflow_admin_need_add_list:
                workflow_admin_need_add_insert_list.append(WorkflowAdmin(
                    workflow_id=workflow_id, username=workflow_admin_need_add))
            WorkflowAdmin.objects.bulk_create(workflow_admin_need_add_insert_list)

        else:
            # 删除所有记录
            WorkflowAdmin.objects.filter(workflow_id=workflow_id, is_deleted=0).update(is_deleted=1)

        return True, ''

    @classmethod
    @auto_log
    def delete_workflow(cls, workflow_id: int)->tuple:
        """
        删除工作流
        delete workflow
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0)
        if workflow_obj:
            workflow_obj.update(is_deleted=True)
        return True, ''


workflow_base_service_ins = WorkflowBaseService()
