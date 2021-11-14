import json
from django.test import TestCase
from django.test.client import Client

from tests.base import LoonflowApiCall


class TestAccountView(TestCase):
    fixtures = ['accounts.json', 'workflows.json']

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

    def test_add_app_token(self):
        """
        新增app_token
        :return:
        """
        c = Client()
        c.login(**dict(username='admin', password='123456'))
        app_token_dict = dict(app_name='ops_test', ticket_sn_prefix='ops_test', workflow_ids='1,2')
        response_content = c.post('/api/v1.0/accounts/app_token', data=json.dumps(app_token_dict), content_type='application/json').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), 0)

    def test_update_app_token(self):
        """
        更新app_token
        :return:
        """
        c = Client()
        c.login(**dict(username='admin', password='123456'))
        app_token_dict = dict(ticket_sn_prefix='yunweinew', workflow_ids='2')
        response_content = c.patch('/api/v1.0/accounts/app_token/4', data=json.dumps(app_token_dict),
                                  content_type='application/json').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        print(response_content_dict)
        self.assertEqual(response_content_dict.get('code'), 0)

        new_response_content = c.get('/api/v1.0/accounts/app_token', content_type='application/json').content
        response_content_dict = json.loads(str(new_response_content, encoding='utf-8'))
        result = response_content_dict['data']['value']
        for result0 in result:
            if result0['id'] == 4:
                self.assertEqual(result0['ticket_sn_prefix'], 'yunweinew')
                self.assertEqual(result0['workflow_ids'], '2')
