import json
import jwt
from django.conf import settings
from django.contrib.auth import login

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.account.account_user_service import AccountUserService
from service.common.common_service import CommonService, common_service_ins


class AppPermissionCheck(MiddlewareMixin):
    """
    app call permission check middleware
    """
    def process_request(self, request):
        if request.path == '/api/v1.0/login':
            # for jwt login
            return
        if request.path.startswith('/api/'):
            if request.COOKIES.get('jwt'):
                # for jwt check
                flag, msg = self.jwt_permission_check(request)
                if flag is False:
                    return HttpResponse(json.dumps(dict(code=-1, msg=msg, data={})))
                else:
                    request.META.update(dict(HTTP_APPNAME='loonflow'))
                    request.META.update(dict(HTTP_EMAIL=msg.email))
                    request.META.update(dict(HTTP_USERID=msg.id))
                    request.META.update(dict(HTTP_TENANTID=msg.tenant_id))
                    request.META.update(dict(HTTP_TENANNAME=msg.tenant.name))
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
        jwt check, user existed check, user status check
        :param request:
        :return:
        """
        jwt_info = request.COOKIES.get('jwt')
        jwt_salt = settings.JWT_SALT

        try:
            jwt_data = jwt.decode(jwt_info, jwt_salt, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False, 'Token expired'

        except jwt.InvalidTokenError:
            return False, 'Invalid token'
        except Exception as e:
            return False, e.__str__()
        #  check user status
        flag, user_info = AccountUserService.get_user_by_email(jwt_data.get("data").get('email'))
        if flag is False:
            return False, "user is not existed or has been deleted"
        if user_info.status == "resigned":
            return False, "resigned staff can not login"
        return True, user_info
