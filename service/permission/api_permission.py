import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from service.account.account_base_service import AccountBaseService
from service.common.common_service import CommonService


class ApiPermissionCheck(MiddlewareMixin):
    """
    api调用权限校验中间件
    """
    def process_request(self, request):
        if request.path.startswith('/api/'):
            # api开头的为接口调用，需要额外验证权限
            flag, msg = self.token_permission_check(request)
            if not flag:
                return HttpResponse(json.dumps(dict(code=-1, msg='权限校验失败：{}'.format(msg), data=[])))

    def token_permission_check(self, request):
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        app_name = request.META.get('HTTP_APPNAME')

        if not app_name:
            return False, '未提供appname(调用loonflow接口需要鉴权，请根据文档中"调用授权"部分说明来调用)'
        app_token_obj, msg = AccountBaseService.get_token_by_app_name(app_name)
        if not app_token_obj:
            return False, 'appname未授权，请联系管理员(调用loonflow接口需要鉴权，请根据文档中"调用授权"部分说明来调用)'
        return CommonService.signature_check(timestamp, signature, app_token_obj.token)
