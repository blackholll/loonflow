import fnmatch
import requests
from django.conf import settings
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.exception.custom_common_exception import CustomCommonException


class HookBaseService(BaseService):
    @classmethod
    def call_hook(cls, hook_url: str, token: str, request_data_dict: dict) -> dict:
        hook_url_forbidden_list = settings.HOOK_HOST_FORBIDDEN
        for url in hook_url_forbidden_list:
            if fnmatch.fnmatch(hook_url, url):
                raise CustomCommonException("hook url is blocked, please contact system administrator to change HOOK_HOST_FORBIDDEN configure")
        signature, timestamp = common_service_ins.gen_signature_by_token(token)
        headers = dict(signature=signature, timestamp=timestamp)
        result = requests.post(hook_url, headers=headers, json=request_data_dict).json()
        return result


hook_base_service_ins = HookBaseService()



