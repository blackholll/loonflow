from service.base_service import BaseService
from apps.workflow.models import Edge
from service.util.archive_service import archive_service_ins


class WorkflowEdgeService(BaseService):
    @classmethod
    def add_workflow_edges(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, edge_info_list: list):
        """
        add workflow edges
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param edge_info_list:
        :return:
        """
        need_insert_edge_record = []
        for edge_info in edge_info_list:
            need_insert_edge_record.append(Edge(
                tenant_id=tenant_id,
                workflow_id=workflow_id,
                version_id=version_id,
                source_node_id=edge_info.get("source_node_id"),
                target_node_id=edge_info.get("target_node_id"),
                type=edge_info.get("type"),
                name=edge_info.get("name"),
                label=edge_info.get("label", {}),
                layout=edge_info.get("layout", {}),
                props=edge_info.get("props", {}),
                creator_id = operator_id
            ))
        Edge.objects.bulk_create(need_insert_edge_record)
        return True

    @classmethod
    def update_workflow_edges(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, edge_info_list: list):
        """
        update workflow edges, need delete removed edge
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param edge_info_list:
        :return:
        """
        exist_edge_id_list = [edge_info.get("id") for edge_info in edge_info_list]
        exist_edge_queryset = Edge.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        for edge_obj in exist_edge_queryset:
            if edge_obj.id not in exist_edge_id_list:
                archive_service_ins.archive_record('workflow_edge', edge_obj, operator_id)


        for edge_info in edge_info_list:
            if edge_info.get("id").startswith('temp_'):
                # new edge
                new_edge_record = Edge(
                    tenant_id=tenant_id,
                    workflow_id=workflow_id,
                    version_id=version_id,
                    source_node_id=edge_info.get("source_node_id"),
                    target_node_id=edge_info.get("target_node_id"),
                    type=edge_info.get("type"),
                    name=edge_info.get("name"),
                    label=edge_info.get("label"),
                    props=edge_info.get("props"),
                    creator_id=operator_id
                )
                new_edge_record.save()
            else:
                # update existed edge
                Edge.objects.filter(id=edge_info.get("id"), tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).update(
                    source_node_id=edge_info.get("source_node_id"),
                    target_node_id=edge_info.get("target_node_id"),
                    type=edge_info.get("type"),
                    name=edge_info.get("name"),
                    label=edge_info.get("label"),
                    props=edge_info.get("props"),
                    updater_id=operator_id
                )
        return True

    @classmethod
    def get_workflow_fd_edge_list(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow full definition edge list
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        edge_queryset = Edge.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id)
        edge_result_list = []
        for edge_obj in edge_queryset:
            edge_result_list.append(
                dict(
                    id=str(edge_obj.id),
                    name=edge_obj.name,
                    type=edge_obj.type,
                    props=edge_obj.props,
                    label=edge_obj.label,
                    layout=edge_obj.layout,
                    source_node_id=str(edge_obj.source_node_id),
                    target_node_id=str(edge_obj.target_node_id),
                )
            )
        return edge_result_list
    

workflow_edge_service_ins = WorkflowEdgeService()
