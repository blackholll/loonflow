import json
from django.conf import settings
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import Record as WorkflowRecord, Permission as WorkflowPermission, BasicInfo, Version as WorkflowVersion
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.common.log_service import auto_log
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.workflow.workflow_hook_service import workflow_hook_service_ins
from service.workflow.workflow_node_service import workflow_node_service_ins
from service.workflow.workflow_notification_service import workflow_notification_service_ins
from service.workflow.workflow_permission_service import workflow_permission_service_ins
from service.workflow.workflow_component_service import workflow_component_service_ins
from service.workflow.workflow_edge_service import workflow_edge_service_ins


class WorkflowBaseService(BaseService):
    """
    workflow service
    """
    @classmethod
    @transaction.atomic
    def add_workflow(cls, operator_id: str, tenant_id: str, request_data: dict) -> str:
        """
        add workflow
        :param operator_id:
        :param tenant_id:
        :param request_data:
        :return:
        """
        basic_info = request_data.get("basic_info")
        workflow_record_info = WorkflowRecord(tenant_id=tenant_id)
        workflow_record_info.save()
        workflow_id = workflow_record_info.id
        new_version_record = WorkflowVersion(tenant_id=tenant_id, name=basic_info.get('version'), workflow_id=workflow_id, type='default')
        new_version_record.save()
        new_version_id = new_version_record.id
        

        workflow_basic_info = BasicInfo(tenant_id=tenant_id, name=basic_info.get('name'), description=basic_info.get("description"), workflow_id=workflow_id, version_id=new_version_id)
        workflow_basic_info.save()
        
        workflow_notification_service_ins.add_workflow_notification(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))
        workflow_component_service_ins.add_workflow_components(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("form_schema", {}).get("component_info_list"))
        node_id_dict = workflow_node_service_ins.add_workflow_node(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("process_schema", {}).get("node_info_list"))

        edge_info_list = request_data.get("process_schema", {}).get("edge_info_list", [])
        for edge_info in edge_info_list:
            edge_info["source_node_id"] = node_id_dict.get(edge_info.get("source_node_id"))
            edge_info["target_node_id"] = node_id_dict.get(edge_info.get("target_node_id")) 
            
        workflow_edge_service_ins.add_workflow_edges(tenant_id, workflow_id, new_version_id, operator_id, edge_info_list)
        
        workflow_permission_service_ins.add_workflow_permission(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("permission_info", {}))
        workflow_permission_service_ins.add_workflow_app_permission(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("authorized_app_id_list", []))
        workflow_hook_service_ins.add_workflow_hook(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("hook_info_list", []))
        
        return str(workflow_record_info.id)


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
        user_obj = account_user_service_ins.get_user_by_user_id(tenant_id, operator_id)
        if user_obj.type != "admin":
            permission_workflow_id_list = workflow_permission_service_ins.get_user_permission_workflow_id_list(operator_id)
            if permission_workflow_id_list:
                query_params &= Q(id__in=permission_workflow_id_list)

        query_params &= Q(version__type='default')
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
        workflow_queryset = BasicInfo.objects.filter(query_params).order_by('id')
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
            
            if simple:
                workflow_data = dict(id=str(workflow_result_object.id), name=workflow_result_object.name, description=workflow_result_object.description)
            else:
                workflow_data = workflow_result_object.get_dict()
            
            workflow_data['version'] = workflow_result_object.version.name
            workflow_data['workflow_id'] = str(workflow_result_object.workflow_id)
            workflow_info_list.append(workflow_data)
        return dict(workflow_info_list=workflow_info_list, per_page=per_page, page=page, total=paginator.count)


    @classmethod
    @transaction.atomic
    def update_workflow(cls, operator_id: str, tenant_id: str, workflow_id: str, request_data: dict)->str:
        """
        update workflow
        :param workflow_id:
        :param request_data:
        :return:
        """
        current_version = request_data.get("basic_info", {}).get("version")
        current_version_queryset = WorkflowVersion.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, name=current_version).all()
        if current_version_queryset.count() == 0:
            # add a new version
            new_version_record = WorkflowVersion(tenant_id=tenant_id, name=current_version, workflow_id=workflow_id, type='candidate')
            new_version_record.save()
            new_version_id = new_version_record.id

            # add new version whole info
            workflow_basic_info = BasicInfo(tenant_id=tenant_id, name=request_data.get("basic_info", {}).get('name'), description=request_data.get("basic_info", {}).get("description"), workflow_id=workflow_id, version_id=new_version_id)
            workflow_basic_info.save()

            workflow_notification_service_ins.add_workflow_notification(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))
            workflow_component_service_ins.add_workflow_components(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("form_schema", {}).get("component_info_list"))
            node_id_dict = workflow_node_service_ins.add_workflow_node(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("process_schema", {}).get("node_info_list"))

            edge_info_list = request_data.get("process_schema", {}).get("edge_info_list", [])
            for edge_info in edge_info_list:
                edge_info["source_node_id"] = node_id_dict.get(edge_info.get("source_node_id"))
                edge_info["target_node_id"] = node_id_dict.get(edge_info.get("target_node_id")) 
                
            workflow_edge_service_ins.add_workflow_edges(tenant_id, workflow_id, new_version_id, operator_id, edge_info_list)
            
            workflow_permission_service_ins.add_workflow_permission(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("permission_info", {}))
            workflow_permission_service_ins.add_workflow_app_permission(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("authorized_app_id_list", []))
            workflow_hook_service_ins.add_workflow_hook(tenant_id, workflow_id, new_version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("hook_info_list", []))
        else:
            # todo: update exist version's info
            version_id = current_version_queryset.first().id
            BasicInfo.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id).update(name=request_data.get("basic_info", {}).get('name'), description=request_data.get("basic_info", {}).get("description"))

            workflow_notification_service_ins.update_workflow_notification(tenant_id, workflow_id, version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))

            workflow_component_service_ins.update_workflow_components(tenant_id, workflow_id, version_id, operator_id, request_data.get("form_schema", {}).get("component_info_list"))

            node_id_dict = workflow_node_service_ins.update_workflow_node(tenant_id, workflow_id, version_id, operator_id, request_data.get("process_schema", {}).get("node_info_list"))
            edge_info_list = request_data.get("process_schema", {}).get("edge_info_list", [])
            for edge_info in edge_info_list:
                edge_info["source_node_id"] = node_id_dict.get(edge_info.get("source_node_id"))
                edge_info["target_node_id"] = node_id_dict.get(edge_info.get("target_node_id")) 
                
            workflow_edge_service_ins.update_workflow_edges(tenant_id, workflow_id, version_id, operator_id, edge_info_list)

            # update permission
            workflow_permission_service_ins.update_workflow_permission(tenant_id, workflow_id, version_id, operator_id, request_data.get("advanced_schema", {}).get("permission_info", {}))
            # update app permission
            workflow_permission_service_ins.update_workflow_app_permission(tenant_id, workflow_id, version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("authorized_app_id_list", []))
            # update hook
            workflow_hook_service_ins.update_workflow_hook(tenant_id, workflow_id, version_id, operator_id, request_data.get("advanced_schema", {}).get("customization_info", {}).get("hook_info_list", []))
            return True
        
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
        return WorkflowRecord.objects.get(id=workflow_id, tenant_id=tenant_id)

    @classmethod
    def get_workflow_version_list(cls, workflow_id: str, tenant_id: str, operator_id: str, search_value: str, page: int, per_page: int) -> dict:
        """
        get workflow version list
        :param workflow_id:
        :return:
        """
        query_params = Q(workflow_id=workflow_id, tenant_id=tenant_id)
        if search_value:
            query_params &= Q(name__contains=search_value)
        workflow_version_queryset = WorkflowVersion.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_version_queryset, per_page)
        try:
            workflow_version_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_version_result_paginator = paginator.page(1)
        except EmptyPage:
            workflow_version_result_paginator = paginator.page(paginator.num_pages)
        workflow_version_result_object_list = workflow_version_result_paginator.object_list
        workflow_version_info_list = [] 
        for workflow_version_result_object in workflow_version_result_object_list:
            workflow_version_info_list.append(workflow_version_result_object.get_dict())
        return dict(version_info_list=workflow_version_info_list, per_page=per_page, page=page, total=paginator.count)

    @classmethod
    def get_ticket_creation_form(cls, workflow_id: str, tenant_id: str, operator_id: str, version_name: str) -> dict:
        """
        get ticket creation form
        :param workflow_id:
        :param tenant_id:
        :param operator_id:
        :param version_name:
        :return:
        """
        if version_name:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, name=version_name)
        else:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, type='default')

        form_schema_component_list = workflow_component_service_ins.get_workflow_fd_component_list(tenant_id, workflow_id, version_obj.id)
        
        # need filter with init node's component list

        init_node_field_permissions = workflow_node_service_ins.get_init_node_field_permissions(tenant_id, workflow_id, version_obj.id)
        result_component_list = []
        for component in form_schema_component_list:
            if component['type'] == 'row':
                for child_component in component['children']:
                    children_length = 0
                    if init_node_field_permissions.get(child_component['component_key']) is not None and init_node_field_permissions.get(child_component['component_key']) != 'hidden' :
                        child_component['required'] = (init_node_field_permissions.get(child_component['component_key'])== 'required')
                        result_component_list.append(child_component)
                        children_length += 1
                if children_length != 0:
                    result_component_list.append(component)
                
        return result_component_list

    @classmethod
    def get_ticket_creation_actions(cls, workflow_id: str, tenant_id: str, operator_id: str, version_name: str) -> dict:
        """
        get ticket creation actions
        :param workflow_id:
        :param tenant_id:
        :param operator_id:
        :param version_name:
        :return:
        """
        if version_name:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, name=version_name)
        else:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, type='default')
        
        init_node = workflow_node_service_ins.get_init_node(tenant_id, workflow_id, version_obj.id)

        edge_info_list = workflow_edge_service_ins.get_workflow_edges_by_source_node_id(tenant_id, workflow_id, version_obj.id, init_node.id)
        action_result_list = []
        for edge_info in edge_info_list:
            action_result_list.append(dict(
                id=str(edge_info.id),
                name=edge_info.name,
                type=edge_info.type,
                props=edge_info.props
            ))
        return action_result_list


    @classmethod
    def get_workflow_version_id_by_name(cls, workflow_id: str, tenant_id: str, version_name: str) -> str:
        """
        get workflow version id
        :param workflow_id:
        :param tenant_id:
        :param version_name:
        :return:
        """
        if version_name:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, name=version_name)
            if version_obj.type == 'archived':
                raise CustomCommonException('workflow version is archived')
        else:
            version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, type='default')
        return version_obj.id

    @classmethod
    def get_workflow_node_form(cls, tenant_id: str, workflow_id: str, version_id: str, node_id: str) -> dict:
        """
        get workflow node form
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_id:
        :return:
        """
        node_obj = workflow_node_service_ins.get_node_by_id(tenant_id, workflow_id, version_id, node_id)
        node_props = node_obj.props
        node_type = node_obj.type
        if node_type == 'end':
            return cls.get_workflow_view_form(tenant_id, workflow_id, version_id, node_id)
        node_form_permission = node_props.get('field_permissions', {})
        result_component_list = []
        form_schema_component_list = workflow_component_service_ins.get_workflow_fd_component_list(tenant_id, workflow_id, version_id)

        for component in form_schema_component_list:
            if component['type'] == 'row':
                new_children = []
                for child_component in component['children']:
                    children_length = 0
                    if node_form_permission.get(child_component['component_key']) is not None and node_form_permission.get(child_component['component_key']) != 'hidden' :
                        child_component['required'] = (node_form_permission.get(child_component['component_key'])== 'required')
                        new_children.append(child_component)
                        children_length += 1
                if children_length != 0:
                    component['children'] = new_children
                    result_component_list.append(component)
        return result_component_list
        

        


    @classmethod
    def get_workflow_view_form(cls, tenant_id: str, workflow_id: str, version_id: str) -> dict:
        """
        get workflow view form, can control special component's visibility by configure tomorrow
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_id:
        :return:
        """
        return workflow_component_service_ins.get_workflow_fd_component_list(tenant_id, workflow_id, version_id)

    
    @classmethod
    def get_workflow_info_by_id_and_version_id(cls, tenant_id: str, workflow_id: str, version_id: str) -> dict:
        """
        get workflow info by id and version id
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        workflow_obj = BasicInfo.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id)
        return workflow_obj.get_dict()


############## below are waiting for update
    @classmethod
    @auto_log
    def get_workflow_manage_list(cls, user_id: str)->tuple:
        """
        获取有管理权限的工作流列表
        :param user_id:
        :return:
        """
        # 如果是超级管理员,拥有所有工作流的权限
        flag, result = account_base_service_ins.admin_permission_check(username=username)
        if flag:
            workflow_queryset = WorkflowRecord.objects.filter(is_deleted=0).all()
        else:
            # 作为工作流创建人+工作流管理员的工作流
            workflow_admin_queryset = WorkflowPermission.objects.filter(permission='admin', user_type='user', user=username).all()
            workflow_admin_id_list = [workflow_admin.workflow_id for workflow_admin in workflow_admin_queryset]

            workflow_queryset = WorkflowRecord.objects.filter(
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
        workflow_obj = WorkflowRecord.objects.filter(is_deleted=0, id=workflow_id).first()
        if not workflow_obj:
            return False, 'workflow is not existed or has been deleted'
        return True, workflow_obj

    @classmethod
    def get_full_definition_info_by_id(cls, tenant_id: str, workflow_id: str, version_name: str='')->tuple:
        """
        get full definition of workflow
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        try:
            if version_name:
                version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, name=version_name)
                if version_obj.type == 'archived':
                    raise CustomCommonException('version is archived, does not support to get full definition')
            else:
                version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, type='default')
                if version_obj.type == 'archived':
                    raise CustomCommonException('version is archived, does not support to get full definition')
        except WorkflowVersion.DoesNotExist:
            raise CustomCommonException('version is not existed or has been deleted')

        # basicinfo
        basic_info_obj = BasicInfo.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_obj.id)
        basic_info = dict(
            id=workflow_id,
            name=basic_info_obj.name,
            description=basic_info_obj.description,
            version=version_obj.name,
            tenant_id=str(basic_info_obj.tenant_id),
            label=basic_info_obj.label
        )

        form_schema_component_list = workflow_component_service_ins.get_workflow_fd_component_list(tenant_id, workflow_id, version_obj.id)
        process_schema_node_list = workflow_node_service_ins.get_workflow_fd_node_list(tenant_id, workflow_id, version_obj.id)
        process_schema_edge_list = workflow_edge_service_ins.get_workflow_fd_edge_list(tenant_id, workflow_id, version_obj.id)
        

        notification_result = workflow_notification_service_ins.get_workflow_fd_notification(tenant_id, workflow_id, version_obj.id)
        
        workflow_permission_result = workflow_permission_service_ins.get_workflow_fd_permission(tenant_id, workflow_id, version_obj.id)
        
        workflow_authorized_app_id_list = workflow_permission_service_ins.get_workflow_fd_authorized_app_id_list(tenant_id, workflow_id, version_obj.id)

        workflow_hook_result = workflow_hook_service_ins.get_workflow_fd_hook_list(tenant_id, workflow_id, version_obj.id)

        label = basic_info_obj.label
        basic_info.pop('label')
        
        return dict(
            basic_info=basic_info,
            form_schema={'component_info_list': form_schema_component_list},
            process_schema={'node_info_list': process_schema_node_list, 'edge_info_list': process_schema_edge_list},
            advanced_schema={'notification_info': notification_result, 'permission_info': workflow_permission_result, 'customization_info': {
                'authorized_app_id_list': workflow_authorized_app_id_list,
                'hook_info_list': workflow_hook_result
            }},
            label=label
        )



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
        workflow_obj = WorkflowRecord.objects.filter(id=workflow_id)
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
        workflow_obj = WorkflowRecord.objects.filter(id=workflow_id)
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
        workflow_query_obj = WorkflowRecord.objects.filter(id=workflow_id).first()
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
