from django.test import TestCase


class LoonflowTest(TestCase):
    def setUp(self):
        # print('start test')
        pass

    def tearDown(self):
        # print('end test')
        pass


class LoonflowApiCall(object):
    """
    loonflow api调用
    """
    def __init__(self):
        from service.common.common_service import CommonService
        flag, msg = CommonService.gen_signature('ops')
        if not flag:
            return dict(code=-1, msg=msg)
        self.signature = msg.get('signature', '')
        self.timestamp = msg.get('timestamp', '')
        self.headers = {'HTTP_SIGNATURE': self.signature, 'HTTP_TIMESTAMP': self.timestamp, 'HTTP_APPNAME':'ops'}

    def api_call(self, method, url, params={}):
        import json
        from django.test.client import Client
        c = Client()
        if method not in ('get', 'post', 'patch', 'delete', 'put'):
            return json.loads(dict(code=-1, msg='method is invalid'))
        if method == 'get':
            response_content = c.get(url, data=params, **self.headers).content
        elif method == 'post':
            response_content = c.post(url, data=json.dumps(params), content_type='application/json', **self.headers).content
        elif method == 'patch':
            response_content = c.patch(url, data=json.dumps(params), content_type='application/json', **self.headers).content
        elif method == 'delete':
            response_content = c.delete(url, data=json.dumps(params), content_type='application/json', **self.headers).content
        elif method == 'put':
            response_content = c.put(url, data=json.dumps(params), content_type='application/json', **self.headers).content
        response_content_dict = json.loads(str(response_content, encoding='utf-8'))

        return response_content_dict
