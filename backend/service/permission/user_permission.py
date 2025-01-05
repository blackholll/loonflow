import json
from functools import wraps
from service.account.account_application_service import account_application_service_ins
from service.account.account_base_service import account_base_service_ins
from service.account.account_user_service import account_user_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response


def user_permission_check(types='', workflow_id_source=''):
    """
    user permission check decorator
    :param workflow_id_source:  from url or body
    :param types:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def _deco(view_class, request, *args, **kwargs):
            email = request.META.get('HTTP_EMAIL')
            tenant_id = request.META.get('HTTP_TENANTID')
            app_name = request.META.get('HTTP_APPNAME')
            if workflow_id_source == 'url':
                workflow_id = kwargs.get('workflow_id')
            elif workflow_id_source == 'body':
                request_data = request.body
                workflow_id = json.loads(request_data).get('workflow_id')

            if app_name != 'loonflow':
                try:
                    account_application_service_ins.app_type_check(tenant_id, app_name, workflow_id)
                except CustomCommonException as e:
                    return api_response(-1, 'has no permission:{}'.format(e.message), {})
            else:
                try:
                    account_user_service_ins.user_type_check(email=email, tenant_id=tenant_id, types=types)
                except CustomCommonException as e:
                    return api_response(-1, 'has no permission:{}'.format(e.message), {})
            return func(view_class, request, *args, **kwargs)
        return _deco
    return decorator

