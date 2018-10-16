import json
from tests.base import LoonflowTest
from tests.base import LoonflowApiCall
from service.common.constant_service import CONSTANT_SERVICE


class TestWorkflowView(LoonflowTest):
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
        from apps.workflow.models import Workflow
        last_workflow_id = Workflow.objects.filter(is_deleted=0).order_by('-id').first().id
        url = '/api/v1.0/workflows/{}/init_state'.format(last_workflow_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_workflow_states(self):
        """
        获取工作流状态列表
        :return:
        """
        from apps.workflow.models import Workflow
        last_workflow_id = Workflow.objects.filter(is_deleted=0).order_by('-id').first().id
        url = '/api/v1.0/workflows/{}/states'.format(last_workflow_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_workflow_state_detail(self):
        """
        获取状态详情
        :return:
        """
        from apps.workflow.models import State
        last_state_id = State.objects.filter(is_deleted=0).order_by('-id').first().id
        url = '/api/v1.0/workflows/states/{}'.format(last_state_id)
        response_content_dict = LoonflowApiCall().api_call('get', url)
        self.assertEqual(response_content_dict.get('code'), -1)
