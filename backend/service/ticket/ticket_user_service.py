import time

from apps.ticket.models import User as TicketUser
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService


class TicketUserService(BaseService):
    """
    ticket user related service
    """
    @classmethod
    def add_record(cls, tenant_id: str, user_id: str, ticket_id: str, as_creator: bool, as_participant: bool,
                   as_processor: bool, as_cc_recipient: bool):
        ticket_user_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=user_id)
        update_dict = dict()
        if as_creator:
            update_dict["as_creator"] = True
        if as_participant:
            update_dict["as_participant"] = True
        if as_processor:
            update_dict["as_processor"] = True
        if as_cc_recipient:
            update_dict["as_participant"] = True

        if ticket_user_queryset:
            ticket_user_queryset.update(**update_dict)
        else:
            ticket_user = TicketUser( tenant_id=tenant_id, ticket_id=ticket_id, user_id=user_id)
            ticket_user.save()
            TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=user_id).update(**update_dict)

    @classmethod
    def update_ticket_user_by_all_next_node_result(cls, tenant_id:str, ticket_id:str, operator_id:str, cc_to_user_id_list:list, next_ticket_node_result_list:list):
        """
        update ticket user
        :param tenant_id:
        :param ticket_id:
        :param operator_id:
        :param cc_to_user_id_list:
        :param next_ticket_node_result_list:
        :return:
        """
        # add or update operator as_processor. ticket creator aslo consider as processor
        
        ticket_user_exist_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=operator_id)
        ticket_user_exist_user_id_list = [ticket_user.user_id for ticket_user in ticket_user_exist_queryset]
        if ticket_user_exist_queryset:
            ## update record if user already exit
            ticket_user_exist_queryset.update(as_processor=True)
        else:
            ## add record if not exist
            TicketUser.objects.create(tenant_id=tenant_id, ticket_id=ticket_id, user_id=operator_id, as_processor=True)
            ticket_user_exist_user_id_list.append(operator_id)
        # add cc_recipient
        for cc_to_user_id in cc_to_user_id_list:
            ticket_cc_recipient_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=cc_to_user_id)
            if not ticket_cc_recipient_queryset:
                TicketUser.objects.create(tenant_id=tenant_id, ticket_id=ticket_id, user_id=cc_to_user_id, as_cc_recipient=True)
                ticket_user_exist_user_id_list.append(cc_to_user_id)
            else:
                ticket_cc_recipient_queryset.update(as_cc_recipient=True)
        
        # add or update assignee
        assigness_list = []
        ## update or add assignee, need consider user that assigned to multi-nodes, need set other user as_assignee=False
        exist_user_id_list = list(TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).values_list('user_id', flat=True))
        exist_user_id_str_list = [str(user_id) for user_id in exist_user_id_list]

        user_assignee_node_ids_dict = dict()
        
        for next_ticket_node_result in next_ticket_node_result_list:
            for target_assignee in next_ticket_node_result.get("target_assignee_list"):
                source_target_assignee_list = user_assignee_node_ids_dict.get(target_assignee, [])
                source_target_assignee_list.append(str(next_ticket_node_result.get("node_id")))
                user_assignee_node_ids_dict[target_assignee] = source_target_assignee_list


        for key, value in user_assignee_node_ids_dict.items():
            if key in exist_user_id_str_list:
                TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=key).update(as_assignee=True, assignee_node_ids= ','.join(value))
            else:
                TicketUser.objects.create(tenant_id=tenant_id, ticket_id=ticket_id, user_id=key, as_assignee=True, assignee_node_ids=','.join(value))
            
        

    @classmethod
    def get_ticket_current_assignee_info(cls, tenant_id: str, ticket_id: str)->dict:
        """
        get ticket current assignee id list
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        ticket_participant_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, as_assignee=True)
        result_dict = dict()
        for ticket_participant in ticket_participant_queryset:
            result_dict[str(ticket_participant.user_id)] = ticket_participant.assignee_node_ids
        return result_dict
    
    @classmethod
    def get_ticket_relation_user_id_list(cls, tenant_id: str, ticket_id: str)->list:
        """
        get ticket relation user id list
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        ticket_user_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id)
        return [ticket_user.user_id for ticket_user in ticket_user_queryset]


ticket_user_service_ins = TicketUserService()

