import os
import uuid
from django.db import models
from apps.loon_base_model import BaseCommonModel
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Workflow(BaseCommonModel):
    """
    workflow,
    limit_expression: {"period":24, "period_unit":"hour", "count":1,  "allow_persons":【"xx","ddd"], "allow_depts":["xx","ss"], "allow_roles":["xx"],["yy"],"level":"personal"}

    """
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=50)
    notices = models.CharField(_('notices'), default='', blank=True, max_length=50)
    limit_expression = models.JSONField(_('limit_expression'), max_length=1000, default=dict, blank=True)
    display_form_str = models.CharField(_('display_form_str'), max_length=10000, default='[]', blank=True)
    title_template = models.CharField(_('title_template'), max_length=50, default='', blank=True)
    content_template = models.CharField(_('content_template'), max_length=1000, default='title:{title}, created at:{created_at}')


class Node(BaseCommonModel):
    """
    node
    """
    TYPE_CHOICE = [
        ('start', 'start'),
        ('common', 'common'),
        ('end', 'end'),
        ('parallel_gw', 'parallel_gw'),
        ('mutual_gw', 'mutual_gw'),
        ('include_gw', 'include_gw'),
        ('timer', 'timer')
    ]
    PARTICIPANT_TYPE_CHOICE = [
        ('', 'none'),
        ('person', 'person'),
        ('multi-person', 'multi-person'),
        ('dept', 'dept'),
        ('role', 'role'),
        ('variable', 'variable'),
        ('ticket-field', 'ticket-field'),
        ('parent-ticket-field', 'parent-ticket-field'),
        ('hook', 'hook'),
        ('from-external', 'from-external')
    ]
    DISTRIBUTE_TYPE_CHOICE = [
        ('voluntary', 'voluntary'),
        ('direct', 'direct'),
        ('random', 'random'),
        ('whole', 'whole')
    ]
    name = models.CharField(_('name'), max_length=50)
    workflow_id = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)
    is_hidden = models.BooleanField(_('is_hidden'), default=False)
    order_id = models.IntegerField(_('order_id'), default=0)
    type = models.CharField(_('type'), max_length=50, choices=TYPE_CHOICE, default='common')
    allow_retreat = models.BooleanField(_('allow_retreat'), default=False)
    remember_last_man = models.BooleanField(_('remember_last_man'), default=False, help_text='ticket to this node will assign to the previous handler if the value is true')
    participant_type = models.CharField(_('participant_type'), max_length=100, choices=PARTICIPANT_TYPE_CHOICE)
    participant = models.CharField(_('participant'), default='', blank=True, max_length=1000, help_text='need support sub-workflow, then you should set the participant as loonflowrobot')
    distribute_type = models.CharField(_('distribute_type'), max_length=50, default='direct', choices=DISTRIBUTE_TYPE_CHOICE)
    node_field_str = models.JSONField(_('state_field_str'), default=dict)


class Transition(BaseCommonModel):
    """
    transition
    """
    TRANSITION_TYPE_CHOICE = [
        ('accept', 'accept'),
        ('reject', 'reject'),
        ('other', 'other')
    ]
    name = models.CharField(_('name'), max_length=50)
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_workflow")
    source_node_id = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING)
    destination_node_id = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_destination")
    condition_expression = models.CharField(_('condition_expression'), max_length=1000, default='')
    transition_type = models.IntegerField(_('transition_type'), choices=TRANSITION_TYPE_CHOICE)
    field_require_check = models.BooleanField(_('field_require_check'), default=True, help_text='will check whether all field rule is valid if this attr is true')
    alert_enable = models.BooleanField(_('alert_enable'), default=False)
    alert_text = models.CharField(_('alert_text'), max_length=100, default='', blank=True)


class CustomField(BaseCommonModel):
    """CustomField"""
    FIELD_TYPE_CHOICE = [
        ('text', 'text'),
        ('number', 'number'),
        ('date', 'date'),
        ('time', 'time'),
        ('radio', 'radio'),
        ('checkbox', 'checkbox'),
        ('select', 'select'),
        ('cascade', 'cascade'),
        ('user', 'user'),
        ('file', 'file'),
        ('rich_text', 'rich_text')
    ]
    #

    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)
    field_type = models.CharField(_('field_type'), max_length=50, choices=FIELD_TYPE_CHOICE)
    field_key = models.CharField(_('field_key'), max_length=50)
    field_name = models.CharField(_('field_name'), max_length=50)
    order_id = models.IntegerField(_('order_id'), default=0)
    default_value = models.TextField(_('default_value'), null=True, blank=True, max_length=100)
    description = models.CharField(_('description'), max_length=100, blank=True, default='')
    placeholder = models.TextField(_('placeholder'), max_length=100, blank=True, default='')
    extra = models.JSONField(_('extra')) # unit, option


class CustomNotice(BaseCommonModel):
    """
    custom notice
    """
    NOTICE_TYPE_CHOICE = [
        ('hook', 'hook'),
        ('wecom', 'wecom'),
        ('dingtalk', 'dingtalk'),
        ('feishu', 'feishu')
    ]
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=100, null=True, blank=True)
    type = models.IntegerField(_('type'), choices=NOTICE_TYPE_CHOICE)
    # todo: save config to json

    corp_id = models.CharField('corp_id', max_length=100, null=True, blank=True)
    corp_secret = models.CharField('corp_secret', max_length=100, null=True, blank=True)  # encrypted
    app_key = models.CharField('app_key', max_length=100, null=True, blank=True)
    app_secret = models.CharField('app_secret', max_length=100, null=True, blank=True)  # encrypted

    hook_url = models.CharField('hook url', max_length=100, null=True, blank=True)
    hook_token = models.CharField('hook token', max_length=100, null=True, blank=True)


class WorkflowUserPermission(BaseCommonModel):
    """
    permission record for workflow
    """
    PERMISSION_CHOICE = [
        ('view', 'view'),
        ('intervene', 'intervene'),
        ('admin', 'admin'),
        ('api', 'api')
    ]
    TARGET_TYPE = [
        ('user', 'user'),
        ('dept', 'dept'),
        ('app', 'app')
    ]
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    permission = models.CharField(_('permission'), choices=PERMISSION_CHOICE, max_length=100, null=True, blank=True)
    target_type = models.CharField(_('target_type'), choices=TARGET_TYPE, max_length=100, null=True, blank=True)
    target = models.CharField(_('target'), max_length=100, null=True, blank=True)  # should be user_id/department_id/app_name
