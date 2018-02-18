from django.utils import six
from rest_framework.response import Response


class JsonResponse(Response):
    def __init__(self, data=None, code=None, msg=None, template_name=None, headers=None, exception=False,
                 content_type=None, per_page=None, page=None, total=None):
        super(Response, self).__init__(None, status=None)

        dava_value = {'value': data}
        if per_page:
            dava_value['per_page'] = per_page
        if per_page:
            dava_value['page'] = page
        if per_page:
            dava_value['total'] = total

        self.data = {"code": code, "msg": msg, "data": dava_value}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type
        self.status_code = code

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

