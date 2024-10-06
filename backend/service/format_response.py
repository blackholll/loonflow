import json

from django.http import HttpResponse


def api_response(code, msg='', data=''):
    """
    格式化返回
    :param code:
    :param msg:
    :param data:
    :return:
    """
    return HttpResponse(json.dumps(dict(code=code, data=data, msg=msg)), content_type="application/json")
