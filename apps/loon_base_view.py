import simplejson
import json
from django.views import View

from service.format_response import api_response


class LoonBaseView(View):
    """
    base view for params validate
    """
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        request_method = request.method.lower()
        meth_schema = getattr(self, request.method.lower() + '_schema', None)
        if meth_schema and request_method in ['post', 'patch', 'put']:
            try:
                json_dict = simplejson.loads(request.body)
                meth_schema.validate(json_dict)
            except Exception as e:
                print(e.__str__())
                return api_response(-1, '请求参数不合法:{}'.format(e.__str__()), {})


        return handler(request, *args, **kwargs)

