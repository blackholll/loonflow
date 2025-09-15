import time
from apps.ticket.models import Node as TicketNode
from service.workflow import workflow_node_service
from service.exception.custom_common_exception import CustomCommonException
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
    def update_ticket_node_record(cls, tenant_id:str, operator_id:str, node_info_list:list) -> bool:
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
            if node_info.node_id not in node_id_list:
                need_delete_node_list.append(node_info)
        
        ## delete records
        for_archive_ticket_node_queryset = TicketNode.objects.filter(
            tenant_id=tenant_id, 
            id__in=[node_info.id for node_info in need_delete_node_list]
        )
        archive_service_ins.archive_record_list("TicketNode", for_archive_ticket_node_queryset, operator_id)

        ## add records
        need_add_bulk_list = []
        for new_node_info in need_add_node_list:
            need_add_bulk_list.append(TicketNode(
                tenant_id=tenant_id,
                ticket_id=new_node_info.get("ticket_id"),
                node_id=new_node_info.get("node_id"),
                in_consult = new_node_info.get("in_consult", False),
                consult_from_id = new_node_info.get("operator_id"),
                consult_target_id = new_node_info.get("consultant_id"),
                is_active = new_node_info.get("is_active"),
                hook_state = new_node_info.get("hook_state"),
                all_assignee_result = new_node_info.get("all_assignee_result"),
                assignee_type = new_node_info.get("target_assignee_type"),
                assignee = ','.join(new_node_info.get("target_assignee_list",[])),
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

    @classmethod
    def replace_node_assignee(cls, tenant_id: str, ticket_id: str, node_id: str, source_assignee_id: str, target_assignee_id: str) -> bool:
        """
        replace node assignee, source_assignee may be empty
        :param tenant_id:
        :param ticket_id:
        :param node_id:
        :param source_assignee_id:
        :param target_assignee_id:
        :return:
        """
        # todo: 考虑source_assignee_id为空的情况
        try:
            exist_ticket_node_record = TicketNode.objects.get(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id)
        except TicketNode.DoesNotExist:
            raise CustomCommonException("Node not found")
        
        if exist_ticket_node_record.assignee_type == "user":
            exist_assignee_list = exist_ticket_node_record.assignee.split(',')
            if source_assignee_id:
                if source_assignee_id in exist_assignee_list:
                    new_assignee_list = [target_assignee_id if user_id == source_assignee_id else user_id for user_id in exist_assignee_list]
                    new_assignee = ",".join(new_assignee_list)
                    currnet_all_assignee_result = exist_ticket_node_record.all_assignee_result
                    if currnet_all_assignee_result:
                        value = currnet_all_assignee_result.get(source_assignee_id)
                        currnet_all_assignee_result.pop(source_assignee_id)
                        currnet_all_assignee_result[target_assignee_id] = value
                else:
                    raise CustomCommonException("Source assignee not found")
                
            else:
                # all assignee replace
                new_assignee = target_assignee_id
                currnet_all_assignee_result = exist_ticket_node_record.all_assignee_result
                if currnet_all_assignee_result:
                    for key, value in currnet_all_assignee_result.items():
                        if not value:
                            value = currnet_all_assignee_result.get(key)
                            currnet_all_assignee_result.pop(key)
                currnet_all_assignee_result[target_assignee_id] = value
                exist_ticket_node_record.all_assignee_result = currnet_all_assignee_result
            
            TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id).update(assignee=new_assignee, all_assignee_result=currnet_all_assignee_result)
        else:
            raise CustomCommonException("This ticket does not support replace assignee")
        
        return True

    @classmethod
    def update_ticket_node_consult_record(cls, tenant_id: str, ticket_id:str, node_id:str, operator_id:str, consultant_id:str) -> bool:
        """
        update ticket node consult record
        :param tenant_id:
        :param ticket_id:
        :param node_id:
        :param operator_id:
        :param consultant_id:
        :return:
        """
        TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id).update(in_consult=True, consult_from_id=operator_id, 
        consult_target_id=consultant_id, assignee=consultant_id, assignee_type='user')
        return True


    @classmethod
    def update_ticket_node_consult_submit(cls, tenant_id:str, ticket_id:str, node_id:str) -> bool:
        """
        update ticket node consult submit record
        :param tenant_id:
        :param ticket_id:
        :param node_id:
        :param operator_id:
        :param consultant_id:
        :return:
        """
        ticket_record = TicketNode.objects.get(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id)
        consult_from = ticket_record.consult_from
        all_assignee_result = ticket_record.all_assignee_result
        next_assignee_list = []
    

        if all_assignee_result:
            for key, value in all_assignee_result.items():
                if not value:
                    next_assignee_list.append(key)
        else:
            next_assignee_list = [consult_from]
        TicketNode.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id).update(in_consult=False, consult_from=None, 
        consult_target=None, assignee=','.join(next_assignee_list), assignee_type='users')
        return True

    def update_ticket_node_accept(cls, tenant_id: str, ticket_id: str, node_id: str, operator_id: str) -> bool:
        """
        update ticket node accept record
        :param tenant_id:
        :param ticket_id:
        :param node_id:
        :param operator_id:
        :return:
        """
        ticket_node_record = TicketNode.objects.get(tenant_id=tenant_id, ticket_id=ticket_id, node_id=node_id)
        if not ticket_node_record.in_accept_wait:
            raise CustomCommonException("Node is not in accept wait status")
        ticket_node_record.in_accept_wait = False
        ticket_node_record.assignee = operator_id
        ticket_node_record.assignee_type = 'users'
        ticket_node_record.save()
        return True


ticket_node_service_ins = TicketNodeService()
