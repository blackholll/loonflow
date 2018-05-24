import datetime, time
from django.db import models
from service.common.constant_service import CONSTANT_SERVICE
# Create your models here.


class TicketRecord(models.Model):
    """
    工单记录
    """
    title = models.CharField(u'标题', max_length=50, blank=True, default='', help_text="工单的标题")
    workflow_id = models.IntegerField('关联的流程id', help_text='与workflow.Workflow流程关联')
    sn = models.CharField(u'流水号', max_length=25, help_text="工单的流水号")
    state_id = models.IntegerField('当前状态', help_text='与workflow.State关联')
    parent_ticket_id = models.IntegerField('父工单id', default=0, help_text='与ticket.TicketRecord关联')
    parent_ticket_state_id = models.IntegerField('对应父工单状态id', default=0, help_text='与workflow.State关联,子工单是关联到父工单的某个状态下的')
    participant_type_id = models.IntegerField('当前处理人类型', default=0, help_text='0.无处理人,1.个人,2.多人,3.部门,4.角色')
    participant = models.CharField('当前处理人', max_length=100, default='', blank=True, help_text='可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\部门id\角色id\脚本文件名等')
    relation = models.CharField('工单关联人', max_length=1000, default='', blank=True, help_text='工单流转过程中将保存所有相关的人(包括创建人、曾经的待处理人)，用于查询')
    in_add_node = models.BooleanField('加签状态中', default=False, help_text='是否处于加签状态下')
    add_node_man = models.CharField('加签人', max_length=50, default='', blank=True, help_text='加签操作的人，工单当前处理人处理完成后会回到该处理人，当处于加签状态下才有效')

    creator = models.CharField('创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = '工单记录'


class TicketFlowLog(models.Model):
    """
    工单流转日志
    """
    ticket_id = models.IntegerField('工单id')
    transition_id = models.IntegerField('流转id', help_text='与worklow.Transition关联， 为0时表示认为干预的操作')
    suggestion = models.CharField('处理意见', max_length=1000, default='', blank=True)

    participant_type_id = models.IntegerField('处理人类型', help_text='见service.constant_service中定义')
    participant = models.CharField('处理人', max_length=50, default='', blank=True)
    state_id = models.IntegerField('当前状态id', default=0, blank=True)
    intervene_type_id = models.IntegerField('干预类型', default=0, help_text='0.非人为干预的流转，1.转交操作 2.加签操作 3.加签处理完成')
    ticket_data = models.CharField('工单数据', max_length=10000, default='', blank=True, help_text='可以用于记录当前表单数据，json格式')

    creator = models.CharField(u'创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)

    class Meta:
        verbose_name = '工单流转日志'
        verbose_name_plural = '工单流转日志'


class TicketStateLastMan(models.Model):
    """
    记录工单每个状态的最后处理人，用于回退时候定位到上次处理的人
    """
    state_id = models.IntegerField('状态id')
    ticket_id = models.IntegerField('工单id')
    participant_type_id = models.IntegerField('处理人类型', help_text='见service.constant_service中定义')
    participant = models.CharField(u'处理人', max_length=100, default='')

    creator = models.CharField(u'创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)

    class Meta:
        verbose_name = '工单状态处理人'
        verbose_name_plural = '工单状态处理人'


class TicketCustomField(models.Model):
    """
    工单自定义字段， 工单自定义字段实际的值。
    """
    name = models.CharField(u'字段名', max_length=50)
    field_key = models.CharField(u'字段标识', max_length=50)
    ticket_id = models.IntegerField(u'工单id')
    field_type_id = models.IntegerField(u'字段类型', help_text='见service.constant_service中定义')
    char_value = models.CharField('字符串值', max_length=1000, default='', blank=True)
    int_value = models.IntegerField('整形值', default=0, blank=True)
    float_value = models.FloatField('浮点值', default=0.0, blank=True)
    bool_value = models.BooleanField('布尔值', default=False, blank=True)
    # date_value = models.DateField('日期值', default='0001-01-01', blank=True)
    date_value = models.DateField('日期值', default=datetime.datetime.strptime('0001-01-01', "%Y-%m-%d"), blank=True)
    # datetime_value = models.DateTimeField('日期时间值', default='0001-01-01 00:00:00', blank=True)
    datetime_value = models.DateTimeField('日期时间值', default=datetime.datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), blank=True)
    # time_value = models.TimeField('时间值', default='00:00:01', blank=True)
    time_value = models.TimeField('时间值', default=datetime.datetime.strptime('00:00:01','%H:%M:%S'), blank=True)
    radio_value = models.CharField('radio值', default='', max_length=50, blank=True)
    checkbox_value = models.CharField('checkbox值', default='', max_length=50, blank=True, help_text='逗号隔开多个选项')
    select_value = models.CharField('下拉列表值', default='', max_length=50, blank=True)
    multi_select_value = models.CharField('多选下拉列表值', default='', max_length=50, blank=True, help_text='逗号隔开多个选项')
    text_value = models.TextField('文本值', default='', blank=True)
    username_value = models.CharField('用户名', max_length=50, default='', blank=True)
    multi_username_value = models.CharField('多选用户名', max_length=1000, default='', blank=True)

    creator = models.CharField(u'创建人', max_length=50, default='admin')
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)

    class Meta:
        verbose_name = '工单自定义字段'
        verbose_name_plural = '工单自定义字段'
