from django.db import models
from apps.loon_base_model import BaseCommonModel


class Workflow(BaseCommonModel):
    """
    workflow record
    """
    name = models.CharField("name", max_length=50)
    description = models.CharField("description", max_length=200)


class WorkflowNotice(BaseCommonModel):
    """
    workflow notice
    """
    workflow = models.ForeignKey(Workflow, db_constraint=False, null=False, on_delete=models.DO_NOTHING)
    notices = models.CharField("workflow_notices", max_length=500, default="", blank=True)
    title_template = models.CharField("title_template", max_length=200, default='', blank=True)  # ',' between notice ids
    content_template = models.CharField("content_template", max_length=1000, default='title:{title}, created at:{created_at}')


class Node(BaseCommonModel):
    """
    node
    node_field: {"field1": "r", "field2":"rwr", "field3": "rwo"}
    r: readonly, rwm: read, write, must provide, rwo: read, write, option(not required))
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
        ('none', 'none'),
        ('person', 'person'),
        ('multi_person', 'multi_person'),
        ('dept', 'dept'),
        ('role', 'role'),
        ('variable', 'variable'),
        ('ticket_field', 'ticket_field'),
        ('parent_ticket_field', 'parent_ticket_field'),
        ('hook', 'hook'),
        ('timer', 'timer'),
        ('from-external', 'from-external')
    ]
    DISTRIBUTE_TYPE_CHOICE = [
        ('voluntary', 'voluntary'),
        ('direct', 'direct'),
        ('random', 'random'),
        ('whole', 'whole')
    ]
    # node field attr: r:read, wo:write option, wr: write require

    name = models.CharField("name", max_length=50)
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)
    type = models.CharField("type", max_length=50, choices=TYPE_CHOICE, default='common')
    allow_retreat = models.BooleanField("allow_retreat", default=False)
    remember_last_participant = models.BooleanField("remember_last_participant", default=False, help_text='ticket to this node will assign to the previous handler if the value is true')
    participant_type = models.CharField("participant_type", max_length=100, choices=PARTICIPANT_TYPE_CHOICE)
    participant = models.CharField("participant", default='', blank=True, max_length=1000, help_text='need support sub-workflow, then you should set the participant as loonflowrobot')
    distribute_type = models.CharField("distribute_type", max_length=50, default='direct', choices=DISTRIBUTE_TYPE_CHOICE)
    node_field = models.JSONField("node_field", default=dict)
    props = models.JSONField("props")


class Transition(BaseCommonModel):
    """
    transition
    """
    TRANSITION_TYPE_CHOICE = [
        ('accept', 'accept'),
        ('reject', 'reject'),
        ('other', 'other')
    ]
    name = models.CharField("name", max_length=50)
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_workflow")
    source_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING)
    destination_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_destination")
    condition_expression = models.CharField("condition_expression", max_length=1000, default='')
    type = models.CharField("transition_type", choices=TRANSITION_TYPE_CHOICE)
    field_require_check = models.BooleanField("field_require_check", default=True, help_text='will check whether all field rule is valid if this attr is true')
    alert_text = models.CharField("alert_text", max_length=200, default='', blank=True)
    props = models.JSONField("props")

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
        ('rich_text', 'rich_text'),
        ('row', 'row'),
        ('col', 'col')
    ]

    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)
    field_type = models.CharField("field_type", max_length=50, choices=FIELD_TYPE_CHOICE)
    field_key = models.CharField("field_key", max_length=50)
    field_name = models.CharField("field_name", max_length=50)
    parent_field = models.ForeignKey('self', db_constraint=False, null=False, default=0, on_delete=models.DO_NOTHING)
    order_id = models.IntegerField("order_id", default=0)  # only for current level's order
    default_value = models.TextField("default_value", null=True, blank=True)
    description = models.CharField("description", max_length=200, blank=True, default='')
    placeholder = models.CharField("placeholder", max_length=200, blank=True, default='')
    props = models.JSONField("props")  # unit, option, different field type has different props


class WorkflowPermission(BaseCommonModel):
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
    permission = models.CharField("permission", choices=PERMISSION_CHOICE, max_length=100, null=True, blank=True)
    target_type = models.CharField("target_type", choices=TARGET_TYPE, max_length=100, null=True, blank=True)
    target = models.CharField("target", max_length=100, null=True, blank=True)  # should be user_id/department_id/app_id


class WorkflowHook(BaseCommonModel):
    """
    hook record
    """
    HOOK_TYPE_CHOICE = [
        ("pre_create", "pre_create"),
        ("create", "create"),
        ("force_close", "force_close"),
        ("normal_end", "normal_end"),
        ("reject", "reject"),
        ("retreat", "retreat"),
    ]
    name = models.CharField("permission", max_length=100, null=True, blank=True)
    description = models.CharField("description", max_length=500, null=True, blank=True)
    url = models.CharField("url", max_length=500, null=True, blank=True)
    token = models.CharField("token", max_length=200, null=True, blank=True)
    types = models.CharField("types", max_length=500, null=True, blank=True)
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)