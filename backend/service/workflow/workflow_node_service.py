import json
import time
import logging
from apps.workflow.models import Node
from service.workflow.workflow_edge_service import workflow_edge_service_ins
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
    def get_node_by_id(cls, tenant_id: str, node_id: str) -> dict:
        """
        get node by id
        :param tenant_id:
        :param node_id:
        :return:
        """
        print("node_id", node_id)
        print("tenant_id", tenant_id)
        node_obj = Node.objects.get(id=node_id, tenant_id=tenant_id)
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
            if str(node_obj.id) not in exist_node_id_list:
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
                node_id_dict[node_info.get("id")] = node_info.get("id")
        return node_id_dict

    def get_parallel_merge_node(cls, tenant_id: str, workflow_id: str, version_id: str, node_id: str) -> dict:
        """
        get parallel merge node
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param node_id:
        :return:
        """
        # 获取并行节点后每条edge的目标节点， 然后每个节点继续根据出边获取目标节点。
        # 当开始的所有edge可达的共同节点存在且相同时，那么这个节点即为汇聚节点。
        # 实现：对每个分支做BFS，求可达节点集合的交集；选择距离各分支最小的共同节点。

        # 获取并行网关的直接后继分支起点
        branch_start_node_id_list = workflow_edge_service_ins.get_parallel_next_node_list(
            tenant_id, workflow_id, version_id, node_id
        )

        if not branch_start_node_id_list or len(branch_start_node_id_list) < 2:
            raise CustomCommonException('parallel node must have at least two outgoing edges')

        # 对每个分支起点进行BFS，记录最短距离
        def bfs_collect_distance(start_node_id: int) -> dict:
            from collections import deque
            visited = set()
            distance = {}
            queue = deque()
            queue.append((start_node_id, 0))
            visited.add(start_node_id)
            distance[start_node_id] = 0

            # 设置一个合理上限避免意外循环
            step_guard = 0
            max_steps = 10000

            while queue:
                current_node_id, current_dist = queue.popleft()
                # 获取后继
                next_node_id_list = workflow_edge_service_ins.get_parallel_next_node_list(
                    tenant_id, workflow_id, version_id, current_node_id
                )
                for next_node_id in next_node_id_list:
                    if next_node_id not in visited:
                        visited.add(next_node_id)
                        distance[next_node_id] = current_dist + 1
                        queue.append((next_node_id, current_dist + 1))

                step_guard += 1
                if step_guard > max_steps:
                    raise CustomCommonException('graph traversal exceeded step guard, please check for cycles')

            return distance

        branch_dist_list = [bfs_collect_distance(start_id) for start_id in branch_start_node_id_list]

        # 计算共同可达节点
        common_nodes = None
        for dist_map in branch_dist_list:
            keys = set(dist_map.keys())
            if common_nodes is None:
                common_nodes = keys
            else:
                common_nodes &= keys

        if not common_nodes:
            raise CustomCommonException('parallel merge node not found')

        # 选择一个“最近的”共同节点：使各分支到它的最大距离最小，再按总和距离最小
        def score_node(nid: int):
            distances = [dm.get(nid, float('inf')) for dm in branch_dist_list]
            return (max(distances), sum(distances))

        merge_node_id = min(common_nodes, key=score_node)

        # 返回节点对象
        merge_node_obj = Node.objects.get(id=merge_node_id, tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        return merge_node_obj



workflow_node_service_ins = WorkflowNodeService()
    