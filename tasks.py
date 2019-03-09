# from __future__ import absolute_import, unicode_literals
import contextlib
import os
import sys
import traceback
import logging
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
import django
django.setup()

app = Celery('loonflow')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


from apps.ticket.models import TicketRecord
from apps.workflow.models import Transition, State, WorkflowScript, Workflow, CustomNotice
from service.account.account_base_service import AccountBaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.ticket.ticket_base_service import TicketBaseService
from django.conf import settings

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

logger = logging.getLogger('django')



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def test_task(a, b):
    print('a:', a)
    print('b:', b)
    print(a+b)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        try:
            # for python2
            stdout = StringIO.StringIO()
        except Exception:
            stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.task
def run_flow_task(ticket_id, script_name, state_id, action_from='loonrobot'):
    """
    执行工作流脚本
    :param script_name:
    :param ticket_id:
    :param state_id:
    :param action_from:
    :return:
    """
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
    if ticket_obj.participant == script_name and ticket_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
        ## 校验脚本是否合法
        script_obj = WorkflowScript.objects.filter(saved_name='workflow_script/{}'.format(script_name), is_deleted=False, is_active=True).first()
        if not script_obj:
            return False, '脚本未注册或非激活状态'

        script_dir = os.path.join(settings.MEDIA_ROOT, "workflow_script")

        script_file = os.path.join(script_dir, script_name)
        globals = {'ticket_id': ticket_id, 'action_from': action_from}
        # 如果需要脚本执行完成后，工单不往下流转(也就脚本执行失败或调用其他接口失败的情况)，需要在脚本中抛出异常
        try:
            with stdoutIO() as s:
                # execfile(script_file, globals)  # for python 2
                exec(open(script_file).read(), globals)
            script_result = True
            # script_result_msg = ''.join(s.buflist)
            script_result_msg = ''.join(s.getvalue())
        except Exception as e:
            logger.error(traceback.format_exc())
            script_result = False
            script_result_msg = e.__str__()

        logger.info('*' * 20 + '工作流脚本回调,ticket_id:[%s]' % ticket_id + '*' * 20)
        logger.info('*******工作流脚本回调，ticket_id:{}*****'.format(ticket_id))

        # 因为上面的脚本执行时间可能会比较长，为了避免db session失效，重新获取ticket对象
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
        # 新增处理记录,脚本后只允许只有一个后续直连状态
        transition_obj = Transition.objects.filter(source_state_id=state_id, is_deleted=False).first()
        new_ticket_flow_dict = dict(ticket_id=ticket_id, transition_id=transition_obj.id,
                                    suggestion=script_result_msg, participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT,
                                    participant=script_name, state_id=state_id, creator='loonrobot')

        TicketBaseService.add_ticket_flow_log(new_ticket_flow_dict)
        if not script_result:
            # 脚本执行失败，状态不更新,标记任务执行结果
            ticket_obj.script_run_last_result = False
            ticket_obj.save()
            return False, script_result_msg
        # 自动执行流转
        tar_state_obj = State.objects.filter(id=transition_obj.destination_state_id, is_deleted=False).first()
        if tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if tar_state_obj.participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = ticket_obj.creator
            elif tar_state_obj.participant == 'creator_tl':
                approver, msg = AccountBaseService.get_user_dept_approver(ticket_obj.creator)
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                else:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = approver
        elif tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            destination_participant, msg = TicketBaseService.get_ticket_field_value(ticket_id, tar_state_obj.participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id =  CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
        elif tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            parent_ticket_id = ticket_obj.parent_ticket_id
            destination_participant, msg = TicketBaseService.get_ticket_field_value(parent_ticket_id, tar_state_obj.participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
        else:
            # 其他类型不换算成实际的处理人
            destination_participant_type_id = tar_state_obj.participant_type_id
            destination_participant = tar_state_obj.participant

        ticket_obj.participant = destination_participant
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.state_id = tar_state_obj.id
        ticket_obj.save()

        add_relation, msg = TicketBaseService.get_ticket_dest_relation(destination_participant_type_id, destination_participant)
        if add_relation:
            new_relation, msg = TicketBaseService.add_ticket_relation(ticket_id, add_relation)  # 更新关系人信息

        logger.info('******脚本执行成功,工单基础信息更新完成, ticket_id:{}******'.format(ticket_id))

        # 子工单处理
        if tar_state_obj.type_id == CONSTANT_SERVICE.STATE_TYPE_END:
            if ticket_obj.parent_ticket_id:
                sub_ticket_queryset = TicketRecord.objects.filter(parent_ticket_id=ticket_obj.parent_ticket_id, is_deleted=False)
                sub_ticket_state_id_list = []
                for sub_ticket_query0 in sub_ticket_queryset:
                    sub_ticket_state_id_list.append(sub_ticket_query0.state_id)
                if set(sub_ticket_state_id_list) == set([ticket_obj.state_id]):
                    # 父工单的所有子工单都已处理结束,自动流转父工单
                    parent_ticket_obj = TicketRecord.objects.filter(id=ticket_obj.parent_ticket_id, is_deleted=False).first()
                    parent_transition_obj = Transition.object.filter(source_state_id=parent_ticket_obj.state_id, is_deleted=False).first()
                    flag, msg = TicketBaseService.handle_ticket(parent_ticket_obj.id, dict(username='loonrobot', suggestion='所有子工单都已结束，自动流转',
                                                                               transition_id=parent_transition_obj.id))
                    if not flag:
                        return True, msg
        # 下个状态也是脚本处理
        if tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            run_flow_task.apply_async(args=[ticket_id, tar_state_obj.participant, tar_state_obj.id], queue='loonflow')
        return True, ''
    else:
        return False, '工单当前处理人为非脚本，不执行脚本'


@app.task
def timer_transition(ticket_id, state_id, date_time, transition_id):
    """
    定时器流转
    :param ticket_id:
    :param state_id:
    :param date_time:
    :param transition_id:
    :return:
    """
    # 需要满足工单此状态后续无其他操作才自动流转
    # 查询该工单此状态所有操作
    flow_log_set, msg = TicketBaseService().get_ticket_flow_log(ticket_id, per_page=1000)
    for flow_log in flow_log_set:
        if flow_log.state_id == state_id and flow_log.gmt_created > date_time:
            return True, '后续有操作，定时器失效'
    # 执行流转
    handle_ticket_data = dict(transition_id=transition_id, username='loonrobot', suggestion='定时器流转')
    TicketBaseService().handle_ticket(ticket_id, handle_ticket_data, True)


@app.task
def send_ticket_notice(ticket_id):
    """
    发送工单通知
    :param ticket_id:
    :return:
    """
    # 获取工单信息
    # 获取工作流信息，获取工作流的通知信息
    # 获取通知信息的标题和内容模板
    # 将通知内容，通知标题，通知人，作为变量传给通知脚本
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
    if not ticket_obj:
        return False, 'ticket is not exist or has been deleted'
    if ticket_obj.participant_type_id not in (CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL, CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI):
        # 个人及多人的情况才需要发送通知
        return True, 'participant is not people, do not need notice'
    workflow_id = ticket_obj.workflow_id
    workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0).first()
    notices = workflow_obj.notices
    if not notices:
        return True, 'no notice defined'
    notice_str_list = notices.split(',')
    notice_id_list = [int(notice_str) for notice_str in notice_str_list]
    for notice_id in notice_id_list:
        notice_obj = CustomNotice.objects.filter(id=notice_id, is_deleted=0).first()
        if not notice_obj:
            continue
        title_template = notice_obj.title_template
        content_template = notice_obj.content_template
        # 获取工单所有字段的变量
        ticket_value_info, msg = TicketBaseService.get_ticket_all_field_value(ticket_id)
        if not ticket_value_info:
            return False, msg
        title_result = title_template.format(**ticket_value_info)
        content_result = content_template.format(**ticket_value_info)
        notice_script_file_name = notice_obj.script.name
        notice_script_file = os.path.join(settings.MEDIA_ROOT, notice_script_file_name)

        globals = {'title_result': title_result, 'content_result': content_result, 'participant': ticket_obj.participant}
        try:
            with stdoutIO() as s:
                # execfile(script_file, globals)  # for python 2
                exec(open(notice_script_file).read(), globals)
            script_result = True
            # script_result_msg = ''.join(s.buflist)
            script_result_msg = ''.join(s.getvalue())
            logger.info('send notice successful for ticket_id: {}, notice_id:{}'.format(ticket_id, notice_id))
        except Exception as e:
            logger.error(traceback.format_exc())
            script_result = False
            script_result_msg = e.__str__()
        return script_result, script_result_msg
