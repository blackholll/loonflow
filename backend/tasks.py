# from __future__ import absolute_import, unicode_literals
import contextlib
import os
import sys
import traceback
import logging
from celery import Celery
from service.account.account_dept_service import account_dept_service_ins
from service.account.account_role_service import account_role_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.hook.hook_base_service import hook_base_service_ins
from service.ticket.ticket_flow_history_service import ticket_flow_history_service_ins
from service.ticket.ticket_node_service import ticket_node_service_ins

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.config')
import django
django.setup()

app = Celery('loonflow')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import json
import requests
from apps.ticket.models import TicketRecord
from apps.workflow.models import Transition, Node, Workflow, WorkflowNotice
from apps.manage.models import Notification
from service.account.account_user_service import account_user_service_ins
from service.common.constant_service import constant_service_ins
from service.ticket.ticket_base_service import TicketBaseService, ticket_base_service_ins
from service.common.common_service import CommonService, common_service_ins
from service.workflow.workflow_transition_service import WorkflowTransitionService, workflow_transition_service_ins
from django.conf import settings

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

logger = logging.getLogger('django')



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def test_task(a, b):
    print('a:', a)
    print('b:', b)
    print(a+b)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        try:
            # for python2
            stdout = StringIO.StringIO()
        except Exception:
            stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old




@app.task
def timer_transition(tenant_id, ticket_id, node_id, date_time, transition_id):
    """
    timer transition
    need no flow record for this node, then run time transition
    :param tenant_id:
    :param ticket_id:
    :param node_id:
    :param date_time:
    :param transition_id:
    :return:
    """
    flow_history_result = ticket_flow_history_service_ins.get_ticket_flow_history(tenant_id, ticket_id, 10000, 1)
    ticket_flow_history_object_format_list = flow_history_result.get("ticket_flow_history_object_format_list")
    for ticket_flow_history_object_format in ticket_flow_history_object_format_list:
        if ticket_flow_history_object_format.get("node_info").get("id") == node_id and ticket_flow_history_object_format.get("created_at") > date_time:
            return "warning: have flow history, timer is invalid"
    handle_ticket_data = dict(transition_id=transition_id, operator='loonrobot', suggestion='定时器流转')
    ticket_base_service_ins.handle_ticket(tenant_id, ticket_id, handle_ticket_data, True)



@app.task
def send_ticket_notice(tenant_id: int, ticket_id: int):
    """
    send ticket notice
    :param ticket_id:
    :return:
    """
    # get ticket info
    # get workflow notice config
    # get notice title and content template
    # hook with title content, ticket info
    ticket_obj = TicketRecord.objects.get(id=ticket_id)

    workflow_id = ticket_obj.workflow_id
    workflow_obj = Workflow.objects.get(id=workflow_id)
    workflow_notices = WorkflowNotice.objects.get(workflow_id=workflow_id).workflow_notices

    notice_str_list = workflow_notices.split(',')
    notice_id_list = [int(notice_str) for notice_str in notice_str_list]
    send_notice_result_list = []

    title_template = workflow_obj.title_template
    content_template = workflow_obj.content_template

    ticket_value_info = ticket_base_service_ins.get_ticket_all_field_value(ticket_id)

    title_result = title_template.format(**ticket_value_info)
    content_result = content_template.format(**ticket_value_info)

    flow_history_result = ticket_flow_history_service_ins.get_ticket_flow_history(tenant_id, ticket_id, 1)
    latest_history = flow_history_result.get("ticket_flow_history_object_format_list")[0]
    participant_queryset = account_user_service_ins.get_ticket_current_participant_list(tenant_id, ticket_id)
    participant_info_list = []
    for participant in participant_queryset:
        participant_info_list.append(dict(username=participant.username, alias=participant.alias,
                                          phone=participant.phone, email=participant.email))

    params = {'title_result': title_result, 'content_result': content_result,
              'participant': ticket_obj.participant, 'participant_type_id': ticket_obj.participant_type_id,
              'ticket_value_info': ticket_value_info, 'latest_history': latest_history,
              'participant_info_list': participant_info_list}
    for notice_id in notice_id_list:
        notice_obj = Notice.objects.filter(id=notice_id).first()
        if not notice_obj:
            continue
        hook_url = notice_obj.hook_url
        from service.workflow.workflow_base_service import workflow_base_service_ins
        flag, msg = workflow_base_service_ins.hook_host_valid_check(hook_url)
        if not flag:
            return False, msg
        hook_token = notice_obj.hook_token
        # gen signature
        flag, headers = common_service_ins.gen_signature_by_token(hook_token)
        try:
            r = requests.post(hook_url, headers=headers, json=params)
            result = r.json()
            if result.get('code') == 0:
                send_notice_result_list.append(dict(notice_id=notice_id, result='success', msg=result.get('msg', '')))
            else:
                send_notice_result_list.append(dict(notice_id=notice_id, result='fail', msg=result.get('msg', '')))
        except Exception as e:
            send_notice_result_list.append(dict(notice_id=notice_id, result='fail', msg=e.__str__()))
    return send_notice_result_list


@app.task
def flow_hook_task(tenant_id: int, ticket_id: int, node_id: int):
    """
    hook task
    :param tenant_id:
    :param ticket_id:
    :param node_id:
    :return:
    """
    node_obj = Node.objects.get(id=node_id)
    hook_config = node_obj.participant
    hook_config_dict = json.loads(hook_config)
    hook_url = hook_config_dict.get('hook_url')
    hook_token = hook_config_dict.get('hook_token')
    wait = hook_config_dict.get('wait')
    extra_info = hook_config_dict.get('extra_info')

    participant_type = node_obj.participant_type
    if participant_type != "hook":
        return CustomCommonException("current node's participant is not hook")

    all_ticket_data = ticket_base_service_ins.get_ticket_all_field_value(ticket_id)
    all_ticket_data.update(extra_info=extra_info)
    hook_result = hook_base_service_ins.call_hook(hook_url, hook_token, all_ticket_data)
    comment = hook_result.get("msg")
    ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, 0, ticket_id, 0, comment, "hook", "", node_id, "hook",
                                                            all_ticket_data)
    if hook_result.get("code") == 0:
        if not wait:
            transition_queryset = workflow_transition_service_ins.get_transition_queryset_by_source_node_id(node_id)
            transition_id = transition_queryset[0].id  # only support one transition behind hook
            all_ticket_data.update(transition_id=transition_id)
            ticket_base_service_ins.handle_ticket(ticket_id, all_ticket_data, by_hook=True)
    else:
        ticket_node_participant_obj = dict()
        ticket_node_participant_obj["ticket_id"] = ticket_id
        ticket_node_participant_obj["node_id"] = node_id
        ticket_node_participant_obj["in_add_node"] = False
        ticket_node_participant_obj["add_node_target"] = ""
        ticket_node_participant_obj["hook_state"] = "fail"
        ticket_node_participant_obj["all_participant_result"] = {}
        ticket_node_service_ins.update_batch_record(tenant_id, [ticket_node_participant_obj])
    return True
