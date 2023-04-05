import json
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Workflow, WorkflowAdmin, WorkflowUserPermission
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.common.log_service import auto_log
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.workflow.workflow_state_service import workflow_state_service_ins
from service.workflow.workflow_transition_service import workflow_transition_service_ins


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
            workflow_info = dict(
                id=workflow_result_object.id,
                name=workflow_result_object.name,
                description=workflow_result_object.description
            )
            if from_admin:
                workflow_info.update(dict(
                     notices=workflow_result_object.notices,
                    view_permission_check=workflow_result_object.view_permission_check,
                    limit_expression=workflow_result_object.limit_expression,
                    display_form_str=workflow_result_object.display_form_str,
                    creator=workflow_result_object.creator, gmt_created=str(workflow_result_object.gmt_created)[:19],
                    title_template=workflow_result_object.title_template,
                    content_template=workflow_result_object.content_template
                ))
            workflow_result_restful_list.append(workflow_info)
        # 获取工作流管理员信息
        if from_admin:
            workflow_admin_queryset = WorkflowUserPermission.objects.filter(workflow_id__in=workflow_result_id_list, permission='admin', is_deleted=0).all()

            for workflow_result_restful in workflow_result_restful_list:
                workflow_admin_list = []
                for workflow_admin_object in workflow_admin_queryset:
                    if workflow_admin_object.workflow_id == workflow_result_restful['id']:
                        workflow_admin_list.append(workflow_admin_object.user)

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
        # 如果是超级管理员,拥有所有工作流的权限
        flag, result = account_base_service_ins.admin_permission_check(username=username)
        if flag:
            workflow_queryset = Workflow.objects.filter(is_deleted=0).all()
        else:
            # 作为工作流创建人+工作流管理员的工作流
            workflow_admin_queryset = WorkflowUserPermission.objects.filter(permission='admin', user_type='user', user=username, is_deleted=0).all()
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
        limit_level = limit_expression_dict.get('level')
        limit_count = limit_expression_dict.get('count')
        limit_allow_persons = limit_expression_dict.get('allow_persons')
        limit_allow_depts = limit_expression_dict.get('allow_depts')
        limit_allow_roles = limit_expression_dict.get('allow_roles')

        from service.ticket.ticket_base_service import ticket_base_service_ins

        if limit_period:
            if limit_level:
                if limit_level == 1:
                    flag, result = ticket_base_service_ins.get_ticket_count_by_args(
                        workflow_id=workflow_id, username=username, period=limit_period)
                    count_result = result.get('count_result')
                elif limit_level == 2:
                    flag, result = ticket_base_service_ins.get_ticket_count_by_args(
                        workflow_id=workflow_id, period=limit_period)
                    count_result = result.get('count_result')
                else:
                    return False, 'level in limit_expression is invalid'
                if count_result is False:
                    return False, result
                if not limit_count:
                    return False, 'count is need when level is not none'
                if count_result >= limit_count:
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
    def get_full_info_by_id(cls, workflow_id: int)->tuple:
        """
        获取工作流详细详情，包括关联数据。管理员， 干预人，查看权限人，查看权限部门，授权应用
        :param workflow_id:
        :return:
        """
        workflow_obj = Workflow.objects.filter(is_deleted=0, id=workflow_id).first()

        # 权限人
        permission_queryset = WorkflowUserPermission.objects.filter(workflow_id=workflow_id, is_deleted=0).all()
        adminer_list = []
        intervener_list = []
        viewer_username_list = []
        viewer_dept_id_list = []
        app_for_api_id_list = []
        for permission_obj in permission_queryset:
            if permission_obj.permission == 'admin':
                adminer_list.append(permission_obj.user)
            elif permission_obj.permission == 'intervene':
                intervener_list.append(permission_obj.user)
            elif permission_obj.permission == 'view':
                if permission_obj.user_type == 'user':
                    viewer_username_list.append(permission_obj.user)
                if permission_obj.user_type == 'department':
                    viewer_dept_id_list.append(permission_obj.user)
            elif permission_obj.permission == 'api':
                app_for_api_id_list.append(permission_obj.user)

        workflow_info_dict = workflow_obj.get_dict()
        workflow_info_dict['workflow_admin'] = adminer_list
        workflow_info_dict['intervener'] = intervener_list
        workflow_info_dict['view_persons'] = viewer_username_list
        workflow_info_dict['view_depts'] = viewer_dept_id_list
        workflow_info_dict['api_permission_apps'] = app_for_api_id_list
        return True, workflow_info_dict

    @classmethod
    @auto_log
    def add_workflow(cls, name: str, description: str, notices: str, view_permission_check: int, limit_expression: str,
                     display_form_str: str, creator: str, workflow_admin: str, title_template: str,
                     content_template: str, intervener: str, view_depts:str, view_persons:str, api_permission_apps:str)->tuple:
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

        intervener_list = intervener.split(',') if intervener else []
        workflow_admin_list = workflow_admin.split(',') if workflow_admin else []
        view_depts_list = view_depts.split(',') if view_depts else []
        view_persons_list = view_persons.split(',') if view_persons else []
        api_permission_app_list = api_permission_apps.split(',') if api_permission_apps else []

        workflow_id = workflow_obj.id
        need_add_permission_queryset = []
        for need_add_intervener in intervener_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='intervene', user_type='user', user=need_add_intervener))

        for need_add_admin in workflow_admin_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='admin', user_type='user', user=need_add_admin))

        for need_add_view_depts in view_depts_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='view', user_type='department', user=need_add_view_depts))

        for need_add_view_persons in view_persons_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='view', user_type='user', user=need_add_view_persons))

        for need_add_app in api_permission_app_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='api', user_type='app', user=need_add_app))

        WorkflowUserPermission.objects.bulk_create(need_add_permission_queryset)

        return True, dict(workflow_id=workflow_obj.id)

    @classmethod
    @auto_log
    def edit_workflow(cls, workflow_id: int, name: str, description: str, notices: str, view_permission_check: int,
                      limit_expression: str, display_form_str: str, workflow_admin: str, title_template: str,
                      content_template: str, intervener: str, view_depts: str, view_persons: str, api_permission_apps:str)->tuple:
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
        # 更新管理员信息
        workflow_permission_existed_queryset = WorkflowUserPermission.objects.filter(workflow_id=workflow_id, is_deleted=0).all()

        existed_intervener,  existed_workflow_admin, existed_view_depts, existed_view_persons, \
        existed_app_permission_apps = [], [], [], [], []
        for workflow_permission_existed in workflow_permission_existed_queryset:
            if workflow_permission_existed.permission == 'intervene':
                existed_intervener.append(workflow_permission_existed.user)
            if workflow_permission_existed.permission == 'admin':
                existed_workflow_admin.append(workflow_permission_existed.user)
            if workflow_permission_existed.permission == 'view' and workflow_permission_existed.user_type == 'department':
                existed_view_depts.append(workflow_permission_existed.user)
            if workflow_permission_existed.permission == 'view' and workflow_permission_existed.user_type == 'user':
                existed_view_persons.append(workflow_permission_existed.user)
            if workflow_permission_existed.permission == 'api' and workflow_permission_existed.user_type == 'app':
                existed_app_permission_apps.append(workflow_permission_existed.user)

        # need del

        intervener_list = intervener.split(',') if intervener else []
        workflow_admin_list = workflow_admin.split(',') if workflow_admin else []
        view_depts_list = view_depts.split(',') if view_depts else []
        view_persons_list = view_persons.split(',') if view_persons else []
        api_list = api_permission_apps.split(',') if api_permission_apps else []


        flag, need_del_intervener_list = common_service_ins.list_subtraction(existed_intervener, intervener_list)

        flag, need_del_admin_list = common_service_ins.list_subtraction(existed_workflow_admin, workflow_admin_list)

        flag, need_del_view_depts_list = common_service_ins.list_subtraction(existed_view_depts, view_depts_list)

        flag, need_del_view_persons_list = common_service_ins.list_subtraction(existed_view_persons, view_persons_list)

        flag, need_del_app_list = common_service_ins.list_subtraction(existed_app_permission_apps, api_list)

        WorkflowUserPermission.objects.filter(
            Q(workflow_id=workflow_id, permission='intervene', user_type='user', user__in=need_del_intervener_list) |
            Q(workflow_id=workflow_id, permission='admin', user_type='user', user__in=need_del_admin_list) |
            Q(workflow_id=workflow_id, permission='view', user_type='user', user__in=need_del_view_persons_list) |
            Q(workflow_id=workflow_id, permission='view', user_type='department', user__in=need_del_view_depts_list) |
            Q(workflow_id=workflow_id, permission='api', user_type='app', user__in=need_del_app_list)
        ).update(is_deleted=1)

        # need add
        flag, need_add_intervener_list = common_service_ins.list_subtraction(intervener_list, existed_intervener)
        flag, need_add_admin_list = common_service_ins.list_subtraction(workflow_admin_list, existed_workflow_admin)
        flag, need_add_view_depts_list = common_service_ins.list_subtraction(view_depts_list, existed_view_depts)
        flag, need_add_view_persons_list = common_service_ins.list_subtraction(view_persons_list, existed_view_persons)
        flag, need_add_app_list = common_service_ins.list_subtraction(api_list, existed_app_permission_apps)

        need_add_permission_queryset = []
        for need_add_intervener in need_add_intervener_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='intervene', user_type='user', user=need_add_intervener))

        for need_add_admin in need_add_admin_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='admin', user_type='user', user=need_add_admin))

        for need_add_view_depts in need_add_view_depts_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='view', user_type='department', user=need_add_view_depts))

        for need_add_view_persons in need_add_view_persons_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='view', user_type='user', user=need_add_view_persons))

        for need_add_app in need_add_app_list:
            need_add_permission_queryset.append(WorkflowUserPermission(
                workflow_id=workflow_id, permission='api', user_type='app', user=need_add_app))

        WorkflowUserPermission.objects.bulk_create(need_add_permission_queryset)

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

    @classmethod
    @auto_log
    def get_simple_description(cls, workflow_id: int)->tuple:
        """
        获取简单描述
        :param workflow_id:
        :return:
        """
        flag, workflow_detail = cls.get_by_id(workflow_id)
        if flag is False:
            return flag, workflow_detail

        flag, state_list = workflow_state_service_ins.get_workflow_states(workflow_id)
        if flag is False:
            return flag, state_list

        flag, transition_list = workflow_transition_service_ins.get_transition_by_args(dict(workflow_id=workflow_id))
        if flag is False:
            return flag, transition_list

        workflow_basic_info = dict(id=workflow_detail.id, name=workflow_detail.name)
        workflow_state_info = []
        for state in state_list:
            workflow_state_info.append(dict(id=state.id, name=state.name))
        workflow_transition_info = []
        for transition in transition_list:
            workflow_transition_info.append(
                dict(id=transition.id, name=transition.name, source_state_id=transition.source_state_id,
                     destination_state_id=transition.destination_state_id,
                     condition_expression=transition.condition_expression,
                     attribute_type_id=transition.attribute_type_id, timer=transition.timer
                     ))
        result = dict(workflow_basic_info=workflow_basic_info, workflow_state_info=workflow_state_info,
                      workflow_transition_info=workflow_transition_info)
        return True, result

    @classmethod
    @auto_log
    def get_permission_list_by_args(cls, app_namelist, role):
        pass

    @classmethod
    @auto_log
    def can_intervene(cls, workflow_id, username):
        """
        判断用户是否有对此工作流对应工单的干预权限
        :param workflow_id:
        :param username:
        :return:
        """
        # todo: intervene列表， 创建人，管理员
        workflow_query_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0).first()
        if not workflow_query_obj:
            return False, 'workflow is not existed'
        if username == workflow_query_obj.creator:
            return True, True

        permission_queryset = WorkflowUserPermission.objects.filter(permission__in=['admin', 'intervene'], is_deleted=0,
                                                                    user_type='user').all()
        for permission in permission_queryset:
            if permission.user == username:
                return True, True
        return True, False

    @classmethod
    @auto_log
    def get_statistics(cls, workflow_id, start_time, end_time):
        """
        对应工单数量统计数据
        :param workflow_id:
        :param start_time:
        :param end_time:
        :return:
        """
        from django.db.models import Count
        query_params = {'is_deleted': 0, 'workflow_id': workflow_id}
        if start_time:
            query_params['gmt_created__gte'] = start_time
        if end_time:
            query_params['gmt_created__lte'] = end_time

        from apps.ticket.models import TicketRecord
        queryset_result = TicketRecord.objects.filter(**query_params).extra(
            select={'year': 'year(gmt_created)', 'month': 'month(gmt_created)', 'day': 'day(gmt_created)',
                    'workflow_id': 'workflow_id'}).values('year', 'month', 'day', 'workflow_id').annotate(
            count_len=Count('gmt_created')).order_by()

        result_list = []
        for queryset in queryset_result:
            date_str = '%d-%02d-%02d' % (queryset['year'], queryset['month'], queryset['day'])

            result_list.append(dict(day=date_str, count=queryset['count_len']))
        # 按日期排序
        result_list = sorted(result_list, key=lambda r: r['day'])

        return True, dict(result_list=result_list)

    @classmethod
    @auto_log
    def hook_host_valid_check(cls, url):
        """
        check the hook host is valid or not
        """
        try:
            host_allowed_list = settings.HOOK_HOST_ALLOWED
        except Exception as e:
            # 兼容历史版本，未设置该配置则允许所有
            return True, ''
        if host_allowed_list:
            from urllib.parse import urlparse
            res = urlparse(url)
            host = res.netloc
            if host in host_allowed_list:
                return True, ''
        return False, 'hook host is not allowed, please contact the administrator to alter the configure'


workflow_base_service_ins = WorkflowBaseService()
