import json
from django.http import HttpResponse
from django.views import View
from schema import Schema, Regex, And, Or, Use, Optional

from apps.loon_base_view import LoonBaseView
from service.account.account_base_service import account_base_service_ins
from service.format_response import api_response
from service.ticket.ticket_base_service import ticket_base_service_ins


class TicketListView(LoonBaseView):
    post_schema = Schema({
        'workflow_id': And(int, lambda n: n != 0, error='workflow_id is needed and type should be int'),
        'transition_id': And(int, lambda n: n != 0, error='transition_id is needed and type should be int'),
        str: object
    })

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

        # 待办,关联的,创建
        category = request_data.get('category')
        # app_name
        app_name = request.META.get('HTTP_APPNAME')

        # 未指定创建起止时间则取最近三年的记录
        if not(create_start or create_end):
            import datetime
            end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            last_year_time = datetime.datetime.now() - datetime.timedelta(days=365*3)
            create_start = str(last_year_time)[:19]
            create_end = str(end_time)[:19]

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
        新建工单，需要根据不同类型工单传的参数不一样
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')

        request_data_dict = json.loads(json_str)

        app_name = request.META.get('HTTP_APPNAME')
        request_data_dict.update(dict(username=request.META.get('HTTP_USERNAME')))

        # 判断是否有创建某工单的权限
        app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, request_data_dict.get('workflow_id'))
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to create this workflow ticket'.format(app_name), '')

        flag, result = ticket_base_service_ins.new_ticket(request_data_dict, app_name)
        if flag:
            code, data = 0, {'ticket_id': result.get('new_ticket_id')}
        else:
            code, data = -1, {}
        return api_response(code, result, data)


class TicketView(LoonBaseView):
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
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        # username = request_data.get('username', '')
        username = request.META.get('HTTP_USERNAME')
        if not username:
            return api_response(-1, '参数不全，请提供username', '')
        flag, result = ticket_base_service_ins.get_ticket_detail(ticket_id, username)
        if flag:
            code, data = 0, dict(value=result)
        else:
            code, data, msg = -1, {}, result
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
        删除工单，仅用于管理员干预处理工单，loonflow管理后台的功能
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 校验工单权限
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
    工单可以做的操作
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
            return api_response(-1, '参数不全，请提供username', '')
        flag, result = ticket_base_service_ins.get_ticket_transition(ticket_id, username)
        if flag is False:
            code, data, msg = -1, {}, result
        else:
            code, data, msg = 0, dict(value=result.get('transition_dict_list')), ''

        return api_response(code, msg, data)


class TicketFlowlog(LoonBaseView):
    """
    工单流转记录
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        ticket_data = int(request_data.get('ticket_data', 0))
        desc = int(request_data.get('desc', 1)) # 是否降序
        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            return api_response(-1, '参数不全，请提供username', '')

        flag, result = ticket_base_service_ins.get_ticket_flow_log(ticket_id, username, per_page, page, ticket_data, desc)

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
    工单流转step: 用于显示工单当前状态的step图(线形结构，无交叉)
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        # username = request_data.get('username', '')  # 可用于权限控制
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            return api_response(-1, '参数不全，请提供username', '')

        flag, result = ticket_base_service_ins.get_ticket_flow_step(ticket_id, username)
        if flag is not False:
            data = dict(value=result.get('state_step_dict_list'), current_state_id=result.get('current_state_id'))
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class TicketState(LoonBaseView):
    """
    工单状态
    """
    put_schema = Schema({
        'state_id': And(int, lambda n: n != 0, error='state_id is needed and type should be int'),
        Optional('suggestion'): str,
    })

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
        username = request.META.get('HTTP_USERNAME')
        state_id = request_data_dict.get('state_id')
        suggestion = request_data_dict.get('suggestion', '')

        app_name = request.META.get('HTTP_APPNAME')
        # 调用来源应用是否有此工单对应工作流的权限校验
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        # 强制修改工单状态需要对应工作流的管理员或者超级管理员
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
        批量获取工单状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        # username = request_data.get('username', '')  # 可用于权限控制
        username = request.META.get('HTTP_USERNAME')
        ticket_ids = request_data.get('ticket_ids')  # 逗号隔开
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
        接单,当工单当前处理人实际为多个人时(角色、部门、多人都有可能， 注意角色和部门有可能实际只有一人)
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
        转交操作会直接修改工单处理人，且工单状态不变，所以在使用的时候可以在前端做些提醒 避免用户把工单直接转交给下个人，从而干扰了工单的正常流转(
        如用户提交了一个请假单，部门TL审批状态下，tl本来应该点击"同意"，工单会自动流转到财务人员审批状态。 应该避免tl直接将工单转交给了某个财务)。这个地方后续会考虑怎么优化下，目前先在前端做提醒
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
            # 非管理员操作，校验用户是否有处理权限
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
        加签,加签操作会修改工单处理人，工单状态不表
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
        修改工单字段
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
        重新执行工单脚本(用于脚本执行出错的情况), 也可用于hook执行失败的情况
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        username = request.META.get('HTTP_USERNAME')

        app_name = request.META.get('HTTP_APPNAME')
        app_permission_check, msg = account_base_service_ins.app_ticket_permission_check(app_name, ticket_id)
        if not app_permission_check:
            return api_response(-1, msg, '')

        if not username:
            api_response(-1, 'need arg username', '')
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
        添加评论
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
        工单hook回调，用于hoot请求后，被请求方执行完任务后回调loonflow,以触发工单继续流转
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ticket_id = kwargs.get('ticket_id')
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
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
        工单当前处理人详情，调用方后端可用获取处理人信息后提供催办等功能
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
        强制关闭工单
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
        工单个数统计
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
        撤回工单，允许创建人在指定状态撤回工单至初始状态，状态设置中开启允许撤回
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
        上传文件
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
