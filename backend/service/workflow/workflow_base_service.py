import json
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Workflow, WorkflowPermission
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.common.log_service import auto_log
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.workflow.workflow_custom_field_service import workflow_custom_field_service_ins
from service.workflow.workflow_hook_service import workflow_hook_service_ins
from service.workflow.workflow_node_service import workflow_node_service_ins
from service.workflow.workflow_notice_service import workflow_notice_service_ins
from service.workflow.workflow_permission_service import workflow_permission_service_ins
from service.workflow.workflow_state_service import workflow_state_service_ins
from service.workflow.workflow_transition_service import workflow_transition_service_ins


class WorkflowBaseService(BaseService):
    """
    workflow service
    """
    @classmethod
    def add_workflow(cls, operator_id: int, tenant_id: int, request_data: dict) -> int:
        """
        add workflow
        :param operator_id:
        :param tenant_id:
        :param request_data:
        :return:
        """
        basic_info = request_data.get("basic_info")
        workflow_info = Workflow(name=basic_info.get('name'), description=basic_info.get("description"))
        workflow_info.save()
        workflow_id = workflow_info.id
        workflow_notice_service_ins.add_workflow_notice(operator_id, tenant_id, workflow_id, request_data.get("notice_info"))
        workflow_custom_field_service_ins.add_workflow_custom_field(tenant_id, workflow_id, request_data.get("field_info_list"))
        node_dict = workflow_node_service_ins.add_workflow_node(operator_id, tenant_id, workflow_id, request_data.get("node_info_list"))
        workflow_transition_service_ins.add_workflow_transition(tenant_id, workflow_id, operator_id, node_dict, request_data.get("transition_info_list"))
        workflow_permission_service_ins.add_workflow_permission(tenant_id, workflow_id, operator_id, request_data.get("permission_info"))
        workflow_hook_service_ins.add_workflow_hook(tenant_id, workflow_id, operator_id, request_data.get("hook_info_list"))
        return workflow_info.id

    @classmethod
    def get_workflow_list(cls, tenant_id: int, operator_id: int, search_value: str, page: int, per_page: int, simple=False) ->dict:
        """
        get workflow list
        :param tenant_id:
        :param operator_id:
        :param search_value:
        :param page:
        :param per_page:
        :param simple: whether return simple data, which mean only include record's id, name
        :return:
        """
        query_params = Q(tenant_id=tenant_id)
        user_obj = account_user_service_ins.get_user_by_user_id(operator_id)
        if user_obj.type != "admin":
            permission_workflow_id_list = workflow_permission_service_ins.get_user_permission_workflow_id_list(operator_id)
            if permission_workflow_id_list:
                query_params &= Q(id__in=permission_workflow_id_list)

        if search_value:
            query_params &= Q(name__contains=search_value)
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
        workflow_info_list = []
        for workflow_result_object in workflow_result_object_list:
            workflow_simple_data = dict(id=workflow_result_object.id, name=workflow_result_object.name,
                                        decription=workflow_result_object.description)
            workflow_info_list.append(workflow_simple_data)
        return dict(workflow_info_list=workflow_info_list, per_page=per_page, page=page, total=paginator.count)

    @classmethod
    def get_workflow_init_node_rest(cls, workflow_id: int) -> dict:
        """
        get workflow's init node info, it includes init node info, init node's transition list
        :param workflow_id:
        :return:
        node_info, transition_info_list,
        """
        init_node = workflow_node_service_ins.get_init_node_rest(workflow_id)
        transition_info_list = workflow_transition_service_ins.get_node_transition_rest(init_node.get('id'))

        return dict(node_info=init_node, transition_info_list=transition_info_list)

    @classmethod
    def get_workflow_record_by_id(cls, tenant_id: int, workflow_id: int) -> dict:
        """
        get workflow record by id
        :param workflow_id:
        :return:
        """
        return Workflow.objects.get(id=workflow_id, tenant_id=tenant_id)



############## below are waiting for update
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
            workflow_admin_queryset = WorkflowPermission.objects.filter(permission='admin', user_type='user', user=username).all()
            workflow_admin_id_list = [workflow_admin.workflow_id for workflow_admin in workflow_admin_queryset]

            workflow_queryset = Workflow.objects.filter(
                Q(creator=username) | Q(id__in=workflow_admin_id_list)).all()

        workflow_restful_list = [workflow.get_dict() for workflow in workflow_queryset]

        return True, dict(workflow_list=workflow_restful_list)


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
        permission_queryset = WorkflowPermission.objects.filter(workflow_id=workflow_id).all()
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
        workflow_obj = Workflow.objects.filter(id=workflow_id)
        if workflow_obj:
            workflow_obj.update(name=name, description=description, notices=notices,
                                view_permission_check=view_permission_check,
                                limit_expression=limit_expression, display_form_str=display_form_str,
                                title_template=title_template, content_template=content_template)
        # 更新管理员信息
        workflow_permission_existed_queryset = WorkflowPermission.objects.filter(workflow_id=workflow_id).all()

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

        WorkflowPermission.objects.filter(
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
            need_add_permission_queryset.append(WorkflowPermission(
                workflow_id=workflow_id, permission='intervene', user_type='user', user=need_add_intervener))

        for need_add_admin in need_add_admin_list:
            need_add_permission_queryset.append(WorkflowPermission(
                workflow_id=workflow_id, permission='admin', user_type='user', user=need_add_admin))

        for need_add_view_depts in need_add_view_depts_list:
            need_add_permission_queryset.append(WorkflowPermission(
                workflow_id=workflow_id, permission='view', user_type='department', user=need_add_view_depts))

        for need_add_view_persons in need_add_view_persons_list:
            need_add_permission_queryset.append(WorkflowPermission(
                workflow_id=workflow_id, permission='view', user_type='user', user=need_add_view_persons))

        for need_add_app in need_add_app_list:
            need_add_permission_queryset.append(WorkflowPermission(
                workflow_id=workflow_id, permission='api', user_type='app', user=need_add_app))

        WorkflowPermission.objects.bulk_create(need_add_permission_queryset)

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
        workflow_obj = Workflow.objects.filter(id=workflow_id)
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
        workflow_query_obj = Workflow.objects.filter(id=workflow_id).first()
        if not workflow_query_obj:
            return False, 'workflow is not existed'
        if username == workflow_query_obj.creator:
            return True, True

        permission_queryset = WorkflowPermission.objects.filter(permission__in=['admin', 'intervene'],
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
            # In order to maintain compatibility with older versions, no configure means allow all
            return True, ''
        if host_allowed_list:
            from urllib.parse import urlparse
            res = urlparse(url)
            host = res.netloc
            if host in host_allowed_list:
                return True, ''
        return False, 'hook host is not allowed, please contact the administrator to alter the configure'


workflow_base_service_ins = WorkflowBaseService()
