import os
import uuid
from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import ugettext_lazy as _


class Workflow(BaseModel):
    """
    workflow
    """
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=50)
    notices = models.CharField(
        _('notices'), default='', blank=True, max_length=50,
        help_text=_('id in CustomNotice. Comma separates multiple notification methods')
    )
    view_permission_check = models.BooleanField(
        _('view_permission_check'), default=True,
        help_text=_('After opening, only the associated person (creator, former handler) of the work order is allowed to have permission to view the work order')
    )
    limit_expression = models.CharField(
        _('limit_expression'), max_length=1000, default='{}', blank=True,
        help_text=_('Limit period ({"period": 24} 24 hours), limit times ({"count": 1} only allow one submission during the limit period), limit level ({"level": 1} for (1 single user) 2 global) limit the number of cycles, default specific users); allow specific people to submit ({"allow_persons":"zhangsan,lisi"} only allow Zhang San to submit work orders, {"allow_depts":"1,2"} only allow Users with department ids 1 and 2 submit work orders, {"allow_roles":"1,2"} only allows users with role ids 1 and 2 to submit work orders)')
    )
    display_form_str = models.CharField(
        _('display_form_str'), max_length=10000, default='[]', blank=True,
        help_text=_('The default "[]" is used for which fields are displayed when the user only has the corresponding work order viewing permission, the json of the field_key list, such as ["days", "sn"], the built-in special field participant_info.participant_name: current handler information (department name, role name), state.state_name: the state name of the current state, workflow.workflow_name: workflow name')
    )
    title_template = models.CharField(
        _('title_template'), max_length=50, default='You have a to-do ticket: {title}', null=True, blank=True,
        help_text=_('The value of the ticket field can be written into the template as a parameter, '
                  'the format is: You have a to-do ticket: {title}')
    )
    content_template = models.CharField(
        _('content_template'), max_length=1000, default='title:{title}, creation time:{gmt_created}', null=True, blank=True,
        help_text=_('The value of the ticket field can be written into the template as a parameter, the format is: title:{title}, creation time:{gmt_created}')
    )


class WorkflowAdmin(BaseModel):
    """
    Workflow administrator
    """
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=False)
    username = models.CharField(
        _('username'), max_length=100,
        help_text=_('In addition to the super administrator and the creator of the workflow, managers can also directly edit the workflow')
    )


class State(BaseModel):
    """
    Status record, variable support to get through script
    """
    name = models.CharField(_('name'), max_length=50)
    workflow_id = models.IntegerField(_('workflow_id'))
    is_hidden = models.BooleanField(
        _('is_hidden'), default=False,
        help_text=_('When set to True, this state is not displayed in the get ticket step api '
                  '(except when it is currently in this state)')
    )
    order_id = models.IntegerField(
        _('order_id'), default=0,
        help_text=_('When used in the work order step interface, the order of the states on the step (because there is a mesh condition, so the order needs to be set manually), the smaller the value, the higher')
    )
    type_id = models.IntegerField(
        _('type_id'), default=0,
        help_text=('0. Common type 1. Initial state (when creating a new work order, the corresponding fields must be filled in and transition information) 2. End state (the work order in this state cannot be processed again, that is, there is no corresponding transition)')
    )
    enable_retreat = models.BooleanField(
        _('enable_retreat'), default=False,
        help_text=_('After opening, allow the creator of the work order to directly withdraw the work order to the initial state in this state')
    )

    remember_last_man_enable = models.BooleanField(
        _('remember_last_man_enable'), default=False,
        help_text=_('After it is turned on, when reaching this state, it will first check whether someone has processed it in this state before, and if so, the processing person will be the last person who processed it.')
    )
    participant_type_id = models.IntegerField(
        _('participant_type_id'), default=1, blank=True,
        help_text=_('0. No handler, 1. Individual, 2. Multiple people, 3. Department, 4. Role, 5. Variable (supports the creator of the ticket, the leader of the creator), 6. Script, 7. Field content of the ticket (For example, the "test leader" in the form needs to be the username or multiple usernames separated by commas), 8. Field content of the parent work order. Please select type 5 for the initial state, and the participant fills in the creator')
    )
    participant = models.CharField(
        _('participant'), default='', blank=True, max_length=1000,
        help_text=_('Can be empty (if there is no processing person, such as end status),'
                    ' username\multiple usernames (separated by ,)\department id\role id\variable (creator, creator_tl)\id of script record, etc., including sub-workflow The need to set the handler for loonrobot')
    )

    distribute_type_id = models.IntegerField(
        _('distribute_type_id'), default=1,
        help_text=_('1. Take the initiative to take orders (if the current handler actually has multiple people,'
                    ' you need to accept the order before processing)'
                    ' 2. Direct processing (even if the current handler actually has multiple people,'
                    ' it can be processed directly)'
                    ' 3. Random allocation (if the actual number of handlers is actually multiple)'
                    ' If there are multiple people, the system will randomly assign it to one of them)'
                    ' 4. Process all (requires all participants to process it once before entering the next step)')
    )
    state_field_str = models.TextField(
        _('state_field_str'), default='{}',
        help_text=_('json format dictionary storage, including read-write attributes 1: read-only, 2: required, 3: optional. Example: {"created_at":1,"title":2, "sn":1}, built-in special field participant_info .participant_name: current processor information (department name, role name), state.state_name: state name of the current state, workflow.workflow_name: workflow name'))  # json format storage, including read and write attributes 1: read-only, 2: required, 3: optional, 4: not displayed, dictionary of dictionaries
    label = models.CharField(
        _('label'), max_length=1000, default='{}',
        help_text=_('json format, which is determined by the caller according to the actual customization requirements, such as which front-end components need to be displayed in the state: {"components":[{"AppList":1, "ProjectList":7}]}')
    )


class Transition(BaseModel):
    """
    Workflow flow, timer, condition (skip is allowed), conditional flow and timer cannot exist at the same time
    """
    name = models.CharField(_('name'), max_length=50)
    workflow_id = models.IntegerField(_('workflow_id'))
    transition_type_id = models.IntegerField(
        _('transition_type_id'), default=1,
        help_text=_('1. Regular circulation, 2. Timer circulation, you need to set the timer time')
    )  # Not in use, will soon be abandoned
    timer = models.IntegerField(
        _('Timer(seconds)'), default=0,
        help_text=_('The flow type is set to take effect when the timer flows,'
                    ' in seconds. After being in the source state for X seconds, '
                    'if the state has not changed, it will automatically flow to the target state')
    )
    source_state_id = models.IntegerField(_('source_state_id'))
    destination_state_id = models.IntegerField(_('destination_state_id'))
    condition_expression = models.CharField(
        _('condition_expression'), max_length=1000, default='[]',
        help_text=_('The flow condition expression, which determines the next state of the flow according'
                    ' to the conditions in the expression, '
                    'the format is [{"expression":"{days} > 3 and {days}<10", "target_state_id":11}]'
                    ' where { } is used to fill the field key of the work order, '
                    'which will be converted into the actual value during operation. '
                    'When the condition is met, the next state will become the value in target_state_id.'
                    ' The expression only supports simple operations or datetime/time operations.'
                    ' Loonflow will start with the first time The conditions for successful matching shall prevail,'
                    ' so multiple conditions should not conflict')
    )
    attribute_type_id = models.IntegerField(
        _('attribute_type_id'), default=1,
        help_text=_('Attribute Type, 1. Agree, 2. Deny, 3. Other')
    )
    field_require_check = models.BooleanField(
        _('field_require_check'), default=True,
        help_text=_('By default, when the user clicks the operation,'
                    ' the required items of the work order form need to be verified.'
                    ' If it is set to otherwise, it will not be checked.'
                    ' Used for operations such as "return" attributes without filling in form content')
    )
    alert_enable = models.BooleanField(_('alert_enable'), default=False)
    alert_text = models.CharField(_('alert_text'), max_length=100, default='', blank=True)


class CustomField(BaseModel):
    """Custom fields, set which custom fields a workflow has"""
    workflow_id = models.IntegerField(_('workflow_id'))
    field_type_id = models.IntegerField(
        _('field_type_id'),
        help_text=_('5. String, 10. Integer, 15. Float, 20. Boolean, 25. Date, 30. Date Time, 35. Radio box,'
                    ' 40. Multi-select box, 45. Drop-down list, 50. Multi-select drop-down List, 55. Text field, 60. '
                    'Username, 70. Username for multiple selections, 80. '
                    'Attachment (only the path is saved, multiple are separated by commas)')
    )
    field_key = models.CharField(
        _('field_key'), max_length=50,
        help_text=_('Please make the field type as special as possible to avoid conflict with keywords in the system')
    )
    field_name = models.CharField('字段名称', max_length=50)
    order_id = models.IntegerField(
        _('order_id'), default=0,
        help_text=_('The basic fields of the work order are sorted in the form:'
                    ' serial number 0, title 20, status id 40, status name 41, creator 80, creation time 100,'
                    ' update time 120. The form that displays the work order information on the front end '
                    'can be arranged according to this id order')
    )
    default_value = models.CharField(
        _('default_value'), null=True, blank=True, max_length=100,
        help_text=_('When the front end is displayed, this content can be used as the default '
                    'value of the field in the form')
    )
    description = models.CharField(
        _('description'), max_length=100, blank=True, default='',
        help_text=_('Description of the field, which can be used to display '
                    'a detailed description of the field below the field')
    )
    placeholder = models.CharField(
        _('placeholder'), max_length=100, blank=True, default='',
        help_text=_('Displayed as a placeholder for a field in the user ticket details form')
    )
    field_template = models.TextField(
        _('field_template'), default='', blank=True,
        help_text=_('When the text field type field is displayed on the front end,'
                    ' this content can be used as the placeholder of the field')
    )
    boolean_field_display = models.CharField(
        _('boolean_field_display'), max_length=100, default='{}', blank=True,
        help_text=_('When it is a boolean type, it can support a custom display form.'
                    ' {"1":"yes","0":"no"} or {"1":"required","0":"not required"}, note that numbers also need quotes')
    )
    field_choice = models.CharField(
        _('radio, checkbox, select options'), max_length=1000, default='{}', blank=True,
        help_text=_('Options for radio, checkbox, select, multiselect types, '
                    'the format is json such as: {"1":"China", "2":"United States"}, '
                    'note that numbers also need quotation marks')
    )
    label = models.CharField(
        _('label'), max_length=100, blank=True, default='{}',
        help_text=_('Custom label, json format, the caller can handle special scene logic according '
                    'to the label, loonflow only saves the text content')
    )


def upload_workflow_script(instance, filename):
    """
    Because there may be some private information in the script, such as account password, etc.,
    rename the file to avoid downloading the file directly
    :param instance:
    :param filename:
    :return:
    """
    upload_to = 'workflow_script'
    ext = filename.split('.')[-1]
    if ext != 'py':
        raise Exception('Only supports python scripts')
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return os.path.join(upload_to, filename)


class WorkflowScript(BaseModel):
    """
    Script executed in the process
    """
    name = models.CharField(_('name'), max_length=50)
    saved_name = models.FileField(
        _('saved_name'), upload_to=upload_workflow_script,
        help_text=_('Please upload the python script, media/workflow_script/demo_script.py'
                    ' is an example script, please refer to writing'))
    description = models.CharField(_('description'), max_length=100, null=True, blank=True)
    is_active = models.BooleanField(
        _('is_active'), default=True, help_text=_('Actual execution is allowed only when available here')
    )


def upload_notice_script(instance, filename):
    """
    Because there may be some private information in the notification script, such as account password, etc.,
     rename the file to avoid downloading the file directly
    :param instance:
    :param filename:
    :return:
    """
    upload_to = 'notice_script'
    ext = filename.split('.')[-1]
    if ext != 'py':
        raise Exception('Only supports python scripts')
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return os.path.join(upload_to, filename)


class CustomNotice(BaseModel):
    """
    Customize notification methods，hook
    """
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=100, null=True, blank=True)
    type_id = models.IntegerField(
        _('type_id'), default=1, help_text=_('hook, enterprise WeChat message, DingTalk message')
    )

    corpid = models.CharField(_('corpid'), max_length=100, null=True, blank=True)
    corpsecret = models.CharField(_('corpsecret'), max_length=100, null=True, blank=True)
    appkey = models.CharField(_('appkey'), max_length=100, null=True, blank=True)
    appsecret = models.CharField(_('appsecret'), max_length=100, null=True, blank=True)

    hook_url = models.CharField('hook url', max_length=100, null=True, blank=True)
    hook_token = models.CharField('hook token', max_length=100, null=True, blank=True)


class WorkflowUserPermission(BaseModel):
    """
    User, department, and application permissions to operate the workflow. view:
    View the details of the corresponding work order
    (regardless of whether the view permission verification is enabled for the workflow),
    intervene:view+ forcibly modify the permission of the work order status. admin:intervene + can modify the workflow
    """
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=False)
    permission = models.CharField(_('permission'), max_length=100, null=True, blank=True)  # view, intervene， admin, api
    user_type = models.CharField(_('user_type'), max_length=100, null=True, blank=True)  # user, department, app
    user = models.CharField(_('user'), max_length=100, null=True, blank=True)  # username, department_id, app_name
