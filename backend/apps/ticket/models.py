import datetime, time
from django.db import models
from apps.loon_base_model import BaseCommonModel
from django.utils.translation import gettext_lazy as _
from apps.workflow.models import Record as WorkflowRecord, Node as WorkflowNode, Edge, Version as WorkflowVersion
from apps.account.models import User as accountUser


class Record(BaseCommonModel):
    """
    ticket record
    """
    ACT_STATE_CHOICE = [
        ("in_draft", "in-draft"),
        ("on_going", "on-going"),
        ("rejected", "rejected"),
        ("withdrawn", "withdrawn"),
        ("finished", "finished"),
        ("closed", "closed")
    ]

    title = models.CharField(_("title"), max_length=500, blank=True, default="", help_text="ticket's title")
    workflow = models.ForeignKey(WorkflowRecord, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_workflow")
    workflow_version = models.ForeignKey(WorkflowVersion, db_constraint=False, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="ticket_workflow_version")
    parent_ticket = models.ForeignKey("self", db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket", null=True, blank=True)
    parent_ticket_node = models.ForeignKey(WorkflowNode, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket_node", null=True, blank=True)
    act_state = models.CharField("act state", choices=ACT_STATE_CHOICE)
    def get_dict(self):
        base_result_dict = super().get_dict()
        from service.workflow.workflow_base_service import workflow_base_service_ins
        workflow_info = workflow_base_service_ins.get_workflow_basic_info_by_id(self.tenant_id, self.workflow_id, self.workflow_version_id)
        base_result_dict['workflow_info'] = dict(
            id = workflow_info.get('id'),
            name = workflow_info.get('name'),
            description = workflow_info.get('description'),
        )
        return base_result_dict


class Node(BaseCommonModel):
    """
    used for save ticket node data, only node's latest info
    """
    HOOK_STATE_CHOICE = [
        ("", "N/A"),
        ('in_progress', 'IN-PROGRESS'),
        ("success", "SUCCESS"),
        ("failure", "FAILURE")
    ]

    ticket = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_ticket")
    node = models.ForeignKey(WorkflowNode, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_node")
    assignee_type = models.CharField('assignee type', max_length=50, null=True) # user, hook, timer etc.
    assignee = models.CharField('assignee', max_length=2000, default='', null=True) # if user,  joined by ','
    is_active = models.BooleanField('is active', default=True, help_text='whether the node is active')
    in_consult = models.BooleanField('in consult status', default=False, help_text='whether in consult status')
    in_parallel = models.BooleanField('in parallel status', default=False, help_text='whether in parallel status')
    in_accept_wait = models.BooleanField('in accept wait status', default=False, help_text='whether in accept wait status')
    consult_from = models.ForeignKey(accountUser, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_consult_from", null=True)
    consult_target = models.ForeignKey(accountUser, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_consult_target", null=True)
    hook_status = models.CharField("hook running status", max_length=50, null=True, choices=HOOK_STATE_CHOICE)
    parallel_node = models.ForeignKey(WorkflowNode, db_constraint=False, on_delete=models.DO_NOTHING, null=True, related_name="ticket_node_parallel_node")
    all_assignee_result = models.JSONField('all assignee result', blank=True)


class FlowHistory(BaseCommonModel):
    """
    ticket;s flow log record
    """
    PARTICIPANT_TYPE_CHOICE = [
        ('', 'none'),
        ('user', 'user'),
        ('hook', 'hook'),
        ('timer', 'timer'),
    ]

    ACTION_TYPE_CHOICE = [
        ('create', 'create'),
        ('forward', 'forward'),
        ('consult', 'consult'), # 加签
        ('consult_submit', 'consult_submit'), # 加签完成
        ('accept', 'accept'),
        ('comment', 'comment'),
        ('delete', 'delete'),
        ('force_close', 'force_close'),
        ('force_alter_node', 'force_alter_node'),
        ('withdraw', 'withdraw'),
        ('hook', 'hook'),
        ('other', 'other')
    ]
    ticket = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING)
    action_type = models.CharField("action type", max_length=50, choices=ACTION_TYPE_CHOICE, null=True)
    action = models.ForeignKey(Edge, db_constraint=False, on_delete=models.DO_NOTHING, null=True)
    comment = models.CharField(_('comment'), max_length=10000, default='', null=True)

    processor_type = models.CharField(_('processor_type'), max_length=50, choices=PARTICIPANT_TYPE_CHOICE)
    processor = models.CharField(_('processor'), max_length=50, default='', blank=True)
    node = models.ForeignKey(WorkflowNode, db_constraint=False, on_delete=models.DO_NOTHING, null=True)
    ticket_data = models.JSONField(_('ticket_data'), default=dict, blank=True)


class CustomField(BaseCommonModel):
    """
    ticket's custom field
    """
    FIELD_TYPE_CHOICE = [
        ('text', 'text'),
        ('number', 'number'),
        ('date', 'date'),
        ('datetime', 'datetime'),
        ('time', 'time'),
        ('select', 'select'),
        ('cascade', 'cascade'),
        ('user', 'user'),
        ('file', 'file'),
        ('rich_text', 'rich_text')
    ]
    field_key = models.CharField("field_key", max_length=50)
    ticket = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING)
    field_type = models.CharField("field_type", max_length=50, choices=FIELD_TYPE_CHOICE)

    common_value = models.CharField('common_value', max_length=2000, null=True)  # for text, select, cascade, user, file
    number_value = models.DecimalField('number', null=True, decimal_places=10, max_digits=20)
    date_value = models.DateField("date value", null=True)
    datetime_value = models.DateTimeField('datetime_value', null=True)
    time_value = models.TimeField('time_value', null=True)
    rich_text_value = models.TextField('rich_text_value', null=True)  # for richtext


class User(BaseCommonModel):
    """
    ticket related user, include as creator, as assignee(current handle user), as processor(handled user), as cc recipient
    """
    ticket = models.ForeignKey(Record, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_user")
    user = models.ForeignKey(accountUser, db_constraint=False, on_delete=models.DO_NOTHING)
    as_creator = models.BooleanField('as creator', default=False)
    as_assignee = models.BooleanField('as assignee', default=False)
    as_processor = models.BooleanField('as processor', default=False)
    as_cc_recipient = models.BooleanField('as cc recipient', default=False)
    assignee_node_ids = models.CharField('assignee node ids', max_length=2000, default='', blank=True)
