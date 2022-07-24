import datetime, time
from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class TicketRecord(BaseModel):
    """
    Work order record
    """
    title = models.CharField(
        _('title'), max_length=500, blank=True, default='',
        help_text=_("Title of the ticket")
    )
    workflow_id = models.IntegerField(
        _('workflow_id'),
        help_text=_('Associated with workflow.Workflow process')
    )
    sn = models.CharField(
        _('sn'), max_length=25,
        help_text=_("The serial number of the work order")
    )
    state_id = models.IntegerField(
        _('state_id'),
        help_text=_('Associated with workflow.State')
    )
    parent_ticket_id = models.IntegerField(
        _('parent_ticket_id'), default=0,
        help_text=_('Associated with ticket.TicketRecord')
    )
    parent_ticket_state_id = models.IntegerField(
        _('parent_ticket_state_id'), default=0,
        help_text=_('Associated with workflow.State, '
                  'the child work order is related to a certain state of the parent work order'))
    participant_type_id = models.IntegerField(
        _('participant_type_id'), default=0,
        help_text=_('0. No handler, 1. Individual, 2. Multi-person, 3. Department, 4. Role')
    )
    participant = models.CharField(
        _('participant'), max_length=1000, default='', blank=True,
        help_text=_('Can be empty (if there is no handler, such as end status),'
                  ' username\multiple usernames (separated by ,)\department id\role id\script file name, etc.'))
    relation = models.CharField(
        _('relation'), max_length=1000, default='', blank=True,
        help_text=_('All related people (including creators and former to-be-processed people) will be saved during the work order transfer process for querying'))
    in_add_node = models.BooleanField(
        _('in_add_node'), default=False,
        help_text=_('Is it under the sign')
    )
    add_node_man = models.CharField(
        _('add_node_man'), max_length=50, default='', blank=True,
        help_text=_('The person who signed the operation,'
                  ' the current handler of the work order will return to the handler after the processing is completed,'
                  ' and it is only valid when it is in the sign-up state')
    )
    script_run_last_result = models.BooleanField(_('script_run_last_result'), default=True)
    act_state_id = models.IntegerField(
        _('act_state_id'), default=1,
        help_text=_('The progress status of the current work order,'
                  ' see the definition in service.constant_service for details')
    )
    multi_all_person = models.CharField(
        _('multi_all_person'), max_length=1000, default='{}', blank=True,
        help_text=_('The actual processing results when the current state handlers are all processed are required,'
                  ' in json format')
    )


class TicketFlowLog(BaseModel):
    """
    Work ticket flow log
    """
    ticket_id = models.IntegerField(_('ticket_id'))
    transition_id = models.IntegerField(
        _('transition_id'),
        help_text=_(
            'Associated with worklow.Transition,'
            ' when it is 0, it means the operation that is considered to be intervening')
    )
    suggestion = models.CharField(
        _('suggestion'), max_length=10000, default='', blank=True
    )

    participant_type_id = models.IntegerField(
        _('participant_type_id'),
        help_text=_('See definition in service.constant_service')
    )
    participant = models.CharField(_('participant'), max_length=50, default='', blank=True)
    state_id = models.IntegerField(_('state_id'), default=0, blank=True)
    intervene_type_id = models.IntegerField(
        _('intervene_type_id'), default=0,
        help_text=_('See definition in service.constant_service')
    )
    ticket_data = models.CharField(
        _('ticket_data'), max_length=10000, default='', blank=True,
        help_text=_('Can be used to record the current form data, json format')
    )


class TicketCustomField(BaseModel):
    """
    Ticket custom field, the actual value of the ticket custom field.
    """
    name = models.CharField(_('name'), max_length=50)
    field_key = models.CharField(_('field_key'), max_length=50)
    ticket_id = models.IntegerField(_('ticket_id'))
    field_type_id = models.IntegerField(
        _('field_type_id'),
        help_text=_('See definition in service.constant_service')
    )
    char_value = models.CharField(_('char_value'), max_length=1000, default='', blank=True)
    int_value = models.IntegerField(_('int_value'), default=0, blank=True)
    float_value = models.FloatField(_('float_value'), default=0.0, blank=True)
    bool_value = models.BooleanField(_('bool_value'), default=False, blank=True)
    # date_value = models.DateField('日期值', default='0001-01-01', blank=True)
    date_value = models.DateField(_('date_value'), default=datetime.datetime.strptime('0001-01-01', "%Y-%m-%d"),
                                  blank=True)
    # datetime_value = models.DateTimeField('日期时间值', default='0001-01-01 00:00:00', blank=True)
    datetime_value = models.DateTimeField(
        _('datetime_value'), default=datetime.datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        blank=True
    )
    # time_value = models.TimeField('时间值', default='00:00:01', blank=True)
    time_value = models.TimeField(_('time_value'), default=datetime.datetime.strptime('00:00:01', '%H:%M:%S'),
                                  blank=True)
    radio_value = models.CharField(_('radio_value'), default='', max_length=50, blank=True)
    checkbox_value = models.CharField(
        _('checkbox_value'), default='', max_length=50, blank=True,
        help_text=_('commas separate multiple options')
    )
    select_value = models.CharField(_('select_value'), default='', max_length=50, blank=True)
    multi_select_value = models.CharField(_('multi_select'), default='', max_length=50, blank=True,
                                          help_text=_('commas separate multiple options'))
    text_value = models.TextField(_('text_value'), default='', blank=True)
    username_value = models.CharField(_('username_value'), max_length=50, default='', blank=True)
    multi_username_value = models.CharField(
        _('multi_username_value'), max_length=1000, default='', blank=True
    )


class TicketUser(BaseModel):
    """
    Work order relationship person, used to speed up to-do work order and related work order list query
    """
    ticket = models.ForeignKey(
        TicketRecord, to_field='id', db_constraint=False, on_delete=False
    )
    username = models.CharField(_('username'), max_length=100)
    in_process = models.BooleanField(_('in_process'), default=False)
    worked = models.BooleanField(_('worked'), default=False)
