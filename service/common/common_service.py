import hashlib

import time

from service.base_service import BaseService
from service.common.log_service import auto_log


class CommonService(BaseService):
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def signature_check(cls, timestamp, signature, md5_key):
        """
        签名校验
        :param timestamp:
        :param signature:
        :param md5_key:
        :return:
        """
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        if tar_str == signature:
            # 时间验证，120s
            time_now_int = int(time.time())
            if abs(time_now_int - int(timestamp)) <= 120:
                # if abs(time_now_int - int(timestamp)) <= 12000000000000000:
                return True, ''
            else:
                msg = '时间戳过期,请保证在120s内'
        else:
            msg = '签名校验失败'
        return False, msg

    @classmethod
    @auto_log
    def get_model_field(cls, app_name, model_name):
        """
        获取model的字段信息
        :param app_name:
        :param model_name:
        :return:
        """
        from django.apps import apps
        model_obj = apps.get_model(app_name, model_name)
        fields = model_obj._meta.fields
        field_dict = {}
        for field0 in fields:
            field_dict[field0.name] = field0.verbose_name

        return field_dict
