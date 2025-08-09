import json
import time
import logging
from apps.workflow.models import Node
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException

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
    
    @classmethod
    def get_init_node_rest(cls, workflow_id: int) -> dict:
        """
        get init node, only include node info
        :param workflow_id:
        :return:
        """
        try:
            node_obj = Node.objects.get(workflow_id=workflow_id, type="start")
        except Node.DoesNotExist as e:
            logger.exception("init node is not exist: ")
            raise CustomCommonException("init node is not exist")
        result = node_obj.get_dict()
        node_field = result["node_field"]
        node_field_info_list = []
        for key, value in node_field.items():
            node_field_info_list.append(dict(field_key=key, field_value=value))
        need_key_list = ["id", "label", "tenant_id", "name", "type", "allow_retreat", "props"]
        new_result = {key: result[key] for key in result if key in need_key_list}
        new_result["node_field_info_list"] = node_field_info_list
        return new_result

    @classmethod
    def get_start_node_field_list(cls, workflow_id: int) ->tuple:
        """
        get start node field list
        :param workflow_id:
        :return: required field list and update_field_list
        """
        start_node = Node.objects.get(workflow_id=workflow_id, type="start")
        return cls.get_node_field_list(start_node)

    @classmethod
    def get_node_field_list(cls, node: Node.objects) -> tuple:
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
    def get_node_by_id(cls, node_id:int):
        return Node.objects.get(id=node_id)

    @classmethod
    def update_workflow_node(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, node_info_list: list):
        """
        update workflow node
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_info_list:
        :return:
        """
        node_id_dict = {}
        for node_info in node_info_list:
            if node_info.get("id").startswith('temp_'):
                # new node
                new_node_record= Node(
                    name=node_info.get("name"),
                    workflow_id=workflow_id,
                    tenant_id=tenant_id,
                    version_id=version_id,
                    creator_id=operator_id,
                    type=node_info.get("type"),
                    props=node_info.get("props", {}),
                    layout=node_info.get("layout", {}),
                    label=node_info.get("label", {})
                )
                new_node_record.save()
                node_id_dict[node_info.get("id")] = new_node_record.id
            else:
                # update existed node
                update_node_record = Node.objects.filter(id=node_info.get("id"), tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).update(
                    name=node_info.get("name"),
                    type=node_info.get("type"),
                    props=node_info.get("props", {}),
                    layout=node_info.get("layout", {}),
                    label=node_info.get("label", {}))

        return node_id_dict



workflow_node_service_ins = WorkflowNodeService()
