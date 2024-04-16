import time

from apps.loon_base_model import SnowflakeIDGenerator
from apps.ticket.models import TicketUser
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService


class TicketUserService(BaseService):
    """
    ticket user related service
    """
    @classmethod
    def add_record(cls, tenant_id: int, user_id: int, ticket_id: int, as_creator: bool, as_participant: bool,
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
            ticket_user = TicketUser(id=SnowflakeIDGenerator()(),  tenant_id=tenant_id, ticket_id=ticket_id, user_id=user_id)
            ticket_user.save()
            TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id=user_id).update(**update_dict)

    @classmethod
    def add_participant_record_list(cls, tenant_id: int, ticket_id: int, user_id_list: list) -> bool:
        """
        add participant record list
        :param tenant_id:
        :param ticket_id:
        :param user_id_list:
        :return:
        """
        exist_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, user_id__in=user_id_list)
        exist_queryset.update(as_participant=True)
        exist_user_id_list = [exist_record.user_id for exist_record in exist_queryset]
        not_exist_user_id_list = [user_id for user_id in user_id_list if user_id not in exist_user_id_list]
        ticket_user_batch_list = []
        for not_exist_user_id in not_exist_user_id_list:
            ticket_user_batch_list.append(TicketUser(id=SnowflakeIDGenerator()(), tenant_id=tenant_id, ticket_id=ticket_id, user_id=not_exist_user_id, as_participant=True))
            time.sleep(0.001)  # workaround for SnowflakeIDGenerator
        TicketUser.objects.bulk_create(ticket_user_batch_list)

    @classmethod
    def get_ticket_current_participant_list(cls, tenant_id: int, ticket_id: int):
        """
        get ticket current participant list
        :param tenant_id:
        :param ticket_id:
        :return:
        """
        ticket_participant_queryset = TicketUser.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id, as_participant=True)
        ticket_participant_id_list = [ticket_participant.user_id for ticket_participant in ticket_participant_queryset]
        return account_user_service_ins.get_user_list_by_id_list(tenant_id, ticket_participant_id_list)


ticket_user_service_ins = TicketUserService()
