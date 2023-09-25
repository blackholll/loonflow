import json
from django.test import TestCase
from django.test.client import Client


class TestAccountView(TestCase):
    fixtures = ['accounts.json', 'workflows.json']

    def test_get_user_list_without_login(self):
        """
        get user list without login
        :return:
        """
        c = Client()
        response_content = c.get('/api/v1.0/accounts/users').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), -1)

    def test_get_user_list_with_login(self):
        """
        get user list with login
        :return:
        """
        c = Client()
        # login
        login_content = c.post('/api/v1.0/login', json.dumps(dict(email='blackholll@163.com', password='123456')),content_type="application/json")
        login_response_dict = json.loads(login_content.content)
        jwt = login_response_dict.get("data").get("jwt")
        c.cookies.load(dict(jwt=jwt))
        response_content = c.get('/api/v1.0/accounts/users').content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))
        self.assertEqual(response_content_dict.get('code'), 0)
