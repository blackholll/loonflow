# from __future__ import absolute_import, unicode_literals
import contextlib
import os
import sys
import traceback
import logging
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.config')
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

import json
import requests
from apps.ticket.models import TicketRecord
from apps.workflow.models import Transition, State, WorkflowScript, Workflow, CustomNotice
from service.account.account_base_service import account_base_service_ins
from service.common.constant_service import constant_service_ins
from service.ticket.ticket_base_service import TicketBaseService, ticket_base_service_ins
from service.common.common_service import CommonService, common_service_ins
from service.workflow.workflow_transition_service import WorkflowTransitionService, workflow_transition_service_ins
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
def run_flow_task(ticket_id, script_id_str, state_id, action_from='loonrobot'):
    """
    执行工作流脚本
    :param script_id_star:通过脚本id来执行, 保存的是字符串
    :param ticket_id:
    :param state_id:
    :param action_from:
    :return:
    """
    script_id = int(script_id_str)
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
    if ticket_obj.participant == script_id_str and ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROBOT:
        ## 校验脚本是否合法
        # 获取脚本名称
        script_obj = WorkflowScript.objects.filter(id=script_id, is_deleted=False, is_active=True).first()
        if not script_obj:
            return False, '脚本未注册或非激活状态'

        script_file = os.path.join(settings.MEDIA_ROOT, script_obj.saved_name.name)
        globals = {'ticket_id': ticket_id, 'action_from': action_from}
        # 如果需要脚本执行完成后，工单不往下流转(也就脚本执行失败或调用其他接口失败的情况)，需要在脚本中抛出异常
        try:
            with stdoutIO() as s:
                # execfile(script_file, globals)  # for python 2
                exec(open(script_file, encoding='utf-8').read(), globals)
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
                                    suggestion=script_result_msg, participant_type_id=constant_service_ins.PARTICIPANT_TYPE_ROBOT,
                                    participant='脚本:(id:{}, name:{})'.format(script_obj.id, script_obj.name), state_id=state_id, creator='loonrobot')

        ticket_base_service_ins.add_ticket_flow_log(new_ticket_flow_dict)
        if not script_result:
            # 脚本执行失败，状态不更新,标记任务执行结果
            ticket_obj.script_run_last_result = False
            ticket_obj.save()
            return False, script_result_msg
        # 自动执行流转
        flag, msg = ticket_base_service_ins.handle_ticket(ticket_id, dict(username='loonrobot',
                                                                    suggestion='脚本执行完成后自行流转',
                                                                    transition_id=transition_obj.id), False, True)
        if flag:
            logger.info('******脚本执行成功,工单基础信息更新完成, ticket_id:{}******'.format(ticket_id))
        return flag, msg
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
    # flow_log_set, msg = TicketBaseService().get_ticket_flow_log(ticket_id, 'loonrobot', per_page=1000)
    flag, result = ticket_base_service_ins.get_ticket_flow_log(ticket_id, 'loonrobot', per_page=1000)
    if flag is False:
        return False, result
    flow_log_list = result.get('ticket_flow_log_restful_list')
    for flow_log in flow_log_list:
        if flow_log.get('state').get('state_id') == state_id and flow_log.get('gmt_created') > date_time:
            return True, '后续有操作，定时器失效'
    # 执行流转
    handle_ticket_data = dict(transition_id=transition_id, username='loonrobot', suggestion='定时器流转')
    ticket_base_service_ins.handle_ticket(ticket_id, handle_ticket_data, True)


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
    # 将通知内容，通知标题，通知人，作为hook的请求参数
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
    if not ticket_obj:
        return False, 'ticket is not exist or has been deleted'

    workflow_id = ticket_obj.workflow_id
    workflow_obj = Workflow.objects.filter(id=workflow_id, is_deleted=0).first()
    notices = workflow_obj.notices
    if not notices:
        return True, 'no notice defined'
    notice_str_list = notices.split(',')
    notice_id_list = [int(notice_str) for notice_str in notice_str_list]
    send_notice_result_list = []

    title_template = workflow_obj.title_template
    content_template = workflow_obj.content_template

    # 获取工单所有字段的变量
    flag, ticket_value_info = ticket_base_service_ins.get_ticket_all_field_value(ticket_id)
    if flag is False:
        return False, ticket_value_info
    title_result = title_template.format(**ticket_value_info)
    content_result = content_template.format(**ticket_value_info)
    # 获取工单最后一条操作记录
    flag, result = ticket_base_service_ins.get_ticket_flow_log(ticket_id, 'loonrobot')
    flow_log_list = result.get('ticket_flow_log_restful_list')

    last_flow_log = flow_log_list[0]
    participant_info_list = []
    participant_username_list = []
    from apps.account.models import LoonUser
    if ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
        participant_username_list = [ticket_obj.participant]
    elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
        participant_username_list = ticket_obj.participant.split(',')
    elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_ROLE:
        flag, participant_username_list = account_base_service_ins.get_role_username_list(ticket_obj.participant)
        if flag is False:
            return False, participant_username_list

    elif ticket_obj.participant_type_id == constant_service_ins.PARTICIPANT_TYPE_DEPT:
        flag, participant_username_list = account_base_service_ins.get_dept_username_list(ticket_obj.participant)
        if not flag:
            return flag, participant_username_list

    if participant_username_list:
        participant_queryset = LoonUser.objects.filter(username__in=participant_username_list, is_deleted=0)
        for participant_0 in participant_queryset:
            participant_info_list.append(dict(username=participant_0.username, alias=participant_0.alias,
                                              phone=participant_0.phone, email=participant_0.email))

    params = {'title_result': title_result, 'content_result': content_result,
               'participant': ticket_obj.participant, 'participant_type_id': ticket_obj.participant_type_id,
               'multi_all_person': ticket_obj.multi_all_person, 'ticket_value_info': ticket_value_info,
               'last_flow_log': last_flow_log, 'participant_info_list': participant_info_list}
    for notice_id in notice_id_list:
        notice_obj = CustomNotice.objects.filter(id=notice_id, is_deleted=0).first()
        if not notice_obj:
            continue
        hook_url = notice_obj.hook_url
        from service.workflow.workflow_base_service import workflow_base_service_ins
        flag, msg = workflow_base_service_ins.hook_host_valid_check(hook_url)
        if not flag:
            return False, msg
        hook_token = notice_obj.hook_token
        # gen signature
        flag, headers = common_service_ins.gen_signature_by_token(hook_token)
        try:
            r = requests.post(hook_url, headers=headers, json=params)
            result = r.json()
            if result.get('code') == 0:
                send_notice_result_list.append(dict(notice_id=notice_id, result='success', msg=result.get('msg', '')))
            else:
                send_notice_result_list.append(dict(notice_id=notice_id, result='fail', msg=result.get('msg', '')))
        except Exception as e:
            send_notice_result_list.append(dict(notice_id=notice_id, result='fail', msg=e.__str__()))

    return True, dict(send_notice_result_list=send_notice_result_list)


@app.task
def flow_hook_task(ticket_id):
    """
    hook 任务
    :param ticket_id:
    :return:
    """
    # 查询工单状态
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
    state_id = ticket_obj.state_id
    state_obj = State.objects.filter(id=state_id, is_deleted=0).first()

    participant_type_id = state_obj.participant_type_id
    if participant_type_id != constant_service_ins.PARTICIPANT_TYPE_HOOK:
        return False, ''
    hook_config = state_obj.participant
    hook_config_dict = json.loads(hook_config)
    hook_url = hook_config_dict.get('hook_url')
    hook_token = hook_config_dict.get('hook_token')
    wait = hook_config_dict.get('wait')
    extra_info = hook_config_dict.get('extra_info')

    from service.workflow.workflow_base_service import workflow_base_service_ins
    hook_check_flag, hook_result_msg = workflow_base_service_ins.hook_host_valid_check(hook_url)

    flag, msg = common_service_ins.gen_hook_signature(hook_token)
    if not flag:
        hook_check_flag, hook_result_msg = flag, msg
    flag, all_ticket_data = ticket_base_service_ins.get_ticket_all_field_value(ticket_id)
    flag, all_field_value_result = ticket_base_service_ins.get_ticket_all_field_value_json(ticket_id)
    all_ticket_data_json = all_field_value_result.get('all_field_value_json')
    if hook_check_flag:
        if extra_info is not None:
            all_ticket_data.update(dict(extra_info=extra_info))
        try:
            r = requests.post(hook_url, headers=msg, json=all_ticket_data, timeout=10)
            result = r.json()
        except Exception as e:
            result = dict(code=-1, msg=e.__str__())
        if result.get('code') == 0:
            # 调用成功

            TicketBaseService().add_ticket_flow_log(dict(ticket_id=ticket_id, transition_id=0,
                                                         suggestion=result.get('msg'),
                                                         participant_type_id=constant_service_ins.PARTICIPANT_TYPE_HOOK,
                                                         participant='hook', state_id=state_id,
                                                         intervene_type_id=constant_service_ins.TRANSITION_INTERVENE_TYPE_HOOK,
                                                         ticket_data=all_ticket_data_json,
                                                         creator='loonrobot'
                                                      ))
            if not wait:
                # 不等待hook目标回调，直接流转
                flag, transition_queryset = workflow_transition_service_ins.get_state_transition_queryset(state_id)
                transition_id = transition_queryset[0].id  # hook状态只支持一个流转

                new_request_dict = {}
                new_request_dict.update({'transition_id': transition_id, 'suggestion': msg, 'username': 'loonrobot'})
                # 执行流转
                flag, msg = ticket_base_service_ins.handle_ticket(ticket_id, new_request_dict, by_hook=True)
                if not flag:
                    return False, msg
            return True, ''
        hook_result_msg = result.get('msg')

    ticket_base_service_ins.update_ticket_field_value(ticket_id, {'script_run_last_result': False})
    ticket_base_service_ins.add_ticket_flow_log(
        dict(ticket_id=ticket_id, transition_id=0, suggestion=hook_result_msg,
             participant_type_id=constant_service_ins.PARTICIPANT_TYPE_HOOK,
             participant='hook', state_id=state_id, ticket_data=all_ticket_data_json, creator='loonrobot'))
