import copy
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
        label = request_data.get("advanced_schema", {}).get("customization_info", {}).get("label", {})
        

        workflow_basic_info = BasicInfo(tenant_id=tenant_id, name=basic_info.get('name'), description=basic_info.get("description"), workflow_id=workflow_id, version_id=new_version_id, label=label)
        workflow_basic_info.save()
        
        workflow_notification_service_ins.add_workflow_notification(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))
        workflow_component_service_ins.add_workflow_components(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("form_schema", {}).get("component_info_list"))
        node_id_dict = workflow_node_service_ins.add_workflow_node(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("process_schema", {}).get("node_info_list"), request_data.get("form_schema", {}).get("component_info_list"))

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
        if user_obj.type != "admin" and not simple:
            permission_workflow_id_list = workflow_permission_service_ins.get_user_permission_workflow_id_list(operator_id)
            if permission_workflow_id_list:
                query_params &= Q(id__in=permission_workflow_id_list)

        query_params &= Q(version__type='default')
        if search_value:
            query_params &= Q(name__contains=search_value) | Q(description__contains=search_value)
        workflow_queryset = BasicInfo.objects.filter(query_params).order_by('-created_at')
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
        label = request_data.get("advanced_schema", {}).get("customization_info", {}).get("label", {})
        if current_version_queryset.count() == 0:
            # add a new version
            new_version_record = WorkflowVersion(tenant_id=tenant_id, name=current_version, workflow_id=workflow_id, type='candidate')
            new_version_record.save()
            new_version_id = new_version_record.id

            # add new version whole info
            workflow_basic_info = BasicInfo(tenant_id=tenant_id, name=request_data.get("basic_info", {}).get('name'), description=request_data.get("basic_info", {}).get("description"), workflow_id=workflow_id, version_id=new_version_id, label=label)
            workflow_basic_info.save()

            workflow_notification_service_ins.add_workflow_notification(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))
            workflow_component_service_ins.add_workflow_components(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("form_schema", {}).get("component_info_list"))
            node_id_dict = workflow_node_service_ins.add_workflow_node(operator_id, tenant_id, workflow_id, new_version_id, request_data.get("process_schema", {}).get("node_info_list"), request_data.get("form_schema", {}).get("component_info_list"))

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
            BasicInfo.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id).update(name=request_data.get("basic_info", {}).get('name'), description=request_data.get("basic_info", {}).get("description"), label=label)

            workflow_notification_service_ins.update_workflow_notification(tenant_id, workflow_id, version_id, request_data.get("advanced_schema", {}).get("notification_info", {}))

            workflow_component_service_ins.update_workflow_components(tenant_id, workflow_id, version_id, operator_id, request_data.get("form_schema", {}).get("component_info_list"))

            node_id_dict = workflow_node_service_ins.update_workflow_node(tenant_id, workflow_id, version_id, operator_id, request_data.get("process_schema", {}).get("node_info_list"),request_data.get("form_schema", {}).get("component_info_list"))
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
    def get_workflow_version_detail(cls, workflow_id: str, version_id: str, tenant_id: str, operator_id: str) -> dict:
        """
        get workflow version detail
        :param workflow_id:
        :param version_id:
        :param tenant_id:
        :param operator_id:
        :return:
        """
        version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, id=version_id)
        return version_obj.get_dict()
    @classmethod
    def update_workflow_version(cls, workflow_id: str, version_id: str, tenant_id: str, operator_id: str, name: str, description: str, type: str) -> bool:
        """
        update workflow version, only allow one default version, and also must have one default version
        :param workflow_id:
        :param version_id:
        :param tenant_id:
        :param operator_id:
        :return:
        """
        default_version_count = WorkflowVersion.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, type='default').count()
        
        version_obj = WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, id=version_id)
        if version_obj.type != 'default' and type == 'default' and default_version_count == 1:
            raise CustomCommonException('can only exist one default version, please change other default version to candidate or archived first')
        version_obj.name = name
        version_obj.description = description
        version_obj.type = type
        version_obj.save()
        return True

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
                new_children_length = 0
                new_children = []
                for child_component in component['children']:
                    if init_node_field_permissions.get(child_component['component_key']) is not None and init_node_field_permissions.get(child_component['component_key']) != 'hidden' :
                        child_component['component_permission'] = (init_node_field_permissions.get(child_component['component_key']))
                        new_children.append(child_component)
                        new_children_length += 1
                if new_children_length != 0:
                    new_component = copy.deepcopy(component)
                    new_component['children'] = new_children
                    result_component_list.append(new_component)
        workflow_basic_obj = workflow_base_service_ins.get_workflow_basic_info_by_id(tenant_id, workflow_id, version_obj.id)

        workflow_metadata = dict(
            id=workflow_id,
            name=workflow_basic_obj.get('name'),
            version_id=str(version_obj.id),
            version_name=version_obj.name,
            description=workflow_basic_obj.get('description')
        )        
        return result_component_list, workflow_metadata

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
        node_obj = workflow_node_service_ins.get_node_by_id(tenant_id, node_id)
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
                children_length = 0
                for child_component in component['children']:
                    if node_form_permission.get(child_component['component_key']) is not None and node_form_permission.get(child_component['component_key']) != 'hidden' :
                        child_component['component_permission'] = (node_form_permission.get(child_component['component_key']))
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


    @classmethod
    def get_workflow_basic_info_by_id(cls, tenant_id: str, workflow_id: str, version_id: str) -> dict:
        """
        get workflow basic info by id
        :param tenant_id:
        :param workflow_id:
        :return:
        """
        return BasicInfo.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id).get_dict()


    @classmethod
    def get_workflow_version_info_by_id(cls, tenant_id: str, workflow_id: str, id: str) -> dict:
        """
        get workflow version by id
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        return WorkflowVersion.objects.get(workflow_id=workflow_id, tenant_id=tenant_id, id=id).get_dict()
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
                'hook_info_list': workflow_hook_result,
                'label': label
            }}
        )

    def get_process_single_schema(cls, workflow_id: str, tenant_id: str, version_id: str) -> dict:
        """
        get process single schema
        :param workflow_id:
        :param tenant_id:
        :param version_name:
        :return:
        """
        process_schema_node_list = workflow_node_service_ins.get_workflow_fd_node_list(tenant_id, workflow_id, version_id)
        process_schema_edge_list = workflow_edge_service_ins.get_workflow_fd_edge_list(tenant_id, workflow_id, version_id)
        
        # remove 
        return dict(node_info_list=process_schema_node_list, edge_info_list=process_schema_edge_list)

workflow_base_service_ins = WorkflowBaseService()
