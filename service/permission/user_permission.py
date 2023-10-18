from functools import wraps
from service.account.account_base_service import account_base_service_ins
from service.account.account_user_service import account_user_service_ins
from service.format_response import api_response


def user_permission_check(types=None):
    """
    user permission check decorator
    :param types:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def _deco(view_class, request, *args, **kwargs):
            email = request.META.get('HTTP_EMAIL')
            flag, result = account_user_service_ins.user_type_check(email=email, types=types)
            if flag is False:
                return api_response(-1, 'has no permission:{}'.format(result), {})
            return func(view_class, request, *args, **kwargs)

        return _deco
    return decorator

