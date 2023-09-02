import datetime, time
from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.workflow.models import Workflow, Node, Transition
from apps.account.models import LoonUser


class TicketRecord(BaseModel):
    """
    ticket record
    """
    HOOK_STATUS_CHOICE = [
        ("", "N/A"),
        ('start', 'START'),
        ("success", "SUCCESS"),
        ("fail", "FAIL")
    ]
    title = models.CharField(_("title"), max_length=500, blank=True, default="", help_text="ticket's title")
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_workflow")
    parent_ticket = models.ForeignKey("self", db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket")
    parent_ticket_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_parent_ticket_node")

    participant_type_id = models.IntegerField('participant type id', default=0, help_text='0.none,1.personal,2.multi,3.department,4.role')
    participant = models.CharField('当前处理人', max_length=1000, default='', blank=True, help_text='可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\部门id\角色id\脚本文件名等')
    in_add_node = models.BooleanField('加签状态中', default=False, help_text='是否处于加签状态下')
    add_node_man = models.CharField('加签人', max_length=50, default='', blank=True, help_text='加签操作的人，工单当前处理人处理完成后会回到该处理人，当处于加签状态下才有效')
    hook_status = models.CharField("hook执行状态", choices=HOOK_STATUS_CHOICE)
    act_state_id = models.IntegerField('进行状态', default=1, help_text='当前工单的进行状态,详见service.constant_service中定义')
    multi_all_person = models.CharField('全部处理的结果', max_length=1000, default='{}', blank=True, help_text='需要当前状态处理人全部处理时实际的处理结果，json格式')


class TicketNode(BaseModel):
    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_ticket")
    node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="ticket_node_node")


class TicketFlowLog(BaseModel):
    """
    ticket;s flow log record
    """
    PARTICIPANT_TYPE_CHOICE = [
        ('', 'none'),
        ('person', 'person'),
        ('hook', 'hook'),
    ]

    FLOW_TYPE_CHOICE = [
        ('forward', 'forward'),
        ('countersign', 'countersign'),
        ('countersign_end', 'countersign_end'),
        ('accept', 'accept'),
        ('comment', 'comment'),
        ('delete', 'delete'),
        ('force_close', 'force_close'),
        ('force_alter_node', 'force_alter_node'),
        ('retreat', 'retreat'),
        ('hook', 'hook')
    ]
    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING)
    transition = models.ForeignKey(Transition, db_constraint=False, on_delete=models.DO_NOTHING)
    comment = models.CharField(_('comment'), max_length=10000, default='', blank=True)

    participant_type = models.CharField(_('participant_type'), choices=PARTICIPANT_TYPE_CHOICE)
    participant = models.CharField(_('participant'), max_length=50, default='', blank=True)
    node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING)
    flow_type = models.IntegerField(_('flow_type'), default=0, help_text='见service.constant_service中定义')
    ticket_data = models.JSONField(_('ticket_data'), default=dict, blank=True)


class TicketCustomField(BaseModel):
    """
    ticket's custom field
    """
    FIELD_TYPE_CHOICE = [
        ('text', 'text'),
        ('number', 'number'),
        ('decimal', 'decimal'),
        ('date', 'date'),
        ('datetime', 'datetime'),
        ('select', 'select'),
        ('cascade', 'cascade'),
        ('user', 'user'),
        ('file', 'file'),
        ('rich_text', 'rich_text')
    ]
    name = models.CharField("name", max_length=50)
    field_key = models.CharField(_("field_key"), max_length=50)
    ticket = models.ForeignKey(TicketRecord, db_constraint=False, on_delete=models.DO_NOTHING)
    field_type = models.CharField(_("field_type"), choices=FIELD_TYPE_CHOICE)
    common_value = models.CharField('common_value', max_length=5000, default='', blank=True) # for string, select, cascade, user, file
    number_value = models.DecimalField('number', default=0, decimal_places=10, max_digits=20, blank=True)
    datetime_value = models.DateTimeField('datetime_value', default=datetime.datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), blank=True)
    time_value = models.TimeField('time_value', default=datetime.datetime.strptime('00:00:01', '%H:%M:%S'), blank=True)
    rich_text_value = models.TextField('rich_text_value', default='', blank=True)  # for richtext


class TicketUser(BaseModel):
    """
    ticket related user
    """
    ticket = models.ForeignKey(TicketRecord, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    username = models.ForeignKey(LoonUser, db_constraint=False, on_delete=models.DO_NOTHING)
    in_process = models.BooleanField('in_process', default=False)
    processed = models.BooleanField('processed', default=False)
