# import json
from django.http import JsonResponse

from django.http import HttpResponse


def api_response(code, msg='', data=''):
    """
    格式化返回
    :param code:
    :param msg:
    :param data:
    :return:
    """
    return JsonResponse(dict(code=code, data=data, msg=msg))
