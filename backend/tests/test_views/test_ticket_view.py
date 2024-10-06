import json
import mock
from django.test import TestCase
from django.test.client import Client
from tests.base import LoonflowApiCall
from service.common.constant_service import constant_service_ins


class TestTicketView(TestCase):
    fixtures = ['accounts.json', 'workflows.json', 'tickets.json']

    def test_get_ticket_list_without_arg_and_header(self):
        """
        获取工单列表,不传参数及header
        :return:
        """
        c = Client()
        response_content = c.get('/api/v1.0/tickets').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_ticket_list_without_arg(self):
        """
        获取工单列表，不传参数
        :return:
        """
        url = '/api/v1.0/tickets'
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_ticket_list_with_arg(self):
        """
        获取工单列表，正确的参数及header
        :return:
        """
        url = '/api/v1.0/tickets'
        response_content_dict = LoonflowApiCall().api_call('get', url, {'category':'all', 'username':'wangfei'})
        self.assertEqual(response_content_dict.get('code'), 0)

    def test_get_ticket_list_category_duty(self):
        """
        获取待办工单列表
        :return:
        """
        result = self.get_ticket_list_by_params(dict(category='duty', username='lilei'))
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_list_category_owner(self):
        """
        获取用户创建的工单列表
        :return:
        """
        result = self.get_ticket_list_by_params(dict(category='owner', username='lilei'))
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_list_category_relation(self):
        """
        获取用户关联的工单列表
        :return:
        """
        result = self.get_ticket_list_by_params(dict(category='relation', username='lilei'))
        self.assertEqual(result.get('code'), 0)

    @mock.patch('tasks.flow_hook_task.apply_async')
    @mock.patch('tasks.send_ticket_notice.apply_async')
    @mock.patch('service.ticket.ticket_base_service.TicketBaseService.gen_ticket_sn')
    def test_new_ticket(self, gen_ticket_sn, notice_apply_async, hook_apply_async):
        """
        新建工单
        :return:
        """
        gen_ticket_sn.return_value = (True, dict(ticket_sn='ops_202005240001'))
        notice_apply_async.return_value = True
        hook_apply_async.return_value = True
        params = dict(title='测试工单0001', leave_start='2018-10-14 09:00:00', leave_end='2018-10-15 09:00:00',
                      leave_proxy='lisi', leave_type='2', leave_reason='请假原因', workflow_id=1,
                      username='guiji', transition_id=1)
        url = '/api/v1.0/tickets'
        result = LoonflowApiCall().api_call('post', url, params)
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_detail(self):
        """
        获取工单详情
        :return:
        """
        url = '/api/v1.0/tickets/{}'.format(39)
        result = LoonflowApiCall().api_call('get', url, dict(username='admin'))
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_transition(self):
        """
        测试获取工单可以执行的操作
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        ticket_participant_type_id = last_ticket_obj.participant_type_id
        ticket_participant = last_ticket_obj.participant
        if ticket_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_PERSONAL:
            username= ticket_participant
        elif ticket_participant_type_id == constant_service_ins.PARTICIPANT_TYPE_MULTI:
            username = ticket_participant.split(',')[0]
        url = '/api/v1.0/tickets/{}/transitions'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('get', url, dict(username=username))
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_flow_logs(self):
        """
        测试获取工单流转记录
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        url = '/api/v1.0/tickets/{}/flowlogs'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('get', url, dict(username='lilie'))
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_flow_steps(self):
        """
        测试获取工单step记录
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        url = '/api/v1.0/tickets/{}/flowsteps'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('get', url, dict(username='admin'))
        self.assertEqual(result.get('code'), 0)

    @mock.patch('tasks.send_ticket_notice.apply_async')
    def test_alter_ticket_state(self, notice_apply_async):
        """
        修改工单状态
        :return:
        """
        ticket_id = 39
        new_state_id = 4
        url = '/api/v1.0/tickets/{}/state'.format(ticket_id)
        notice_apply_async.return_value = True
        result = LoonflowApiCall().api_call('put', url, dict(state_id=new_state_id))
        self.assertEqual(result.get('code'), 0)

    def test_alter_ticket_field_value(self):
        """
        修改工单字段的值
        :return:
        """
        from apps.ticket.models import TicketRecord
        ticket_id = 39
        ticket_obj = TicketRecord.objects.get(id=ticket_id)
        ticket_title = ticket_obj.title
        url = '/api/v1.0/tickets/{}/fields'.format(ticket_id)
        result = LoonflowApiCall().api_call('patch', url, dict(username='lilie', title='_test'.format(ticket_title)))
        self.assertEqual(result.get('code'), 0)

    def test_add_ticket_comment(self):
        """
        测试新增评论
        :return:
        """
        from apps.ticket.models import TicketRecord
        ticket_id = 39
        last_ticket_obj = TicketRecord.objects.get(id=ticket_id)
        last_ticket_id = last_ticket_obj.id
        url = '/api/v1.0/tickets/{}/comments'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('post', url, dict(suggestion='test for commnet'))
        self.assertEqual(result.get('code'), 0)

    def get_ticket_list_by_params(self, params):
        """
        根据参数获取用户工单列表
        :param category:
        :return:
        """
        url = '/api/v1.0/tickets'
        response_content_dict = LoonflowApiCall().api_call('get', url, params)
        return response_content_dict

