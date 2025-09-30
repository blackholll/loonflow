import datetime
import json
import decimal
from datetime import date, time
from django.core.serializers.json import DjangoJSONEncoder
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
            elif isinstance(value, decimal.Decimal):
                finally_ticket_data[key] = json.dumps(value, cls=DjangoJSONEncoder)
            else:
                finally_ticket_data[key] = value

        record = FlowHistory(tenant_id=tenant_id, creator_id=operator_id, ticket_id=ticket_id, action_type=action_type,
                                   action_id=action_id, comment=comment, processor_type=processor_type,
                                   processor=processor, node_id=node_id, ticket_data=finally_ticket_data)
        record.save()
        return record.id

    @classmethod
    def get_ticket_flow_history(cls, tenant_id: str, ticket_id: str, per_page: int=10, page: int=1, include_ticket_data: int=0, desc: int=1) -> dict:
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
            ticket_flow_history_queryset = FlowHistory.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).select_related('node', 'action').order_by("created_at")
        else:
            ticket_flow_history_queryset = FlowHistory.objects.filter(tenant_id=tenant_id, ticket_id=ticket_id).select_related('node', 'action').order_by("-created_at")
        paginator = Paginator(ticket_flow_history_queryset, per_page)

        try:
            ticket_history_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_history_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            ticket_history_result_paginator = paginator.page(paginator.num_pages)
        ticket_flow_history_object_format_list = []
        for ticket_flow_history in ticket_history_result_paginator:
            node_info = dict(id=str(ticket_flow_history.node.id), name=ticket_flow_history.node.name)
            action_name= ''
            if ticket_flow_history.action:
                action_name = ticket_flow_history.action.name


            processor_info = dict(processor_type=ticket_flow_history.processor_type,
                                    processor=ticket_flow_history.processor,
                                    processor_alias='',
                                    processor_email='',
                                    processor_phone=''
                                    )

            if ticket_flow_history.processor_type == "user":
                user_info = account_user_service_ins.get_user_by_user_id(tenant_id, ticket_flow_history.processor)
                processor_info.update(processor_alias=user_info.alias, processor_email=user_info.email,
                                        participant_phone=user_info.phone)
            ticket_flow_history_restful = dict(id=str(ticket_flow_history.id), ticket_id=str(ticket_id),
                                               node_info=node_info, processor_info=processor_info,
                                               comment=ticket_flow_history.comment,
                                               action_type=ticket_flow_history.action_type,
                                               action_name=action_name,
                                               created_at=ticket_flow_history.created_at.strftime('%Y-%m-%d %H:%M:%S %z'))
            if include_ticket_data:
                ticket_flow_history_restful.update(ticket_data=ticket_flow_history.ticket_data)
            ticket_flow_history_object_format_list.append(ticket_flow_history_restful)

        return dict(ticket_flow_history_object_format_list=ticket_flow_history_object_format_list,
                    paginator_info=dict(per_page=per_page, page=page, total=paginator.count))













ticket_flow_history_service_ins = TicketFlowHistoryService()
