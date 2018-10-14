import json
from tests.base import LoonflowTest
from django.test.client import Client
from tests.base import LoonflowApiCall
from service.common.constant_service import CONSTANT_SERVICE


class TestTicketView(LoonflowTest):
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

    def test_new_ticket(self):
        """
        新建工单
        :return:
        """
        params = dict(title='测试工单0001', leave_start='2018-10-14 09:00:00', leave_end='2018-10-15 09:00:00',
                      leave_days=2, leave_proxy='lisi', leave_type='2', leave_reason='请假原因', workflow_id=1,
                      username='guiji', transition_id=1)
        url = '/api/v1.0/tickets'
        result = LoonflowApiCall().api_call('post', url, params)
        self.assertEqual(result.get('code'), 0)

    def test_get_ticket_detail(self):
        """
        获取工单详情
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_id = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first().id
        url = '/api/v1.0/tickets/{}'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('get', url, dict(username='lilei'))
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
        if ticket_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            username= ticket_participant
        elif ticket_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
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
        result = LoonflowApiCall().api_call('get', url, dict(username='lilie'))
        self.assertEqual(result.get('code'), 0)

    def test_alter_ticket_state(self):
        """
        修改工单状态
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        last_ticket_state_id = last_ticket_obj.state_id
        url = '/api/v1.0/tickets/{}/state'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('put', url, dict(username='lilie', state_id=last_ticket_state_id))
        self.assertEqual(result.get('code'), 0)

    def test_alter_ticket_field_value(self):
        """
        修改工单字段的值
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        last_ticket_title = last_ticket_obj.title
        url = '/api/v1.0/tickets/{}/fields'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('patch', url, dict(username='lilie', title=last_ticket_title))
        self.assertEqual(result.get('code'), 0)

    def test_add_ticket_comment(self):
        """
        测试新增评论
        :return:
        """
        from apps.ticket.models import TicketRecord
        last_ticket_obj = TicketRecord.objects.filter(is_deleted=0).order_by('-id').first()
        last_ticket_id = last_ticket_obj.id
        url = '/api/v1.0/tickets/{}/comments'.format(last_ticket_id)
        result = LoonflowApiCall().api_call('post', url, dict(username='lilie', suggestion='test for commnet'))
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

