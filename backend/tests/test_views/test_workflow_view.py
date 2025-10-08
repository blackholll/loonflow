import json
from django.test import TestCase
from tests.base import LoonflowApiCall


class TestWorkflowView(TestCase):
    fixtures = ['accounts.json', 'workflows.json']

    def test_get_workflow_list_without_arg(self):
        """
        获取工作流列表
        :return:
        """
        url = '/api/v1.0/workflows'
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), 0)
        self.assertGreater(len(response_content_dict.get('data')), 1)

    def test_get_workflow_init_state(self):
        """
        获取工作流初始状态
        :return:
        """
        workflow_id = 1
        url = '/api/v1.0/workflows/{}/init_state'.format(workflow_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), 0)

    def test_get_workflow_states(self):
        """
        获取工作流状态列表
        :return:
        """
        workflow_id = 1
        url = '/api/v1.0/workflows/{}/states'.format(workflow_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), 0)

    def test_get_workflow_state_detail(self):
        """
        获取状态详情
        :return:
        """
        state_id = 3
        url = '/api/v1.0/workflows/states/{}'.format(state_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), 0)
