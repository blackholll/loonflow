import json
from tests.base import LoonflowTest
from django.test.client import Client
from service.common.common_service import CommonService
from tests.base import LoonflowApiCall


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
