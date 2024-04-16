import time

from apps.loon_base_model import SnowflakeIDGenerator
from apps.ticket.models import TicketNode, TicketNodeParticipant
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
            ticket_node_id = SnowflakeIDGenerator()()
            ticket_node_bulk = TicketNode(id=ticket_node_id, tenant_id=tenant_id,
                                          ticket_id=ticket_node_participant_obj.get("ticket_id"),
                                          node_id=ticket_node_participant_obj.get("node_id"),
                                          in_add_node=ticket_node_participant_obj.get("in_add_node"),
                                          add_node_target=ticket_node_participant_obj.get("add_node_target"),
                                          hook_state=ticket_node_participant_obj.get("hook_state"),
                                          all_participant_result=ticket_node_participant_obj.get("all_participant_result"))
            ticket_node_bulk_list.append(ticket_node_bulk)
            time.sleep(0.001)  # SnowflakeIDGenerator has bug will, just workaround provisionally

            if ticket_node_participant_obj.get("destination_participant_type") in ("multi-person", "person"):
                real_destination_participant_type = "person"
            else:
                real_destination_participant_type = ticket_node_participant_obj.get("destination_participant_type")
            for destination_participant in ticket_node_participant_obj.get("destination_participant_list"):
                ticket_node_participant_bulk = TicketNodeParticipant(id=SnowflakeIDGenerator()(), tenant_id=tenant_id,
                                                                     ticket_id=ticket_node_participant_obj.get("ticket_id"),
                                                                     node_id=ticket_node_participant_obj.get("node_id"),
                                                                     participant_type=real_destination_participant_type,
                                                                     participant=destination_participant
                                                                     )
                time.sleep(0.001)  # SnowflakeIDGenerator has bug, just workaround provisionally
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

ticket_node_service_ins = TicketNodeService()
