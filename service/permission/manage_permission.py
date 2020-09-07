from functools import wraps
from service.account.account_base_service import account_base_service_ins
from service.format_response import api_response


def manage_permission_check(permission=None):
    """
    manage permission check decorator
    :param permission:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def _deco(view_class, request, *args, **kwargs):
            username = request.META.get('HTTP_USERNAME')
            if permission == 'admin':
                flag, result = account_base_service_ins.admin_permission_check(username)
                if flag is False:
                    return api_response(-1, 'has no permission:{}'.format(result), {})
            elif permission == 'workflow_admin':
                flag, result = account_base_service_ins.workflow_admin_permission_check(username)
                if flag is False:
                    return api_response(-1, 'has no permission:{}'.format(result), {})
            return func(view_class, request, *args, **kwargs)

        return _deco
    return decorator

