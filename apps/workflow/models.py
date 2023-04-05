import os
import uuid
from django.db import models
from apps.loon_base_model import BaseModel


class Workflow(BaseModel):
    """
    工作流
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=50)
    notices = models.CharField('通知', default='', blank=True, max_length=50, help_text='CustomNotice中的id.逗号隔开多个通知方式')
    view_permission_check = models.BooleanField('查看权限校验', default=True, help_text='开启后，只允许工单的关联人(创建人、曾经的处理人)有权限查看工单')
    limit_expression = models.CharField('限制表达式', max_length=1000, default='{}', blank=True, help_text='限制周期({"period":24} 24小时), 限制次数({"count":1}在限制周期内只允许提交1次), 限制级别({"level":1} 针对(1单个用户 2全局)限制周期限制次数,默认特定用户);允许特定人员提交({"allow_persons":"zhangsan,lisi"}只允许张三提交工单,{"allow_depts":"1,2"}只允许部门id为1和2的用户提交工单，{"allow_roles":"1,2"}只允许角色id为1和2的用户提交工单)')
    display_form_str = models.CharField('展现表单字段', max_length=10000, default='[]', blank=True, help_text='默认"[]"，用于用户只有对应工单查看权限时显示哪些字段,field_key的list的json,如["days","sn"],内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称')
    title_template = models.CharField('标题模板', max_length=50, default='你有一个待办工单:{title}', null=True, blank=True, help_text='工单字段的值可以作为参数写到模板中，格式如：你有一个待办工单:{title}')
    content_template = models.CharField('内容模板', max_length=1000, default='标题:{title}, 创建时间:{gmt_created}', null=True, blank=True, help_text='工单字段的值可以作为参数写到模板中，格式如：标题:{title}, 创建时间:{gmt_created}')


class WorkflowAdmin(BaseModel):
    """
    工作流管理员, 该model已经废弃， 当前使用的是WorkflowUserPermission
    """
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    username = models.CharField('管理员', max_length=100, help_text='除超级管理员及该工作流创建人外，管理人员也可以直接编辑该工作流')


class State(BaseModel):
    """
    状态记录, 变量支持通过脚本获取
    """
    name = models.CharField('名称', max_length=50)
    workflow_id = models.IntegerField('工作流')
    is_hidden = models.BooleanField('是否隐藏', default=False, help_text='设置为True时,获取工单步骤api中不显示此状态(当前处于此状态时除外)')
    order_id = models.IntegerField('状态顺序', default=0, help_text='用于工单步骤接口时，step上状态的顺序(因为存在网状情况，所以需要人为设定顺序),值越小越靠前')
    type_id = models.IntegerField('状态类型id', default=0, help_text='0.普通类型 1.初始状态(用于新建工单时,获取对应的字段必填及transition信息) 2.结束状态(此状态下的工单不得再处理，即没有对应的transition)')
    enable_retreat = models.BooleanField('允许撤回', default=False, help_text='开启后允许工单创建人在此状态直接撤回工单到初始状态')

    remember_last_man_enable = models.BooleanField('记忆最后处理人', default=False, help_text='开启后，到达此状态时会先检查之前是否有人在此状态处理过，如果有则处理人为最后一次处理的人')
    participant_type_id = models.IntegerField('参与者类型id', default=1, blank=True, help_text='0.无处理人,1.个人,2.多人,3.部门,4.角色,5.变量(支持工单创建人,创建人的leader),6.脚本(已废弃),7.工单的字段内容(如表单中的"测试负责人"，需要为用户名或者逗号隔开的多个用户名),8.父工单的字段内容,10.hook,11.外部获取。 初始状态请选择类型5，参与人填creator')
    participant = models.CharField('参与者', default='', blank=True, max_length=1000, help_text='可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\部门id\角色id\变量(creator,creator_tl)\脚本记录的id等，包含子工作流的需要设置处理人为loonrobot')

    distribute_type_id = models.IntegerField('分配方式', default=1, help_text='1.主动接单(如果当前处理人实际为多人的时候，需要先接单才能处理) 2.直接处理(即使当前处理人实际为多人，也可以直接处理) 3.随机分配(如果实际为多人，则系统会随机分配给其中一个人) 4.全部处理(要求所有参与人都要处理一遍,才能进入下一步)')
    state_field_str = models.TextField('表单字段', default='{}', help_text='json格式字典存储,包括读写属性1：只读，2：必填，3：可选. 示例：{"created_at":1,"title":2, "sn":1}, 内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称')  # json格式存储,包括读写属性1：只读，2：必填，3：可选，4：不显示, 字典的字典
    label = models.CharField('状态标签', max_length=1000, default='{}', help_text='json格式，由调用方根据实际定制需求自行确定,如状态下需要显示哪些前端组件:{"components":[{"AppList":1, "ProjectList":7}]}')


class Transition(BaseModel):
    """
    工作流流转，定时器，条件(允许跳过)， 条件流转与定时器不可同时存在
    """
    name = models.CharField('操作', max_length=50)
    workflow_id = models.IntegerField('工作流id')
    transition_type_id = models.IntegerField('流转类型', default=1, help_text='1.常规流转，2.定时器流转,需要设置定时器时间')  # 未在使用，即将废弃
    timer = models.IntegerField('定时器(单位秒)', default=0, help_text='流转类型设置为定时器流转时生效,单位秒。处于源状态X秒后如果状态都没有过变化则自动流转到目标状态')
    source_state_id = models.IntegerField('源状态id')
    destination_state_id = models.IntegerField('目的状态id')
    condition_expression = models.CharField('条件表达式', max_length=1000, default='[]', help_text='流转条件表达式，根据表达式中的条件来确定流转的下个状态，格式为[{"expression":"{days} > 3 and {days}<10", "target_state_id":11}] 其中{}用于填充工单的字段key,运算时会换算成实际的值，当符合条件下个状态将变为target_state_id中的值,表达式只支持简单的运算或datetime/time运算.loonflow会以首次匹配成功的条件为准，所以多个条件不要有冲突' )
    attribute_type_id = models.IntegerField('属性类型', default=1, help_text='属性类型，1.同意，2.拒绝，3.其他')
    field_require_check = models.BooleanField('是否校验必填项', default=True, help_text='默认在用户点击操作的时候需要校验工单表单的必填项,如果设置为否则不检查。用于如"退回"属性的操作，不需要填写表单内容')
    alert_enable = models.BooleanField('点击弹窗提示', default=False)
    alert_text = models.CharField('弹窗内容', max_length=100, default='', blank=True)


class CustomField(BaseModel):
    """自定义字段, 设定某个工作流有哪些自定义字段"""
    workflow_id = models.IntegerField('工作流id')
    field_type_id = models.IntegerField('类型', help_text='5.字符串，10.整形，15.浮点型，20.布尔，25.日期，30.日期时间，35.单选框，40.多选框，45.下拉列表，50.多选下拉列表，55.文本域，60.用户名, 70.多选的用户名, 80.附件(只保存路径，多个使用逗号隔开)')
    field_key = models.CharField('字段标识', max_length=50, help_text='字段类型请尽量特殊，避免与系统中关键字冲突')
    field_name = models.CharField('字段名称', max_length=50)
    order_id = models.IntegerField('排序', default=0, help_text='工单基础字段在表单中排序为:流水号0,标题20,状态id40,状态名41,创建人80,创建时间100,更新时间120.前端展示工单信息的表单可以根据这个id顺序排列')
    default_value = models.CharField('默认值', null=True, blank=True, max_length=100, help_text='前端展示时，可以将此内容作为表单中的该字段的默认值')
    description = models.CharField('描述', max_length=100, blank=True, default='', help_text='字段的描述信息，可用于显示在字段的下方对该字段的详细描述')
    placeholder = models.CharField('占位符', max_length=100, blank=True, default='', help_text='用户工单详情表单中作为字段的占位符显示')
    field_template = models.TextField('文本域模板', default='', blank=True, help_text='文本域类型字段前端显示时可以将此内容作为字段的placeholder')
    boolean_field_display = models.CharField('布尔类型显示名', max_length=100, default='{}', blank=True,
                                             help_text='当为布尔类型时候，可以支持自定义显示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意数字也需要引号')
    field_choice = models.CharField('radio、checkbox、select的选项', max_length=1000, default='{}', blank=True,
                                    help_text='radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{"1":"中国", "2":"美国"},注意数字也需要引号')
    label = models.CharField('标签', max_length=100, blank=True, default='{}', help_text='自定义标签，json格式，调用方可根据标签自行处理特殊场景逻辑，loonflow只保存文本内容')


def upload_workflow_script(instance, filename):
    """
    因为脚本中可能会存在一些私密信息，如账号密码等，所以重命名文件，避免可以直接下载此文件。已经废弃，不再支持脚本方式的notice,请使用hook
    :param instance:
    :param filename:
    :return:
    """
    upload_to = 'workflow_script'
    ext = filename.split('.')[-1]
    if ext != 'py':
        raise Exception('只支持python脚本')
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return os.path.join(upload_to, filename)


class WorkflowScript(BaseModel):
    """
    流程中执行的脚本, 已经废弃，不再支持脚本方式的notice,请使用hook
    """
    name = models.CharField('名称', max_length=50)
    saved_name = models.FileField('存储的文件名', upload_to=upload_workflow_script, help_text='请上传python脚本,media/workflow_script/demo_script.py为示例脚本，请参考编写')
    description = models.CharField('描述', max_length=100, null=True, blank=True)
    is_active = models.BooleanField('可用', default=True, help_text='此处可用时，才允许实际执行')


def upload_notice_script(instance, filename):
    """
    因为通知脚本中可能会存在一些私密信息，如账号密码等，所以重命名文件，避免可以直接下载此文件。 已经废弃，不再支持脚本方式的notice,请使用hook
    :param instance:
    :param filename:
    :return:
    """
    upload_to = 'notice_script'
    ext = filename.split('.')[-1]
    if ext != 'py':
        raise Exception('只支持python脚本')
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return os.path.join(upload_to, filename)


class CustomNotice(BaseModel):
    """
    自定义通知方式，hook
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, null=True, blank=True)
    type_id = models.IntegerField('类型', default=1, help_text='hook,企业微信消息,钉钉消息')

    corpid = models.CharField('企微corpid', max_length=100, null=True, blank=True)
    corpsecret = models.CharField('企微corpsecret', max_length=100, null=True, blank=True)
    appkey = models.CharField('钉钉appkey', max_length=100, null=True, blank=True)
    appsecret = models.CharField('钉钉appsecret', max_length=100, null=True, blank=True)

    hook_url = models.CharField('hook url', max_length=100, null=True, blank=True)
    hook_token = models.CharField('hook token', max_length=100, null=True, blank=True)


class WorkflowUserPermission(BaseModel):
    """
    用户，部门，应用对工作流的操作权限。 view: 查看对应工单详情(不管该工作流是否开启查看权限校验)，intervene:view+强制修改工单状态的权限。 admin:intervene + 可以修改工作流
    """
    workflow = models.ForeignKey(Workflow, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    permission = models.CharField('权限', max_length=100, null=True, blank=True)  # view, intervene， admin, api
    user_type = models.CharField('用户类型', max_length=100, null=True, blank=True)  # user, department, app
    user = models.CharField('用户', max_length=100, null=True, blank=True)  # username, department_id, app_name
