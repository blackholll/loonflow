import datetime, time
from django.db import models
from apps.loon_base_model import BaseCommonModel
from django.utils.translation import gettext_lazy as _
from apps.workflow.models import Workflow, Node, Transition
from apps.account.models import User


class TicketRecord(BaseCommonModel):
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
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_workflow")
    parent_ticket = models.ForeignKey("self", db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket")
    parent_ticket_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket_node")
    act_state = models.CharField("act state", choices=ACT_STATE_CHOICE)


class TicketNode(BaseCommonModel):
    """
    used for save ticket node data, only node's latest info
    """
    HOOK_STATE_CHOICE = [
        ("", "N/A"),
        ('in_progress', 'IN-PROGRESS'),
        ("success", "SUCCESS"),
        ("failure", "FAILURE")
    ]

    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_ticket")
    node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_node")
    in_add_node = models.BooleanField('in add node status', default=False, help_text='whether in add node status')
    add_node_target = models.CharField('add node target', max_length=500, default='', blank=True)
    hook_state = models.CharField("hook running state", max_length=50, choices=HOOK_STATE_CHOICE)
    all_participant_result = models.JSONField('all participant result', blank=True)


class TicketNodeParticipant(BaseCommonModel):
    """
    ticket node's participant, only runtime info， one user has only one record for one node,
    """
    PARTICIPANT_TYPE_CHOICE = [
        ('', 'none'),
        ('person', 'person'),
        ('hook', 'hook'),
    ]

    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_ticket")
    node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_node")
    participant_type = models.CharField("participant_type", max_length=50, choices=PARTICIPANT_TYPE_CHOICE)
    participant = models.CharField("participant", max_length=50, default='', blank=True)


class TicketFlowHistory(BaseCommonModel):
    """
    ticket;s flow log record
    """
    PARTICIPANT_TYPE_CHOICE = [
        ('', 'none'),
        ('person', 'person'),
        ('hook', 'hook'),
    ]

    FLOW_TYPE_CHOICE = [
        ('create', 'create'),
        ('forward', 'forward'),
        ('countersign', 'countersign'),
        ('countersign_end', 'countersign_end'),
        ('accept', 'accept'),
        ('comment', 'comment'),
        ('delete', 'delete'),
        ('force_close', 'force_close'),
        ('force_alter_node', 'force_alter_node'),
        ('withdraw', 'withdraw'),
        ('hook', 'hook'),
        ('other', 'other')
    ]
    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING)
    transition = models.ForeignKey(Transition, db_constraint=False, on_delete=models.DO_NOTHING)
    comment = models.CharField(_('comment'), max_length=10000, default='', blank=True)

    participant_type = models.CharField(_('participant_type'), max_length=50, choices=PARTICIPANT_TYPE_CHOICE)
    participant = models.CharField(_('participant'), max_length=50, default='', blank=True)
    node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING)
    flow_type = models.CharField("flow type", max_length=50, default="", blank=True)
    ticket_data = models.JSONField(_('ticket_data'), default=dict, blank=True)


class TicketCustomField(BaseCommonModel):
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
    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING)
    field_type = models.CharField("field_type", max_length=50, choices=FIELD_TYPE_CHOICE)

    common_value = models.CharField('common_value', max_length=2000, default='', blank=True)  # for text, select, cascade, user, file
    number_value = models.DecimalField('number', default=0, decimal_places=10, max_digits=20)
    date_value = models.DateField("date value", default="1970-01-01")
    datetime_value = models.DateTimeField('datetime_value', default=datetime.datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
    time_value = models.TimeField('time_value', default=datetime.datetime.strptime('00:00:01', '%H:%M:%S'))
    rich_text_value = models.TextField('rich_text_value', default='')  # for richtext


class TicketUser(BaseCommonModel):
    """
    ticket related user, include as creator, as participant, as processor, as cc recipient
    """
    ticket = models.ForeignKey(TicketRecord, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, db_constraint=False, on_delete=models.DO_NOTHING)
    as_creator = models.BooleanField('as creator', default=False)
    as_participant = models.BooleanField('as participant', default=False)
    as_processor = models.BooleanField('as processor', default=False)
    as_cc_recipient = models.BooleanField('as cc recipient', default=False)
