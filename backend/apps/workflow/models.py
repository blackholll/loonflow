from django.db import models

# Create your models here.


class Workflow(models.Model):
    """
    工作流
    """
    name = models.CharField('名称', max_length=50)
    desc = models.CharField('描述', max_length=50)
    flowchart = models.CharField('流程图', max_length=100, default='', blank=True)
    notice_type = models.CharField('通知方式', max_length=50)  # 逗号隔开: 1,
    initial_state_id = models.IntegerField('初始状态', default=0, blank=True)
    display_form = models.CharField('展现表单', max_length=10000, default='', blank=True)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class State(models.Model):
    """
    状态记录, 变量支持通过脚本获取
    """
    name = models.CharField('名称', max_length=50)
    workflow_id = models.IntegerField('工作流')
    participant_type = models.IntegerField('参与者类型', default=1, blank=True)  # 1.个人 2.职位 3.部门 4.角色 5.变量 6.多人 9.bot
    is_end_state = models.BooleanField('是否为最终状态', default=0)
    participant = models.CharField('参与者', max_length=100)  # 可以为username\多个username(以,隔开)\部门id\角色id\变量id等
    distribute_type = models.IntegerField('接单方式', default=1)  # 1主动接单,2.随机分配,3.全部处理(要求所有参与人都要处理一遍)
    state_field_str = models.TextField('表单字段', default='')  # json格式存储,包括读写属性1：只读，2：必填，3：可选，4：不显示, 字典的字典
    task_dict_info = models.TextField('执行脚本', default='')  # json格式存储,[{'task_name':'a', 'arguments':[1,2]},{'task_name':'b', 'arguments':[3,4]}]

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class Transition(models.Model):
    """
    工作流流转，定时器，条件(允许跳过)， 条件流转与定时器不可同时存在
    """
    name = models.CharField('操作', max_length=50)
    workflow_id = models.IntegerField('工作流id')
    transition_type = models.IntegerField('流转类型', default=1) #常规流转，定时器流转，选择定时器后需要设置定时fa器时间，同时不得设置条件，不得设置弹窗信息
    source_state_id = models.IntegerField('源状态id')
    destination_state_id = models.IntegerField('目的状态id')
    enable_condition = models.BooleanField('开启条件流转', default=0)
    condition = models.CharField('条件表达式', max_length=1000, default='')  # {condition1:state1, condition2:state2}.如{'aaa<10':2, 'aaa>10':3}

    enable_alert = models.BooleanField('点击弹窗提示', default=0)
    alert_text = models.CharField('弹窗内容', max_length=100, default='')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class CustomField(models.Model):
    """自定义字段"""

    FIELD_TYPE_CHOICE = (
        (5, '字符串'),
        (10, '整型'),
        (15, '浮点型'),
        (20, '布尔'),
        (25, '日期'),
        (30, '日期时间'),
        (35, 'radio'),
        (40, '下拉列表'),
        (45, '文本域'),
        (50, '用户名'))

    workflow_id = models.IntegerField('工作流id')
    field_type_id = models.IntegerField('类型', choices=FIELD_TYPE_CHOICE)
    key = models.CharField('字段标识', max_length=50)
    name = models.CharField('字段名称', max_length=50)
    order_id = models.IntegerField('排序', default=0)
    default_value = models.CharField('默认值', null=True, blank=True, max_length=100)
    desc = models.CharField('描述', max_length=100)
    multi_enable = models.BooleanField('允许多选', default=False)
    field_template = models.TextField('模板', default='', blank=True, null=True, help_text='文本域字段支持配置内容模板')
    boolean_field_display = models.CharField('布尔类型显示名', max_length=100, null=True, blank=True,
                                             help_text='当为布尔类型时候，可以支持自定义显示形式。{1:"是",0:"否"}或{1:"需要",0:"不需要"}')
    radio_field_choice = models.CharField('radio选项', max_length=500, null=True, blank=True,
                                          help_text='radio类型可供选择的选项，格式为json如:{1:"中国",2:"美国"}')
    select_field_choice = models.CharField('下拉列表选项', max_length=500, null=True, blank=True,
                                           help_text='下拉列表类型类型可供选择的选项，格式为json如:{1:"中国",2:"美国"}')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class WorkflowScript(models.Model):
    """
    流程中执行的脚本
    """
    name = models.CharField('名称', max_length=50)
    saved_name = models.CharField('存储的文件名', max_length=50)
    desc = models.CharField('描述', max_length=100, null=True, blank=True)
    is_active = models.BooleanField('可用', default=True)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class CustomNotice(models.Model):
    """
    自定义通知方式，初始化邮件方式
    """
    name = models.CharField('名称', max_length=50)
    desc = models.CharField('描述', max_length=100, null=True, blank=True)
    script = models.FileField('通知脚本', upload_to='notice_script', null=True, blank=True)
    title_template = models.CharField('标题模板', max_length=50, null=True, blank=True)  # 如果为空就按照默认模板生成
    content_template = models.CharField('内容模板', max_length=1000, null=True, blank=True)  # 如果为空就按照默认模板生成

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)
