import json
import time
import logging
from apps.workflow.models import Node
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException

logger = logging.getLogger("django")


class WorkflowNodeService(BaseService):
    @classmethod
    def add_workflow_node(cls, operator_id: int, tenant_id: int, workflow_id: int, node_info_list: list) -> dict:
        """
        add workflow node
        :param operator_id:
        :param tenant_id:
        :param workflow_id:
        :param node_info_list:
        :return:
        """
        node_create_list = []
        result_dict = dict()
        for node_info in node_info_list:
            f_id = node_info.get("f_id")
            node_field_dict = dict()
            node_field_info_list = node_info.get("node_field_info_list")
            for node_field_info in node_field_info_list:
                node_field_dict[node_field_info.get("field_key")] = node_field_info.get("field_attr")

            node_create = Node(name=node_info.get("name"),
                               workflow_id=workflow_id,
                               tenant_id=tenant_id,
                               creator_id=operator_id,
                               type=node_info.get("type"),
                               allow_retreat=node_info.get("allow_retreat"),
                               remember_last_participant=node_info.get("remember_last_participant"),
                               participant_type=node_info.get("participant_type"),
                               participant=node_info.get("participant"),
                               distribute_type=node_info.get("distribute_type"),
                               node_field=node_field_dict,
                               props=node_info.get("props")
                               )
            node_create_list.append(node_create)
        Node.objects.bulk_create(node_create_list)
        return result_dict

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


workflow_node_service_ins = WorkflowNodeService()
