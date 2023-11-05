import logging
import simplejson
from django.views import View
from schema import SchemaError

from service.format_response import api_response

logger = logging.getLogger('django')


class BaseView(View):
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
        if meth_schema:
            if request_method in ['post', 'patch', 'put', 'delete']:
                json_dict = simplejson.loads(request.body)
            else:
                json_dict = dict(request.GET)
            try:
                meth_schema.validate(json_dict)
            except SchemaError as Se:
                logger.error(Se)
                return api_response(-1, 'Request data is invalid:{}'.format(str(Se)), {})
            except Exception as e:
                logger.error(e)
                return api_response(-1, 'Internal Server Error', {})
        return handler(request, *args, **kwargs)
