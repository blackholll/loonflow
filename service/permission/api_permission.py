import json
import jwt
from django.conf import settings
from django.contrib.auth import login

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.common.common_service import CommonService, common_service_ins


class ApiPermissionCheck(MiddlewareMixin):
    """
    api call permission check middleware
    """
    def process_request(self, request):
        if request.path.startswith('/api/v1.0/accounts/login'):
            # 登录接口特殊处理
            return
        if request.path == '/api/v1.0/login':
            # jwt 登录
            return
        if request.path.startswith('/api/'):
            # for common check
            if request.user.is_authenticated:
                request.META.update(dict(HTTP_APPNAME='loonflow'))
                request.META.update(dict(HTTP_USERNAME=request.user.username))
                return
            if request.COOKIES.get('jwt'):
                # for jwt check
                flag, msg = self.jwt_permission_check(request)
                if flag is False:
                    return HttpResponse(json.dumps(dict(code=-1, msg=msg, data={})))
                else:
                    username = msg['data']['username']
                    flag, user_obj = account_base_service_ins.get_user_by_username(username)
                    if flag is False:
                        return HttpResponse(json.dumps(dict(code=-1, msg=user_obj, data={})))
                    request.META.update(dict(HTTP_APPNAME='loonflow'))
                    request.META.update(dict(HTTP_USERNAME=username))
                    user_obj.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user_obj)

                return
            # for app call token check
            flag, msg = self.token_permission_check(request)
            if not flag:
                return HttpResponse(json.dumps(dict(code=-1, msg='permission check fail：{}'.format(msg), data={})))

    def token_permission_check(self, request):
        """
        token permission check
        :param request:
        :return:
        """

        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        app_name = request.META.get('HTTP_APPNAME')

        if not app_name:
            return False, 'appname is not provide in request header'

        flag, result = account_base_service_ins.get_token_by_app_name(app_name)
        if flag is False:
            return False, result
        if not result:
            return False, 'Appname:{} in request header is unauthorized, please contact administrator to add ' \
                          'authorization for appname:{} in loonflow'.format(app_name, app_name)

        return common_service_ins.signature_check(timestamp, signature, result.token)

    def jwt_permission_check(self, request):
        """
        jwt check
        :param request:
        :return:
        """
        jwt_info = request.COOKIES.get('jwt')
        jwt_salt = settings.JWT_SALT

        try:
            return True, jwt.decode(jwt_info, jwt_salt, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False, 'Token expired'

        except jwt.InvalidTokenError:
            return False, 'Invalid token'
        except Exception as e:
            return False, e.__str__()
