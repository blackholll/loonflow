import json
import time

from apps.loon_base_model import SnowflakeIDGenerator
from apps.workflow.models import Node
from service.base_service import BaseService


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
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            f_id = node_info.get("f_id")
            node_id = SnowflakeIDGenerator()()
            result_dict[f_id] = node_id
            node_field_dict = dict()
            node_field_info_list = node_info.get("node_field_info_list")
            for node_field_info in node_field_info_list:
                node_field_dict[node_field_info.get("field_key")] = node_field_info.get("field_attr")
            node_field_str = json.dumps(node_field_dict)

            node_create = Node(id=node_id, name=node_info.get("name"),
                               workflow_id=workflow_id,
                               tenant_id=tenant_id,
                               creator_id=operator_id,
                               type=node_info.get("type"),
                               allow_retreat=node_info.get("allow_retreat"),
                               remember_last_participant=node_info.get("remember_last_participant"),
                               participant_type=node_info.get("participant_type"),
                               participant=node_info.get("participant"),
                               distribute_type=node_info.get("distribute_type"),
                               node_field_str=node_field_str,
                               props=node_info.get("props")
                               )
            node_create_list.append(node_create)
        Node.objects.bulk_create(node_create_list)
        return result_dict

    @classmethod
    def get_init_node(cls, workflow_id: int) -> Node.objects:
        """
        get init node
        :param workflow_id:
        :return:
        """
        node_obj = Node.objects.get(workflow_id=workflow_id, type="start")
        result = dict(name=node_obj.name, type=node_obj.type, allow_retreat=node_obj.allow_retreat,
                      node_field_str=node_obj.node_field_str)
        return result


workflow_node_service_ins = WorkflowNodeService()
