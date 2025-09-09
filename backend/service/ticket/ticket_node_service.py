import time

from apps.ticket.models import Node as TicketNode
from service.base_service import BaseService
from service.util.archive_service import archive_service_ins


class TicketNodeService(BaseService):
    @classmethod
    def update_batch_record(cls, tenant_id: int, ticket_node_participant_obj_list: list) -> bool:
        """
        update btch ticket record
        :param tenant_id:
        :param ticket_node_participant_obj_list:
        :return:
        """
        ticket_node_bulk_list = []
        ticket_node_participant_bulk_list = []
        for ticket_node_participant_obj in ticket_node_participant_obj_list:
            ticket_node_bulk = TicketNode(tenant_id=tenant_id,
                                          ticket_id=ticket_node_participant_obj.get("ticket_id"),
                                          node_id=ticket_node_participant_obj.get("node_id"),
                                          in_add_node=ticket_node_participant_obj.get("in_add_node"),
                                          add_node_target=ticket_node_participant_obj.get("add_node_target"),
                                          hook_state=ticket_node_participant_obj.get("hook_state"),
                                          all_participant_result=ticket_node_participant_obj.get("all_participant_result"))
            ticket_node_bulk_list.append(ticket_node_bulk)

            if ticket_node_participant_obj.get("destination_participant_type") in ("multi-person", "person"):
                real_destination_participant_type = "person"
            else:
                real_destination_participant_type = ticket_node_participant_obj.get("destination_participant_type")
            for destination_participant in ticket_node_participant_obj.get("destination_participant_list"):
                ticket_node_participant_bulk = TicketNodeParticipant(tenant_id=tenant_id,
                                                                     ticket_id=ticket_node_participant_obj.get("ticket_id"),
                                                                     node_id=ticket_node_participant_obj.get("node_id"),
                                                                     participant_type=real_destination_participant_type,
                                                                     participant=destination_participant
                                                                     )
                ticket_node_participant_bulk_list.append(ticket_node_participant_bulk)

        # del and add new record
        node_id_list = [ticket_node_participant_obj.get("id") for ticket_node_participant_obj in ticket_node_participant_obj_list]

        for_archive_ticket_node_queryset = TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_node_participant_obj_list[0].get("ticket_id"), node_id__in=node_id_list)
        for_archive_ticket_node_participant_queryset = TicketNodeParticipant.objects.filter(tenant_id=tenant_id,
                                                                                            ticket_id=ticket_node_participant_obj_list[0].get("ticket_id"), node_id__in=node_id_list)

        archive_service_ins.archive_record_list("TicketNode", for_archive_ticket_node_queryset, 0)
        archive_service_ins.archive_record_list("TicketNodeParticipant", for_archive_ticket_node_participant_queryset, 0)
        TicketNode.objects.bulk_create(ticket_node_bulk_list)
        TicketNodeParticipant.objects.bulk_create(ticket_node_participant_bulk_list)
        return True

    @classmethod
    def update_ticket_node_record(cls, tenant_id:str, node_info_list:list) -> bool:
        """
        update ticket node record
        :param tenant_id:
        :param node_info_list:
        :return:
        """
        # todo: 1. 其他node的is_active 设置false, 2. for update node record
        node_id_list = [node_info.get("node_id") for node_info in node_info_list]
        node_info_dict = dict()
        for node_info in node_info_list:
            node_info_dict[node_info.get("node_id")] = node_info
        
        need_add_node_list, need_update_node_list, need_delete_node_list = [], [], []
    
        if node_info_list:
            exist_ticket_node_queryset = TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=node_info_list[0].get("ticket_id"))
        
        # get need add records, geet need update records, get need delete records
        ## get need add records
        for node_info in node_info_list:
            if node_info.get("node_id") not in exist_ticket_node_queryset.values_list("node_id", flat=True):
                need_add_node_list.append(node_info)

        ## get need update records
        for node_info in node_info_list:
            if node_info.get("node_id") in exist_ticket_node_queryset.values_list("node_id", flat=True):
                need_update_node_list.append(node_info)

        ## get need delete records
        for node_info in exist_ticket_node_queryset:
            if node_info.get("node_id") not in node_id_list:
                need_delete_node_list.append(node_info)
        
        ## delete records
        for_archive_ticket_node_queryset = TicketNode.objects.filter(
            tenant_id=tenant_id, 
            id__in=[node_info.id for node_info in need_delete_node_list]
        )
        archive_service_ins.archive_record_list("TicketNode", for_archive_ticket_node_queryset, '')

        ## add records
        need_add_bulk_list = []
        for new_node_info in need_add_node_list:
            need_add_bulk_list.append(TicketNode(
                tenant_id=tenant_id,
                ticket_id=node_info.get("ticket_id"),
                node_id=node_info.get("node_id"),
                in_add_node = new_node_info.get("in_add_node"),
                add_node_target = new_node_info.get("add_node_target"),
                is_active = new_node_info.get("is_active"),
                hook_state = new_node_info.get("hook_state"),
                all_assignee_result = new_node_info.get("all_assignee_result"),
                assignee_type = new_node_info.get("target_assignee_type"),
                assignee = new_node_info.get("target_assignee_list"),
                in_parallel = new_node_info.get("in_parallel", False)
            ))
        TicketNode.objects.bulk_create(need_add_bulk_list)
        
        ## update records
        for need_update_node in need_update_node_list:
            TicketNode.objects.filter(id=need_update_node.id).update(
                in_add_node = need_update_node.get("in_add_node"),
                add_node_target = need_update_node.get("add_node_target"),
                is_active = need_update_node.get("is_active"),
                hook_state = need_update_node.get("hook_state"),
                all_assignee_result = need_update_node.get("all_assignee_result"),
                assignee_type = need_update_node.get("assignee_type"),
                assignee = need_update_node.get("assignee"),
                in_paraller = need_update_node.get("in_paraller")
            )

    @classmethod
    def get_ticket_current_nodes(cls, tenant_id: str, ticket_id: str) -> list:
        """
        get ticket current nodes
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        ticket_node_queryset = TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, is_active=True)
        return list(ticket_node_queryset)

ticket_node_service_ins = TicketNodeService()
