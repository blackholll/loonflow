from django.db import models
from apps.loon_base_model import BaseCommonModel


class Record(BaseCommonModel):
    """
    workflow record
    """
    pass

class Version(BaseCommonModel):
    """
    version
    """
    TYPE_CHOICE = [
        ('archived', 'archived'),
        ('default', 'default'),
        ('candidate', 'candidate')
    ]
    workflow = models.ForeignKey(Record, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING, related_name='workflow_versions')
    name = models.CharField("name", max_length=50, null=True, blank=True)
    description = models.CharField("description", max_length=500, null=True, blank=True)
    type = models.CharField("type", choices=TYPE_CHOICE, max_length=50, null=True, blank=True)

class BaseWorkflowModel(BaseCommonModel):
    """
    basic workflow model
    """
    version = models.ForeignKey(Version, db_constraint=False, on_delete=models.DO_NOTHING)
    class Meta:
        abstract = True



class BasicInfo(BaseWorkflowModel):
    """
    workflow basic info
    """
    workflow = models.ForeignKey(Record, db_constraint=False, null=False, on_delete=models.DO_NOTHING, related_name='basic_info')
    name = models.CharField("name", max_length=50)
    description = models.CharField("description", max_length=200)

class Notification(BaseWorkflowModel):
    """
    workflow notification
    """
    workflow = models.ForeignKey(Record, db_constraint=False, null=False, on_delete=models.DO_NOTHING)
    channels = models.CharField("workflow_notification", max_length=500, default="", blank=True)
    title_template = models.CharField("title_template", max_length=200, default='', blank=True)
    content_template = models.CharField("content_template", max_length=1000, default='title:{title}, created at:{created_at}')

class Node(BaseWorkflowModel):
    """
    node
    node_field: {"field1": "r", "field2":"rwr", "field3": "rwo"}
    r: readonly, rwm: read, write, must provide, rwo: read, write, option(not required))
    """
    TYPE_CHOICE = [
        ('start', 'start'),
        ('common', 'common'),
        ('end', 'end'),
        ('parallel', 'parallel'), # 平行网关
        ('exclusive', 'exclusive'), # 排他网关
        ('include_gw', 'include_gw'), # 包含网关
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
    workflow = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING)
    type = models.CharField("type", max_length=50, choices=TYPE_CHOICE, default='common')
    layout = models.JSONField("layout")
    props = models.JSONField("props")


class Edge(BaseWorkflowModel):
    """
    edge
    """
    TYPE_CHOICE = [
        ('accept', 'accept'),
        ('reject', 'reject'),
        ('other', 'other')
    ]
    name = models.CharField("name", max_length=50)
    workflow = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_workflow")
    source_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING)
    target_node = models.ForeignKey(Node, db_constraint=False, on_delete=models.DO_NOTHING, related_name="transition_destination")
    type = models.CharField("type", choices=TYPE_CHOICE)
    layout = models.JSONField("layout")
    props = models.JSONField("props")


class Component(BaseWorkflowModel):
    """Component"""
    COMPONENT_TYPE_CHOICE = [
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

    workflow = models.ForeignKey(Record, db_constraint=False, on_delete=models.DO_NOTHING)
    type = models.CharField("type", max_length=50, choices=COMPONENT_TYPE_CHOICE)
    component_key = models.CharField("field_key", max_length=50)
    component_name = models.CharField("component_name", max_length=50)
    parent_component = models.ForeignKey('self', db_constraint=False, null=True, default='0000', on_delete=models.DO_NOTHING)
    description = models.CharField("description", max_length=200, blank=True, default='')
    layout = models.JSONField("layout")
    props = models.JSONField("props")  # unit, option, different field type has different props


class Permission(BaseWorkflowModel):
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
    workflow = models.ForeignKey(Record, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    permission = models.CharField("permission", choices=PERMISSION_CHOICE, max_length=100, null=True, blank=True)
    target_type = models.CharField("target_type", choices=TARGET_TYPE, max_length=100, null=True, blank=True)
    target = models.CharField("target", max_length=100, null=True, blank=True)  # should be user_id/department_id/app_id


class Hook(BaseWorkflowModel):
    """
    hook record
    """
    EVENT_TYPE_CHOICE = [
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
    events = models.CharField("events", max_length=500, null=True, blank=True)
    workflow = models.ForeignKey(Record, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)



