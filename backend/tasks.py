import contextlib
import traceback
import os
import sys
import logging
from celery import Celery

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

import requests
from django.conf import settings
from io import StringIO
from service.workflow.workflow_hook_service import workflow_hook_service_ins
from service.ticket.ticket_flow_history_service import ticket_flow_history_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.workflow.workflow_node_service import workflow_node_service_ins
from service.ticket.ticket_node_service import ticket_node_service_ins
from service.ticket.ticket_base_service import ticket_base_service_ins
from service.ticket.ticket_field_service import ticket_field_service_ins
from service.common.common_service import common_service_ins
from service.workflow.workflow_edge_service import workflow_edge_service_ins
from service.workflow.workflow_notification_service import workflow_notification_service_ins
from service.ticket.ticket_user_service import ticket_user_service_ins
from service.account.account_user_service import account_user_service_ins
from service.manage.notification_service import notification_service_ins

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
def flow_hook_task(tenant_id:str, ticket_id: str, node_id: str):
    """
    flow hook task
    :param ticket_id:
    :param node_id:
    :return:
    """
    # 1.query currenet ticket_node, 2.check whether have ticke_node with assignee_type is hook 3.trigger hook
    current_ticket_node_list = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
    for current_ticket_node in current_ticket_node_list:
        if current_ticket_node.assignee_type == "hook" and current_ticket_node.id == node_id:
            # todo: trigger hook
            workflow_node_record = workflow_node_service_ins.get_node_by_id(tenant_id, current_ticket_node.node_id)
            workflow_node_props = workflow_node_record.props
            hook_url = workflow_node_props.get("hook_url")
            hook_token = workflow_node_props.get("hook_token")
            signature, timestamp = common_service_ins.gen_signature_by_token(hook_token)
            is_async = workflow_node_props.get("is_async")
            ticket_field_values = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
            try:
                r = requests.post(hook_url, json=dict(type="flow_hook", fields=ticket_field_values, is_async=is_async), headers=dict(signature=signature, timestamp=timestamp))
                result = r.json()
            except Exception as e:
                logger.error(traceback.format_exc())
                result = dict(code=-1, msg=str(e))
            if result.get("code") == 0:
                # TOOO: add flow history, and update hook status
                ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, 'hook', ticket_id, "hook", None, "", "hook", "*", node_id, ticket_field_values)
                ticket_node_service_ins.update_ticket_node_hook_status(tenant_id, ticket_id, node_id, "success")
                if not is_async:
                    # get first edge, hook node should have only one out edge
                    out_edge_record_list = workflow_edge_service_ins.get_workflow_edges_by_source_node_id(tenant_id, workflow_node_record.workflow_id, workflow_node_record.version_id, node_id)
                    out_edge_id = str(out_edge_record_list[0].id)
                    hook_handle_data_dict = dict( action_id=out_edge_id,
                    action_props = dict(node_id=node_id),
                    fields = {},
                    comment = ""
                    )
                    ticket_base_service_ins.handle_ticket(tenant_id, "loonflow", ticket_id, 'hook', hook_handle_data_dict)
                else: 
                    return True
            else:
                ticket_flow_history_service_ins.add_ticket_flow_history(tenant_id, 'hook', ticket_id, "hook", None, "", "hook", "*", node_id, ticket_field_values)
            ticket_node_service_ins.update_ticket_node_hook_status(tenant_id, ticket_id, node_id, "failed")
    return True


@app.task
def flow_notification_task(tenant_id:str, ticket_id: str, target_node_id: str):
    """
    flow timer task
    :param ticket_id:
    :param node_id:
    :param action_type:
    :param action_id:
    :return:
    """
    # 1. get ticket recored 2.get notificaton id from workflow info 3.get notificaton configure 4. get assignee info 5. send notification
    ticket_record = ticket_base_service_ins.get_ticket_by_id(tenant_id, ticket_id)
    workflow_id = ticket_record.workflow_id
    workflow_version_id = ticket_record.workflow_version_id
    workflow_notification_record = workflow_notification_service_ins.get_notification_record_by_workflow_id_and_version_id(tenant_id, workflow_id, workflow_version_id)
    title_template = workflow_notification_record.title_template
    content_template = workflow_notification_record.content_template
    if workflow_notification_record.channels:
        selected_channel_id_list = workflow_notification_record.channels.split(',')
    else:
        selected_channel_id_list = []
        return True
    ticket_field_values = ticket_field_service_ins.get_ticket_all_field_value(tenant_id, ticket_id)
    title_template_format = title_template.format(**ticket_field_values)
    content_template_format = content_template.format(**ticket_field_values)
    
    ticket_node_list = ticket_node_service_ins.get_ticket_current_nodes(tenant_id, ticket_id)
    assignee_id_list = []
    for ticket_node in ticket_node_list:
        if ticket_node.node_id == target_node_id:
            assignee_type = ticket_node.assignee_type
            assignee = ticket_node.assignee
            if assignee_type == "users":
                # dept or role will transform to users then save to ticket_node table
                assignee_id_list = assignee.split(',')
    notification_to_user_record_list = account_user_service_ins.get_user_list_by_id_list(tenant_id, assignee_id_list)
    notification_to_list =[]
    for notification_to_user_record in notification_to_user_record_list:
        notification_to_list.append(dict(
            user_id=notification_to_user_record.id,
            user_name=notification_to_user_record.name,
            user_email=notification_to_user_record.email,
            user_phone=notification_to_user_record.phone
        ))
    channel_notification_record_list = notification_service_ins.get_notification_record_by_id_list(tenant_id, selected_channel_id_list)
    for channel_notification_record in channel_notification_record_list:
        channel_type = channel_notification_record.type
        if channel_type == 'hook':
            # only support hook for now
            signature, timestamp = common_service_ins.gen_signature_by_token(channel_notification_record.extra.get("hook_token"))
            headers = dict(signature=signature, timestamp=timestamp)
            requests.post(channel_notification_record.extra.get("hook_url"), headers=headers, json=dict(type="flow_notification", title=title_template_format, content=content_template_format, to_list=notification_to_list))
    return True
    

@app.task
def flow_action_hook_task(tenant_id:str, ticket_id: str, event_type:str, workflow_id: str = '', workflow_version_id: str = ''):
    """
    flow action hook task
    :param ticket_id:
    :param action_id:
    :param workflow_id:
    :param workflow_version_id:
    :return:
    """
    # get workflow action hook configure record
    if not ticket_id:
        if event_type == "pre_create":
            if not workflow_id and not workflow_version_id:
                raise CustomCommonException("pre create event require workflow_id and workflow_version_id")
            hook_match_record_list = workflow_hook_service_ins.get_workflow_hook_by_event(tenant_id, workflow_id, workflow_version_id, event_type)
            for hook_match_record in hook_match_record_list:
                hook_url = hook_match_record.url
                hook_token = hook_match_record.token
                signature, timestamp = common_service_ins.gen_signature_by_token(hook_token)
                headers = dict(signature=signature, timestamp=timestamp)
                r = requests.post(hook_url, headers=headers, json=dict(type="flow_action_hook", event_type=event_type))
                if r.json().get("code") != 0:
                    return CustomCommonException(r.json().get("msg"))
        else:
            raise CustomCommonException("ticket id is required for event hook")
    else:
        ticket_record = ticket_base_service_ins.get_ticket_by_id(tenant_id, ticket_id)
        workflow_id = ticket_record.workflow_id
        version_id = ticket_record.workflow_version_id
        hook_match_record_list = workflow_hook_service_ins.get_workflow_hook_by_event(tenant_id, workflow_id, version_id, event_type)
        for hook_match_record in hook_match_record_list:
            hook_url = hook_match_record.url
            hook_token = hook_match_record.token
            signature, timestamp = common_service_ins.gen_signature_by_token(hook_token)
            headers = dict(signature=signature, timestamp=timestamp)
            requests.post(hook_url, headers=headers, json=dict(type="flow_action_hook", event_type=event_type))
    return True
    
