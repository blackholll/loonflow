import json
from django.http import HttpResponse
from django.views import View
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
        workflow_ids = request_data.get('workflow_ids', '')
        state_ids = request_data.get('state_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        category = request_data.get('category')
        ticket_result_restful_list, msg = TicketBaseService.get_ticket_list(sn=sn, title=title, username=username,
                                                                            create_start=create_start, create_end=create_end,
                                                                            workflow_ids=workflow_ids, state_ids=state_ids, category=category, reverse=reverse, per_page=per_page, page=page)
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
            code, data = 0, {'ticket_id': new_ticket_result}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class TicketView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工单详情，根据用户返回不同的内容(是否有工单表单的编辑权限)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get('username', '')
        if not username:
            return api_response(-1, '参数不全，请提供username', '')
        result, msg = TicketBaseService.get_ticket_detail(ticket_id, username)
        if result:
            code, data = 0, dict(value=result)
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

    def patch(self, request, *args, **kwargs):
        """
        处理工单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'patch参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        result, msg = TicketBaseService.handle_ticket(ticket_id, request_data_dict)
        if result or result is not False:
            code, data = 0, dict(value=result)
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class TicketTransition(View):
    """
    工单可以做的操作
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get('username', '')
        if not username:
            return api_response(-1, '参数不全，请提供username', '')
        result, msg = TicketBaseService.get_ticket_transition(ticket_id, username)
        if result or result is not False:
            code, data = 0, dict(value=result)
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class TicketFlowlog(View):
    """
    工单流转记录
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get('username', '')  # 可用于权限控制
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        if not username:
            return api_response(-1, '参数不全，请提供username', '')

        result, msg = TicketBaseService.get_ticket_flow_log(ticket_id, username, per_page, page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class TicketFlowStep(View):
    """
    工单流转step: 用于显示工单当前状态的step图(线形结构，无交叉)
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get('username', '')  # 可用于权限控制
        if not username:
            return api_response(-1, '参数不全，请提供username', '')

        result, msg = TicketBaseService.get_ticket_flow_step(ticket_id, username)
        if result is not False:
            data = dict(value=result)
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class TicketState(View):
    """
    工单状态
    """
    def put(self, request, *args, **kwargs):
        """
        修改工单状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'patch参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request_data_dict.get('username', '')  # 可用于权限控制
        state_id = request_data_dict.get('state_id')
        if not state_id:
            code = -1
            msg = '请提供新的状态id'
            data = ''
        else:
            result, msg = TicketBaseService.update_ticket_state(ticket_id, state_id, username)
            if result:
                code, msg, data = 0, msg, ''
            else:
                code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketsStates(View):
    def get(self, request, *args, **kwargs):
        """
        批量获取工单状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request_data.get('username', '')  # 可用于权限控制
        ticket_ids = request_data.get('ticket_ids')  # 逗号隔开
        ticket_id_list = ticket_ids.split(',')
        ticket_id_list = [int(ticket_id) for ticket_id in ticket_id_list]

        result, msg = TicketBaseService.get_tickets_states_by_ticket_id_list(ticket_id_list, username)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketAccept(View):
    def post(self, request, *args, **kwargs):
        """
        接单,当工单当前处理人实际为多个人时(角色、部门、多人都有可能， 注意角色和部门有可能实际只有一人)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request_data_dict.get('username', '')
        result, msg = TicketBaseService.accept_ticket(ticket_id, username)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketDeliver(View):
    def post(self, request, *args, **kwargs):
        """
        转交操作会直接修改工单处理人，且工单状态不变，所以在使用的时候可以在前端做些提醒 避免用户把工单直接转交给下个人，从而干扰了工单的正常流转(
        如用户提交了一个请假单，部门TL审批状态下，tl本来应该点击"同意"，工单会自动流转到财务人员审批状态。 应该避免tl直接将工单转交给了某个财务)。这个地方后续会考虑怎么优化下，目前先在前端做提醒
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request_data_dict.get('username', '')
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')

        result, msg = TicketBaseService.deliver_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketAddNode(View):
    def post(self, request, *args, **kwargs):
        """
        加签,加签操作会修改工单处理人，工单状态不表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request_data_dict.get('username', '')
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')
        result, msg = TicketBaseService.add_node_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketAddNodeEnd(View):
    def post(self, request, *args, **kwargs):
        """
        加签处理完成,加签完成操作后工单处理人回回到之前加签发起人
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request_data_dict.get('username', '')
        suggestion = request_data_dict.get('suggestion', '')
        result, msg = TicketBaseService.add_node_ticket_end(ticket_id, username, suggestion)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)




def ticketlist(response):
    if response.method == 'POST':
        return HttpResponse('postssss')
    else:
        return HttpResponse('getsss')
