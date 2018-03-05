from django.db import models
from service.common.constant_service import CONSTANT_SERVICE
# Create your models here.


class TicketRecord(models.Model):
    """
    工单记录
    """
    title = models.CharField(u'标题', max_length=50, blank=True, help_text="工单的标题")
    ticket_type_id = models.IntegerField('工单类型', help_text='与TicketType关联')
    workflow_id = models.IntegerField('关联的流程id', help_text='与workflow.Workflow流程关联')
    sn = models.CharField(u'流水号', max_length=25, help_text="工单的流水号")
    default_notice_to = models.CharField('默认通知人', max_length=50, help_text='工单创建和结束时候会将相应信息通知此用户')
    current_state_id = models.IntegerField('当前状态', help_text='与workflow.State关联')
    current_man_type_id = models.IntegerField('当前处理人类型', choices=CONSTANT_SERVICE.CURRENT_MAN_TYPE_CHOICE)
    current_man = models.CharField('当前处理人', max_length=50, default='', blank=True, help_text='当工单结束时候处理人为空')
    is_add_node = models.BooleanField('加签中', default=0, help_text='')
    add_node_next_man = models.CharField('加签完成后处理人', max_length=50, default='', blank=True)
    is_end = models.BooleanField('已结束', default=0)

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False, help_text='')


class TicketType(models.Model):
    """
    工单类型
    """
    name = models.CharField(u'工单类型', max_length=30)
    parent_type_id = models.IntegerField(u'父类型id', default=0, blank=True)
    workflow_id = models.IntegerField('流程id', default=0, blank=True)  # 当有子类型时不需要关联工作流
    # 限制周期({'period':24} 24小时), 限制次数({'count':1}在限制周期内只允许提交1次), 限制级别({'level':1} 针对(1特定用户 2全局)限制周期限制次数)
    # 允许特定人员提交({'allow_person':'zhangsan'}只允许张三提交工单,{'allow_dept':1}只允许部门id的用户提交工单，{'allow_role':1}只允许角色id为1的用户提交工单)
    limit_expression = models.CharField('限制表达式', max_length=100, default='', blank=True)
    default_notice_to = models.CharField('默认通知人', max_length=50, default='', blank=True, help_text='表单创建及结束时会发送相应通知信息')
    description = models.CharField(u'描述', max_length=50, default='', blank=True)
    order_id = models.IntegerField(u'顺序', default=0, help_text='工单类型列表排列顺序')

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False, help_text='删除的工单无允许查看，不允许新建，工单类型中不显示')
    is_abandoned = models.BooleanField(u'已废弃', default=False, help_text='废弃的类型的工单允许查看，不允许创建，工单类型中会显示')


class TicketFlowLog(models.Model):
    """
    工单流转日志
    """
    ticket_id = models.IntegerField('工单id')
    action = models.CharField('动作', max_length=50)
    suggestion = models.CharField('处理意见', max_length=1000, default='', blank=True)
    user_type = models.IntegerField('处理人类型', choices=CONSTANT_SERVICE.HANDLER_TYPE_CHOICE)
    user = models.CharField('处理人', max_length=20)
    current_state_id = models.IntegerField('当前状态', default=0, blank=True)
    related_users = models.CharField('当前相关处理人', max_length=1000, help_text='此状态下所有的有权限的处理人，逗号隔开')
    ticket_data = models.CharField('工单数据', max_length=10000, help_text='用于记录当前表单数据，json格式')

    creator = models.CharField(u'创建人', max_length=100)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class TicketStateLastMan(models.Model):
    """
    记录工单每个状态的最后处理人，用于回退时候定位
    """
    state_id = models.IntegerField('状态id')
    ticket_id = models.IntegerField('工单id')
    user_type_id = models.IntegerField('处理人类型', choices=CONSTANT_SERVICE.HANDLER_TYPE_CHOICE)
    user = models.CharField(u'处理人', max_length=100, default='')
    creator = models.CharField(u'创建人', max_length=100)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)


class TicketCustomField(models.Model):
    """
    工单自定义字段
    """
    name = models.CharField(u'字段名', max_length=50)
    key = models.CharField(u'字段标识', max_length=50)
    ticket_id = models.IntegerField(u'工单id')
    field_type_id = models.IntegerField(u'字段类型', choices=CONSTANT_SERVICE.FIELD_TYPE_CHOICE)
    char_value = models.CharField('字符串值', max_length=1000, default='', blank=True)
    int_value = models.IntegerField('整形值', default=0, blank=True)
    float_value = models.FloatField('浮点值', default=0.0, blank=True)
    bool_value = models.BooleanField('布尔值', default=0, blank=True)
    date_value = models.DateField('日期值', default='0000-00-00', blank=True)
    datetime_value = models.DateTimeField('日期时间值', default='0000-00-00 00:00:00', blank=True)
    time_value = models.TimeField('时间值', default='00:00:00', blank=True)
    radio_value = models.CharField('radio值', default='', max_length=50, blank=True)
    select_value = models.CharField('下拉列表值', default='', max_length=50, blank=True)
    text_value = models.TextField('文本值', default='', blank=True)

    creator = models.CharField(u'创建人', max_length=100)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)
