import json
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from service.format_response import api_response
from service.ticket.ticket_base_service import TicketBaseService


class TicketListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工单列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        username = request_data.get('username', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        category = request_data.get('category', 'all')
        ticket_result_restful_list, msg = TicketBaseService.get_ticket_list(sn=sn, title=title, username=username,
                                                                            create_start=create_start, create_end=create_end,
                                                                            category=category, reverse=reverse, per_page=per_page, page=page)
        if ticket_result_restful_list is not False:
            data = dict(value=ticket_result_restful_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新建工单，需要根据不同类型工单传的参数不一样
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        new_ticket_result, msg = TicketBaseService.new_ticket(request_data_dict)
        if new_ticket_result:
            code, data = 0, {'ticket_id': new_ticket_result.id}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

def ticketlist(response):
    if response.method == 'POST':
        return HttpResponse('postssss')
