import datetime
from datetime import date, time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.ticket.models import FlowHistory
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService
from service.workflow.workflow_edge_service import workflow_edge_service_ins


class TicketFlowHistoryService(BaseService):
    """
    ticket flow history related service
    """
    @classmethod
    def add_ticket_flow_history(cls, tenant_id: str, operator_id: str, ticket_id: str, action_type: str, action_id: str, comment: str,
                                processor_type: str, processor: str, node_id: str,  ticket_data: dict) -> int:
        # todo: ticket_data serialize
        finally_ticket_data = dict()
        for key, value in ticket_data.items():
            if isinstance(value, datetime.datetime):
                finally_ticket_data[key] = value.strftime('%Y-%m-%d %H:%M:%S %z')
            elif isinstance(value, date):
                finally_ticket_data[key] = value.strftime('%Y-%m-%d')
            elif isinstance(value, time):
                finally_ticket_data[key] = value.strftime('%H:%M:%S')
            else:
                finally_ticket_data[key] = value

        record = FlowHistory(tenant_id=tenant_id, creator_id=operator_id, ticket_id=ticket_id, action_type=action_type,
                                   action_id=action_id, comment=comment, processor_type=processor_type,
                                   processor=processor, node_id=node_id, ticket_data=finally_ticket_data)
        record.save()
        return record.id

    @classmethod
    def get_ticket_flow_history(cls, tenant_id: int, ticket_id: int, per_page: int=10, page: int=1, include_ticket_data: int=0, desc: int=1) -> dict:
        """
        get ticket flow history
        :param tenant_id:
        :param ticket_id:
        :param per_page:
        :param page:
        :param include_ticket_data:
        :param desc:
        :return:
        """
        if desc == 0:
            ticket_flow_history_queryset = TicketFlowHistory.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).order_by("id")
        else:
            ticket_flow_history_queryset = TicketFlowHistory.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).order_by("-id")
        paginator = Paginator(ticket_flow_history_queryset, per_page)

        try:
            ticket_history_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_history_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            ticket_history_result_paginator = paginator.page(paginator.num_pages)
        ticket_flow_history_object_format_list = []
        for ticket_flow_history in ticket_flow_history_queryset:
            node_info = dict(id=ticket_flow_history.node.id, name=ticket_flow_history.node.name)
            transition_id = ticket_flow_history.transition_id
            transition_info_dict = dict(id=transition_id)
            flow_type = ticket_flow_history.flow_type
            if transition_id == 0:
                transition_name = flow_type
            else:
                transition_obj = workflow_transition_service_ins.get_workflow_transition_by_id(transition_id)
                transition_name = transition_obj.name
            transition_info_dict["name"] = transition_name
            participant_info = dict(participant_type=ticket_flow_history.participant_type,
                                    participant=ticket_flow_history.participant,
                                    participant_alias=ticket_flow_history.participant,
                                    participant_email='', participant_phone=''
                                    )
            if ticket_flow_history.participant_type == "personal":
                user_info = account_user_service_ins.get_user_by_user_id(ticket_flow_history.participant)
                participant_info.update(participant_alias=user_info.alias, participant_email=user_info.email,
                                        participant_phone=user_info.phone)
            ticket_flow_history_restful = dict(id=ticket_flow_history.id, ticket_id=ticket_id,
                                               node_info=node_info, participant_info=participant_info,
                                               comment=ticket_flow_history.comment,
                                               create_at=ticket_flow_history.created_at.strftime('%Y-%m-%d %H:%M:%S %z'))
            if include_ticket_data:
                ticket_flow_history_restful.update(ticket_data=ticket_flow_history.ticket_data)
            ticket_flow_history_object_format_list.append(ticket_flow_history_restful)

            return dict(ticket_flow_history_object_format_list=ticket_flow_history_object_format_list,
                        paginator_info=dict(per_page=per_page, page=page, total=paginator.count))













ticket_flow_history_service_ins = TicketFlowHistoryService()
