import json
from django.http import HttpResponse
from django.views import View
from schema import Schema, Regex, And, Or, Use, Optional

from apps.loon_base_view import LoonBaseView
from service.account.account_base_service import account_base_service_ins
from service.format_response import api_response
from service.ticket.ticket_base_service import ticket_base_service_ins
from django.utils.translation import ugettext_lazy as _


class TicketListView(LoonBaseView):
    post_schema = Schema({
        'workflow_id': And(int, lambda n: n != 0, error='workflow_id is needed and type should be int'),
        'transition_id': And(int, lambda n: n != 0, error='transition_id is needed and type should be int'),
        str: object
    })

    def get(self, request, *args, **kwargs):
        """
        Get a list of tickets
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        # username = request_data.get('username', '')
        username = request.META.get('HTTP_USERNAME')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        state_ids = request_data.get('state_ids', '')
        ticket_ids = request_data.get('ticket_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        act_state_id = request_data.get('act_state_id', '')
        from_admin = request_data.get('from_admin', '')
        creator = request_data.get('creator', '')
        parent_ticket_id = int(request_data.get('parent_ticket_id', 0))
        parent_ticket_state_id = int(request_data.get('parent_ticket_state_id', 0))

        # to do, associated, create
        category = request_data.get('category')
        # app_name
        app_name = request.META.get('HTTP_APPNAME')

        # If the start and end time of creation is not specified, the records of the most recent year will be taken
        if not(create_start or create_end):
            import datetime
            now = datetime.datetime.now()
            now_str = str(now)[:19]
            last_year_time = '%4d%s' % (now.year-1, now_str[4:])
            datetime.datetime.now() - datetime.timedelta(days=365)
            create_start = last_year_time
            create_end = now_str

        flag, result = ticket_base_service_ins.get_ticket_list(
            sn=sn, title=title, username=username, create_start=create_start, create_end=create_end,
            workflow_ids=workflow_ids, state_ids=state_ids, ticket_ids=ticket_ids, category=category, reverse=reverse,
            per_page=per_page, page=page, app_name=app_name, act_state_id=act_state_id, from_admin=from_admin,
            creator=creator, parent_ticket_id=parent_ticket_id, parent_ticket_state_id=parent_ticket_state_id)
        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('ticket_result_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg,  = 0, ''
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        To create a new work order, you need to pass different parameters according to different types of work orders
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')

        request_data_dict = json.loads(json_str)

        app_name = request.META.get('HTTP_APPNAME')
        request_data_dict.update(dict(username=request.META.get('HTTP_USERNAME')))

        # Determine whether you have permission to create a work order
        app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, request_data_dict.get('workflow_id'))
        if not app_permission:
            return api_response(-1, _('APP:{} have no permission to create this workflow ticket').format(app_name), '')

        flag, result = ticket_base_service_ins.new_ticket(request_data_dict, app_name)
        if flag:
            code, data = 0, {'ticket_id': result.get('new_ticket_id')}
        else:
            code, data = -1, {}
        return api_response(code, result, data)


class TicketView(LoonBaseView):
    def get(self, request, *args, **kwargs):
        """
        Get the details of the work order, and return different content according to the user (whether there is editing permission for the work order form)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        # username = request_data.get('username', '')
        username = request.META.get('HTTP_USERNAME')
        if not username:
            return api_response(-1, _('Incomplete parameters, please provide username'), '')
        flag, result = ticket_base_service_ins.get_ticket_detail(ticket_id, username)
        if flag:
            code, data = 0, dict(value=result)
        else:
            code, data, msg = -1, {}, result
        return api_response(code, msg, data)

    def patch(self, request, *args, **kwargs):
        """
        Process work orders
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('patch parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')

        app_name = request.META.get('HTTP_APPNAME')
        request_data_dict.update(dict(username=request.META.get('HTTP_USERNAME')))
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, {})

        result, msg = ticket_base_service_ins.handle_ticket(ticket_id, request_data_dict)
        if result or result is not False:
            code, data = 0, dict(value=result)
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        Delete the work order, only for the administrator to intervene in the processing of the work order,
        the function of the loonflow management background
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # Verify work order permissions
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        json_str = request.body.decode('utf-8')
        suggestion = ''
        if json_str:
            request_data_dict = json.loads(json_str)
            suggestion = request_data_dict.get('suggestion')

        flag, result = ticket_base_service_ins.ticket_admin_permission_check(ticket_id, username)
        if flag is False:
            return api_response(-1, result, {})
        flag, result = ticket_base_service_ins.delete_ticket(ticket_id, username, suggestion)
        if flag is False:
            return api_response(-1, result, {})
        else:
            return api_response(0, '', {})


class TicketTransition(LoonBaseView):
    """
    What the work order can do
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        # username = request_data.get('username', '')
        username = request.META.get('HTTP_USERNAME')
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(0, msg, dict(value=[]))

        if not username:
            return api_response(-1, _('Incomplete parameters, please provide username'), '')
        flag, result = ticket_base_service_ins.get_ticket_transition(ticket_id, username)
        if flag is False:
            code, data, msg = -1, {}, result
        else:
            code, data, msg = 0, dict(value=result.get('transition_dict_list')), ''

        return api_response(code, msg, data)


class TicketFlowlog(LoonBaseView):
    """
    Work order transfer record
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        ticket_data = int(request_data.get('ticket_data', 0))
        desc = int(request_data.get('desc', 1)) # descending order
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            return api_response(-1, _('Incomplete parameters, please provide username'), '')

        flag, result = ticket_base_service_ins.get_ticket_flow_log(
            ticket_id, username, per_page, page, ticket_data, desc
        )

        if flag is not False:
            paginator_info = result.get('paginator_info')
            data = dict(value=result.get('ticket_flow_log_restful_list'), per_page=paginator_info.get('per_page'),
                        page=paginator_info.get('page'), total=paginator_info.get('total'))
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class TicketFlowStep(LoonBaseView):
    """
    Work order flow step: step diagram used to display the current state of the work order (linear structure, no intersection)
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        # username = request_data.get('username', '')  # Can be used for permission control
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            return api_response(-1, _('Incomplete parameters, please provide username'), '')

        flag, result = ticket_base_service_ins.get_ticket_flow_step(ticket_id, username)
        if flag is not False:
            data = dict(value=result.get('state_step_dict_list'), current_state_id=result.get('current_state_id'))
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class TicketState(LoonBaseView):
    """
    work order status
    """
    put_schema = Schema({
        'state_id': And(int, lambda n: n != 0, error='state_id is needed and type should be int'),
        Optional('suggestion'): str,
    })

    def put(self, request, *args, **kwargs):
        """
        Modify ticket status
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('patch parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        state_id = request_data_dict.get('state_id')
        suggestion = request_data_dict.get('suggestion', '')

        app_name = request.META.get('HTTP_APPNAME')
        # Whether the calling source application has permission verification for the workflow corresponding to this ticket
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        # Forcibly modifying the work order status requires the administrator or super administrator of the corresponding workflow
        flag, result = ticket_base_service_ins.ticket_admin_permission_check(ticket_id, username)
        if flag is False:
            return api_response(-1, result, {})

        flag, result = ticket_base_service_ins.update_ticket_state(ticket_id, state_id, username, suggestion)
        if flag is False:
            return api_response(-1, result, {})
        else:
            return api_response(0, '', {})


class TicketsStates(LoonBaseView):
    def get(self, request, *args, **kwargs):
        """
        Get work order status in batches
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        # username = request_data.get('username', '')  # Can be used for permission control
        username = request.META.get('HTTP_USERNAME')
        ticket_ids = request_data.get('ticket_ids')  # comma separated
        ticket_id_list = ticket_ids.split(',')
        ticket_id_list = [int(ticket_id) for ticket_id in ticket_id_list]

        flag, result = ticket_base_service_ins.get_tickets_states_by_ticket_id_list(ticket_id_list, username)
        if flag:
            code, msg, data = 0, '', result
        else:
            code, msg, data = -1, result, ''
        return api_response(code, msg, data)


class TicketAccept(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        Accepting an order, when the current handling person of the work order is actually multiple people
        (roles, departments, and multiple people are possible,
         note that roles and departments may actually have only one person)

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        result, msg = ticket_base_service_ins.accept_ticket(ticket_id, username)
        if result:
            code, msg, data = 0, msg, {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketDeliver(LoonBaseView):
    post_schema = Schema({
        'target_username': And(str, lambda n: n != '', error='target_username is needed'),
        Optional('from_admin'): int,
        Optional('suggestion'): str,
    })

    def post(self, request, *args, **kwargs):
        """
        The transfer operation will directly modify the work order handler,
        and the work order status will remain unchanged,
        so you can make some reminders on the front end when using it to
        prevent the user from directly transferring the work order to the next person,
        thus interfering with the normal flow of the work order (
        If the user submits a leave request, the TL should have clicked "Agree"
        in the approval state of the department TL,
        and the work order will be automatically transferred to the approval state of the financial staff.
        It should be avoided that tl hand over the work order directly to a finance).
        This place will consider how to optimize it in the future. At present, it will be reminded on the front end.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')
        from_admin = request_data_dict.get('from_admin', 0)

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, {})

        if from_admin:
            flag, result = ticket_base_service_ins.ticket_admin_permission_check(ticket_id, username)
            if flag is False:
                return api_response(-1, result, {})
        else:
            # Non-administrator operation, check whether the user has processing rights
            flag, result = ticket_base_service_ins.ticket_handle_permission_check(ticket_id, username)
            if flag is False:
                return api_response(-1, result, {})
            if result.get('permission') is False:
                return api_response(-1, result.get('msg'), {})

        result, msg = ticket_base_service_ins.deliver_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 0, msg, result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketAddNode(LoonBaseView):
    post_schema = Schema({
        'target_username': And(str, lambda n: n != '', error='target_username is needed'),
        Optional('suggestion'): str,
    })

    def post(self, request, *args, **kwargs):
        """
        Add sign, the add sign operation will modify the work order handler, and the work order status is not displayed
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        target_username = request_data_dict.get('target_username', '')
        suggestion = request_data_dict.get('suggestion', '')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        result, msg = ticket_base_service_ins.add_node_ticket(ticket_id, username, target_username, suggestion)
        if result:
            code, msg, data = 0, msg, {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketAddNodeEnd(LoonBaseView):
    post_schema = Schema({
        Optional('suggestion'): str,
    })

    def post(self, request, *args, **kwargs):
        """
        The signature processing is completed.
        After the signature processing is completed, the work order handler returns to the previous issuer to add the signature
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('post parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        suggestion = request_data_dict.get('suggestion', '')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        result, msg = ticket_base_service_ins.add_node_ticket_end(ticket_id, username, suggestion)
        if result:
            code, msg, data = 0, msg, {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketField(LoonBaseView):

    def patch(self, request, *args, **kwargs):
        """
        Modify ticket fields
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('post parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)

        if not app_permission_check:
            return api_response(-1, msg, '')

        result, msg = ticket_base_service_ins.update_ticket_field_value(ticket_id, request_data_dict)
        if result:
            code, msg, data = 0, msg, {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketScriptRetry(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        Re-execute the ticket script (for the case of script execution error),
         also for the case of hook execution failure
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            api_response(-1, _('need arg username'), '')
        result, msg = ticket_base_service_ins.retry_ticket_script(ticket_id, username)
        if result:
            code, msg, data = 0, 'Ticket script or hook retry start successful', {}
        else:
            code, msg, data = -1, msg, {}
        return api_response(code, msg, data)


class TicketComment(LoonBaseView):

    post_schema = Schema({
        'suggestion': And(str, lambda n: n != '', error='suggestion is needed'),
    })

    def post(self, request, *args, **kwargs):
        """
        add comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('Post parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        suggestion = request_data_dict.get('suggestion', '')
        result, msg = ticket_base_service_ins.add_comment(ticket_id, username, suggestion)
        if result:
            code, msg, data = 0, 'add ticket comment successful', {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketHookCallBack(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        The work order hook callback is used to call back loonflow after the requested party has performed the task after the hoot request to trigger the work order to continue to flow.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, _('post parameter is empty'), {})
        request_data_dict = json.loads(json_str)
        app_name = request.META.get('HTTP_APPNAME')

        result, msg = ticket_base_service_ins.hook_call_back(ticket_id, app_name, request_data_dict)
        if result:
            code, msg, data = 0, 'add ticket comment successful', {}
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class TicketParticipantInfo(LoonBaseView):
    def get(self, request, *args, **kwargs):
        """
        Details of the current handler of the work order.
        The caller's backend can obtain the handler information and provide functions such as reminders
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        flag, msg = ticket_base_service_ins.get_ticket_participant_info(ticket_id)
        if flag:
            code, msg, data = 0, '', msg
        else:
            code, msg, data = -1, msg, {}
        return api_response(code, msg, data)


class TicketClose(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        Force close a ticket
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        ticket_id = kwargs.get('ticket_id')
        request_data_dict = json.loads(json_str)
        username = request.META.get('HTTP_USERNAME')
        suggestion = request_data_dict.get('suggestion', '')

        flag, result = ticket_base_service_ins.close_ticket_permission_check(ticket_id, username)
        if flag is False:
            return api_response(-1, result, {})

        flag, msg = ticket_base_service_ins.close_ticket(ticket_id, username, suggestion)
        if flag:
            code, msg, data = 0, '', msg
        else:
            code, msg, data = -1, msg, {}
        return api_response(code, msg, data)


class TicketsNumStatistics(LoonBaseView):
    def get(self, request, *args, **kwargs):
        """
        Statistics of work orders
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        start_date = kwargs.get('start_date', '')
        end_date = kwargs.get('end_date', '')
        username = request.META.get('HTTP_USERNAME')

        flag, result = ticket_base_service_ins.get_ticket_num_statistics(start_date, end_date, username)
        if flag:
            return api_response(0, '', result.get('result_list'))
        else:
            return api_response(-1, result, {})


class TicketRetreat(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        Withdraw the work order,
        allowing the creator to withdraw the work order to the initial state in the specified state, and enable the allowable withdrawal in the state settings
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        suggestion = request_data_dict.get('suggestion', '')

        flag, result = ticket_base_service_ins.retreat_ticket(ticket_id, username, suggestion)
        if flag:
            return api_response(0, '', {})
        else:
            return api_response(-1, result, {})


class UploadFile(LoonBaseView):
    def post(self, request, *args, **kwargs):
        """
        upload files
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        flag, result = ticket_base_service_ins.upload_file(request)
        if flag:
            return api_response(0, '', result)
        else:
            return api_response(-1, result, {})
