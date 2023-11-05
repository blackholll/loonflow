import logging
import traceback

from django.http import HttpResponse
from apps.loon_base_view import BaseView
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from service.manage.common_config_service import common_config_service_ins

logger = logging.getLogger('django')


def index(request):
    """
    overview
    :param request:
    :return:
    """
    return HttpResponse("This is loonflow's api server, please view frontend page, reference: http://loonflow.readthedocs.io/")


class CommonConfigView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get common config info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = common_config_service_ins.get_common_config(tenant_id, operator_id)
            return api_response(0, "", dict(common_config=result))
        except CustomCommonException as e:
            return api_response(-1, {}, str(e))
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, {}, "Internal Server Error")

