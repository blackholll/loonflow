import json
from tests.base import LoonflowTest
from django.test.client import Client


class TestAccountView(LoonflowTest):
    def test_get_user_list_without_login(self):
        """
        获取用户列表，不登录
        :return:
        """
        c = Client()
        response_content = c.get('/api/v1.0/accounts/users').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_user_list_with_login(self):
        """
        获取用户列表
        :return:
        """
        c = Client()
        c.login(**dict(username='admin', password='123456'))
        response_content = c.get('/api/v1.0/accounts/users').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), 0)
