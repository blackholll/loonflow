import json
import time
import logging
from apps.workflow.models import Node
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins

logger = logging.getLogger("django")


class WorkflowNodeService(BaseService):
    @classmethod
    def add_workflow_node(cls, operator_id: str, tenant_id: str, workflow_id: str, version_id: str, node_info_list: list) -> dict:
        """
        add workflow node
        :param operator_id:
        :param tenant_id:
        :param workflow_id:
        :param node_info_list:
        :return:
        """
        # since we need get each record's id,  have to insert record one by one
        node_id_dict = {}
        for node_info in node_info_list:
            new_node_info = {
                'name': node_info.get("name"),
                'workflow_id': workflow_id,
                'tenant_id': tenant_id,
                'version_id': version_id,
                'creator_id': operator_id,
                'type': node_info.get("type"),
                'props': node_info.get("props", {}),
                'layout': node_info.get("layout", {}),
                'label': node_info.get("label", {})
            }
            new_node_record = Node(**new_node_info)
            new_node_record.save()
            new_node_id = new_node_record.id
            node_id_dict[node_info.get("id")] = new_node_id
        return node_id_dict

    @classmethod
    def get_node_field_permissions(cls, tenant_id: str, workflow_id: str, version_id: str, node_id: str) -> dict:
        """
        get init node field permissions
        :param workflow_id:
        :param version_id:
        :param node_id:
        :return:
        """
        node_obj = Node.objects.get(id=node_id, tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        node_permissions = node_obj.props.get('field_permissions', {})
        return node_permissions

    @classmethod
    def get_workflow_fd_node_list(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow node list
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        node_queryset = Node.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        node_result_list = []
        for node_obj in node_queryset:
            node_result_list.append(
                dict(
                    id=str(node_obj.id),
                    name=node_obj.name,
                    type=node_obj.type,
                    props=node_obj.props,
                    layout=node_obj.layout,
                    label=node_obj.label,
                )
            )
        return node_result_list
    
    
    

        """
        get node's required field list and update field list
        :param node:
        :return:
        """
        node_field = node.node_field
        require_field_list, update_field_list= [], []
        # required, optional, readonly
        for key, value in node_field.items():
            if value == "rwm":
                require_field_list.append(key)
                update_field_list.append(key)
            elif value == "rwo":
                update_field_list.append(key)
        return require_field_list, update_field_list

    @classmethod
    def get_init_node_field_permissions(cls, tenant_id: str, workflow_id: str, version_id: str) -> list:
        """
        get init node field permissions
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        init_node = Node.objects.get(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, type='start')
        return cls.get_node_field_permissions(tenant_id, workflow_id, version_id, init_node.id) 
    
    @classmethod
    def get_init_node(cls, tenant_id: str, workflow_id: str, version_id: str) -> dict:
        """
        get init node rest
        :param workflow_id:
        :return:
        """
        init_node = Node.objects.get(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, type='start')
        return init_node
    
    @classmethod
    def get_end_node(cls, tenant_id: str, workflow_id: str, version_id: str) -> dict:
        """
        get end node
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        end_node = Node.objects.get(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, type='end')
        return end_node
    
    @classmethod
    def get_node_by_id(cls, tenant_id: str, workflow_id: str, version_id: str, node_id: str) -> dict:
        """
        get node by id
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_id:
        :return:
        """
        node_obj = Node.objects.get(id=node_id, tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        return node_obj

    @classmethod
    def get_node_queryset_by_id_list(cls, tenant_id: str, workflow_id: str, version_id: str, node_id_list: list) -> list:
        """
        get node queryset by id list
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_id_list:
        :return:
        """
        node_queryset = Node.objects.filter(id__in=node_id_list, tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        return node_queryset
    @classmethod
    def update_workflow_node(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, node_info_list: list) -> dict:
        """
        update workflow node, need delete removed node
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param node_info_list:
        :return:
        """
        node_id_dict = {}
        exist_node_id_list = [node_info.get("id") for node_info in node_info_list]
        exist_node_queryset = Node.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        for node_obj in exist_node_queryset:
            if node_obj.id not in exist_node_id_list:
                archive_service_ins.archive_record('workflow_node', node_obj, operator_id)
        
        for node_info in node_info_list:
            if node_info.get("id").startswith('temp_'):
                new_node_info = {
                'name': node_info.get("name"),
                'workflow_id': workflow_id,
                'tenant_id': tenant_id,
                'version_id': version_id,
                'creator_id': operator_id,
                'type': node_info.get("type"),
                'props': node_info.get("props", {}),
                'layout': node_info.get("layout", {}),
                'label': node_info.get("label", {})
            }
                new_node_record = Node(**new_node_info)
                new_node_record.save()
                node_id_dict[node_info.get("id")] = new_node_record.id
            else:
                # update exist node
                Node.objects.filter(id=node_info.get("id")).update(
                    name=node_info.get("name"),
                    type=node_info.get("type"),
                    props=node_info.get("props", {}),
                    layout=node_info.get("layout", {}),
                    label=node_info.get("label", {})
                )
        return node_id_dict
                



workflow_node_service_ins = WorkflowNodeService()
    