from ast import pattern
import json
from django.db.models.constraints import F
import jwt
import re
import traceback
from celery.worker.consumer.mingle import exception
from django.conf import settings
from django.contrib.auth import login

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from service.account.account_application_service import account_application_service_ins
from service.account.account_base_service import AccountBaseService, account_base_service_ins
from service.account.account_user_service import AccountUserService, account_user_service_ins
from service.common.common_service import CommonService, common_service_ins
from service.exception.custom_common_exception import CustomCommonException


class AppPermissionCheck(MiddlewareMixin):
    """
    app call permission check middleware
    """
    def process_request(self, request, *args, **kwargs):
        if request.path == '/api/v1.0/login':
            # for jwt login
            return
        if request.path.startswith('/api/v1.0/accounts/tenants/by_domain'):
            return
        if request.path.startswith('/api/v1.0/tickets/mock_external_assignee'):
            return
        if request.path.startswith('/api/v1.0/tickets/mock_external_data_source'):
            return
        # OAuth related endpoints don't require authentication
        if request.path.startswith('/api/v1.0/manage/auth/'):
            # Set default tenant_id for OAuth endpoints
            if not request.META.get('HTTP_TENANTID'):
                request.META.update(dict(HTTP_TENANTID='00000000-0000-0000-0000-000000000001'))
            return
        if request.path.startswith('/api/'):
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header:
                # PAT management endpoints must use JWT only (avoid bootstrap loops).
                if request.path.startswith('/api/v1.0/accounts/personal_access_tokens'):
                    user_info = self.jwt_permission_check(auth_header)
                else:
                    user_info = self.resolve_user_from_authorization_header(auth_header)
                if not request.META.get('HTTP_APPNAME'):
                    request.META.update(dict(HTTP_APPNAME='loonflow'))
                request.META.update(dict(HTTP_EMAIL=user_info.email))
                request.META.update(dict(HTTP_USERID=str(user_info.id)))
                request.META.update(dict(HTTP_TENANTID=str(user_info.tenant_id)))
                return
            elif request.path == '/api/v1.0/configs/common':
                request.META.update(dict(HTTP_TENANTID='00000000-0000-0000-0000-000000000001'))
                request.META.update(dict(HTTP_USERID='00000000-0000-0000-0000-000000000000'))
                return
            # for app call token check
            try:
                self.token_permission_check(request)
                return
            except Exception as e:
                return HttpResponse(json.dumps(dict(code=-1, msg='permission check fail：{}'.format(e.__str__()), data={})), status=401)

    def token_permission_check(self, request):
        """
        token permission check
        :param request:
        :return:
        """
        if request.method.lower() == 'get':
            pattern = r'/api/v1\.0/tickets/([^/]+)/([^/]+)/files/([^/]+\.\w+)$'
            if re.match(pattern, request.path):
                if request.GET.get('token'):
                    request.META.update(dict(HTTP_TENANTID=""))
                    request.META.update(dict(HTTP_APPNAME=""))
                    request.META.update(dict(HTTP_EMAIL=""))
                    request.META.update(dict(HTTP_USERID=""))
                    return
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        app_name = request.META.get('HTTP_APPNAME')
        email = request.META.get('HTTP_EMAIL')
        tenant_id = request.META.get('HTTP_TENANTID')
        err_msg = ''
        if not signature:
            err_msg += 'signature is not provide in request header;'
        if not timestamp:
            err_msg += 'timestamp is not provide in request header;'
        if not app_name:
            err_msg += 'appname is not provide in request header;'
        if not email:
            err_msg += 'email is not provide in request header;'
        if not tenant_id:
            err_msg += 'tenantid is not provide in request header;'
        if err_msg:
            raise CustomCommonException(err_msg)
        
        try:
            app_record = account_application_service_ins.get_record_by_app_name(tenant_id, app_name)
            user_record = account_user_service_ins.get_user_by_email(email)
            request.META.update(dict(HTTP_USERID=user_record.id))
        except CustomCommonException:
                raise
        except Exception as e:
            raise CustomCommonException('Appname:{} in request header is unauthorized, please contact administrator to add ' \
                          'authorization for appname:{} in loonflow'.format(app_name, app_name))
        return common_service_ins.signature_check(timestamp, signature, app_record.token)

    def resolve_user_from_authorization_header(self, auth_header: str):
        """
        Resolve user from Bearer token: personal access token (lfpat.*) or JWT.
        """
        if not auth_header.startswith('Bearer '):
            raise CustomCommonException('Authorization header is not valid')
        token = auth_header.split(' ', 1)[1].strip()
        if token.startswith('lfpat.'):
            from service.account.personal_access_token_service import personal_access_token_service_ins

            return personal_access_token_service_ins.verify_token_string(token)
        return self.jwt_permission_check_token(token)

    def jwt_permission_check(self, auth_header: str):
        """
        jwt check, user existed check, user status check
        :param auth_header:
        :return:
        """
        if not auth_header.startswith('Bearer '):
            raise CustomCommonException('Authorization header is not valid')
        jwt_info = auth_header.split(' ', 1)[1].strip()
        return self.jwt_permission_check_token(jwt_info)

    def jwt_permission_check_token(self, jwt_info: str):
        """
        jwt check given raw JWT string (no Bearer prefix).
        """
        jwt_salt = settings.JWT_SALT
        try:
            jwt_data = jwt.decode(jwt_info, jwt_salt, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise CustomCommonException('Token expired')

        except jwt.InvalidTokenError:
            raise CustomCommonException('Invalid token')
        except Exception as e:
            # logger.error(traceback.format_exc)
            raise CustomCommonException('Internal Server Error')
        #  check user status
        user_info = AccountUserService.get_user_by_email(jwt_data.get("data").get('email'))
        return user_info
