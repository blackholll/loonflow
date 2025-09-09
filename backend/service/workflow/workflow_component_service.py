from calendar import c
import json
from math import e
import time
import copy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.workflow.models import Component
from service.base_service import BaseService
from service.common.log_service import auto_log
from service.util.archive_service import archive_service_ins


class WorkflowComponentService(BaseService):

    @classmethod
    def update_workflow_components(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id:str, component_info_list: list):
        """
        update workflow component, means tenant_id, workflow_id, version_id is already exist
        :param tenant_id:
        :param workflow_id:
        :param component_info_list:
        :return:
        """
        # need to check whether the component should be insert, update or delete
        # if the id start with temp_, means it is a new component, need to insert
        
        exist_componet_queryset = Component.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        exist_componet_dict = {str(component.id): component for component in exist_componet_queryset}
        
        id_to_new_id_dict = {}
        for component_info in component_info_list:
            # if id is startswith 'temp_', means it is a new component, need to insert
            if component_info.get("id").startswith('temp_'):
                new_component_info = copy.deepcopy(component_info)  
                new_component_info.pop('id')
                new_component_info = {**new_component_info, 'tenant_id': tenant_id, 'workflow_id': workflow_id, 'version_id': version_id}
                new_componet_record = Component(**new_component_info)
                new_componet_record.save()
                id_to_new_id_dict[component_info.get("id")] = new_component_info.id
                # for children
                for child_info in component_info.get("children"):
                    if child_info.get("id").startswith('temp_'):
                        new_child_component_info = copy.deepcopy(child_info)
                        new_child_component_info.pop('id')
                        new_child_component_info = {**new_child_component_info, 'tenant_id': tenant_id, 'workflow_id': workflow_id, 'version_id': version_id, 'parent_component_id': id_to_new_id_dict.get(component_info.get("id"))}
                        new_child_component_record = Component(**new_child_component_info)
                        new_child_component_record.save()
                        id_to_new_id_dict[child_info.get("id")] = new_child_component_record.id

            else:
                # if id is not startswith 'temp_', means existed in database need update
                if component_info.get("id") in exist_componet_dict.keys():
                    update_component_info = copy.deepcopy(component_info)
                    update_component_info.pop('id')
                    update_component_info.pop('children')
                    Component.objects.filter(id=component_info.get('id')).update(**update_component_info )
                    
                    # for children
                    for child_info in component_info.get("children"):
                        if child_info.get("id").startswith('temp_'):
                            # new child component
                            new_child_component_info = copy.deepcopy(child_info)
                            new_child_component_info.pop('id')
                            new_child_component_info = {**new_child_component_info, 'tenant_id': tenant_id, 'workflow_id': workflow_id, 'version_id': version_id, 'parent_component_id': id_to_new_id_dict.get(component_info.get("id"))}
                            new_child_component_record = Component(**new_child_component_info)
                            new_child_component_record.save()
                            id_to_new_id_dict[child_info.get("id")] = new_child_component_record.id
                        else:
                            # update existed child component
                            update_child_component_info = copy.deepcopy(child_info)
                            update_child_component_info.pop('id')
                            update_child_component_info = {**update_child_component_info, 'tenant_id': tenant_id, 'workflow_id': workflow_id, 'version_id': version_id, 'parent_component_id': id_to_new_id_dict.get(component_info.get("id"))}
                            Component.objects.filter(id=child_info.get('id')).update(**update_child_component_info)
                            id_to_new_id_dict[child_info.get("id")] = child_info.get("id")
                else:
                    raise('new component id shoud start with temp_')

        # todo: delete componet that not contain is new component list
        for component_id in exist_componet_dict:
            if component_id not in id_to_new_id_dict.values():
                archive_service_ins.archive_record('workflow_component', exist_componet_dict[component_id], operator_id)
        return id_to_new_id_dict

    @classmethod
    def add_workflow_components(cls, operator_id: str, tenant_id: str, workflow_id: str, version_id: str, component_info_list: list):
        """
        add workflow component, just or add new version worflow info
        :param tenant_id:
        :param workflow_id:
        :param component_info_list:
        :return:
        """
        # since new workflow may be created from old version, so we need to update all the id to new id
        id_to_new_id_dict = {}
        for component_info in component_info_list:
            new_component_info = {
                'tenant_id': tenant_id,
                'workflow_id': workflow_id,
                'version_id': version_id,
                'type': component_info.get("type"),
                'component_key': component_info.get("component_key"),
                'component_name': component_info.get("component_name"),
                'parent_component_id': component_info.get("parent_component_id"),
                'description': component_info.get("description", ""),
                'layout': component_info.get("layout", {}),
                'props': component_info.get("props", {}),
                'creator_id': operator_id
            }
            new_componet_record = Component(**new_component_info)
            new_componet_record.save()
            id_to_new_id_dict[component_info.get("id")] = new_componet_record.id

            for child_info in component_info.get("children"):
                new_child_component_info = {
                    'tenant_id': tenant_id,
                    'workflow_id': workflow_id,
                    'version_id': version_id,
                    'type': child_info.get("type"),
                    'component_key': child_info.get("component_key"),
                    'component_name': child_info.get("component_name"),
                    'parent_component_id': id_to_new_id_dict.get(component_info.get("id")),
                    'description': child_info.get("description", ""),
                    'layout': child_info.get("layout", {}),
                    'props': child_info.get("props"),
                    'creator_id': operator_id
                }
                new_child_component_record = Component(**new_child_component_info)
                new_child_component_record.save()
                id_to_new_id_dict[child_info.get("id")] = new_child_component_record.id
        return True


    @classmethod
    def get_workflow_fd_component_list(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        add workflow component
        :param tenant_id:
        :param workflow_id:
        :param component_info_list:
        :return:
        """
        component_queryset = Component.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        component_result_list = []
        for component_obj in component_queryset:
            if component_obj.type == 'row':
                # todo: get children
                children_source_list = [component_obj2 for component_obj2 in component_queryset if component_obj2.parent_component_id==component_obj.id]
                children_result_list = []
                for child_obj in children_source_list:
                    children_result_list.append(dict(
                        id=str(child_obj.id),
                        type=child_obj.type,
                        component_key=child_obj.component_key,
                        component_name=child_obj.component_name,
                        description=child_obj.description,
                        props=child_obj.props,
                        label=child_obj.label,
                        layout=child_obj.layout,
                    ))
                component_result = dict(
                    id=str(component_obj.id),
                    type=component_obj.type,
                    component_key=component_obj.component_key,
                    component_name=component_obj.component_name,
                    description=component_obj.description,
                    props=component_obj.props,
                    label=component_obj.label,
                    layout=component_obj.layout,
                    children=children_result_list
                )
                component_result_list.append(component_result)
                
        return component_result_list
    
    @classmethod
    def get_workflow_custom_fields(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow custom field
        :param workflow_id:
        :param tenant_id:
        :param version_id:
        :return:
        """
        component_queryset = Component.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        custom_field_list = []
        for component_obj in component_queryset:
            if component_obj.type != 'row':
                custom_field_list.append(component_obj.get_dict())
        return custom_field_list


workflow_component_service_ins = WorkflowComponentService()
