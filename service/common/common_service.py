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
    def gen_signature(cls, app_name):
        """
        生成签名信息
        :param app_name:
        :return:
        """
        from apps.account.models import AppToken
        app_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        md5_key = app_obj.token
        timestamp = str(int(time.time()))
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return True, dict(signature=tar_str, timestamp=timestamp)

    @classmethod
    @auto_log
    def gen_hook_signature(cls, token):
        """
        生成hook签名
        :param token:
        :return:
        """
        timestamp = str(int(time.time()))
        ori_str = timestamp + token
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return True, dict(signature=tar_str, timestamp=timestamp)


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

    @classmethod
    @auto_log
    def get_dict_blank_or_false_value_key_list(cls, dict_obj):
        """
        获取字典的空值的key的list
        :param dict_obj:
        :return:
        """
        result_list = []
        for key, value in dict_obj.items():
            if not value:
                result_list.append(key)
        return result_list, ''

    @classmethod
    @auto_log
    def check_dict_has_all_same_value(cls, dict_obj):
        """
        判断字段是否所有key的值都相同
        :param dict_obj:
        :return:
        """
        value_list = []
        for key, value in dict_obj.items():
            value_list.append(value)
        value_0 = value_list[0]
        for value in value_list:
            if value_0 != value:
                return False, 'not all dict value is same'
        return True, ''


if __name__ == '__main__':
    print(CommonService().check_dict_has_all_same_value({'a':{'a': 1, 'b': 2}, 'b':{'a': 1, 'b': 2}}))
