from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from service import format_response
from service.ticket.ticket_type_service import TICKET_TYPE_SERVICE, TicketTypeService
from apps.ticket.serializers import TicketTypeSerializer, FormatTicketTypeSerializer
from rest_framework import status


class TicketTypeAPIView(APIView):
    """
    工单类别
    """
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = request.GET
        query_value = request_data.get('query_value', '')
        page = int(request_data.get('page', 1)) if request_data.get('page', 0) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10

        ticket_types, msg = TicketTypeService.get_ticket_types(query_value, per_page, page)

        if ticket_types is not False:
            ticket_type_serializer_list = [TicketTypeSerializer(ticket_type) for ticket_type in ticket_types]

            ticket_type_serializer_list = [ticket_type_serializer.data for ticket_type_serializer in
                                           ticket_type_serializer_list]

            return format_response.JsonResponse(data=ticket_type_serializer_list, code=status.HTTP_200_OK,
                                                per_page=msg.get('per_page', ''), page=msg.get('page', ''),
                                                total=msg.get('total', ''))
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_OK, msg=msg)


class FormatTicketTypeAPIView(APIView):
    """
    新建工单选择项目
    """
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = request.GET
        query_value = request_data.get('query_value', '')
        page = int(request_data.get('page', 1)) if request_data.get('page', 0) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10

        ticket_types, msg = TicketTypeService.get_format_ticket_types(query_value, per_page, page)

        if ticket_types is not False:
            ticket_type_serializer_list = [FormatTicketTypeSerializer(ticket_type) for ticket_type in ticket_types]

            ticket_type_serializer_list = [ticket_type_serializer.data for ticket_type_serializer in
                                           ticket_type_serializer_list]

            return format_response.JsonResponse(data=ticket_type_serializer_list, code=status.HTTP_200_OK,
                                                per_page=msg.get('per_page', ''), page=msg.get('page', ''),
                                                total=msg.get('total', ''))
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_OK, msg=msg)

