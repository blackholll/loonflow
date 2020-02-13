import json
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
        if request.path.startswith('/api/'):
            # api开头的为接口调用，需要额外验证权限,如果用户已经登录loonflow管理后台，允许直接调用
            if request.user.is_authenticated:
                request.META.update(dict(HTTP_APPNAME='loonflow'))
                request.META.update(dict(HTTP_USERNAME=request.user.username))
                return
            flag, msg = self.token_permission_check(request)
            if not flag:
                return HttpResponse(json.dumps(dict(code=-1, msg='permission check fail：{}'.format(msg), data=[])))

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
