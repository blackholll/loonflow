import time
import hashlib
from service.base_service import BaseService
from service.common.log_service import auto_log


class CommonService(BaseService):
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def signature_check(cls, timestamp: str, signature: str, md5_key: str)->tuple:
        """
        signature check
        :param timestamp:
        :param signature:
        :param md5_key:
        :return:
        """
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        if tar_str == signature:
            # The validity of the signature: 120s
            time_now_int = int(time.time())
            if abs(time_now_int - int(timestamp)) <= 120:
                # if abs(time_now_int - int(timestamp)) <= 12000000000000000:
                return True, ''
            else:
                msg = 'The signature you provide in request header is expire, please ensure in 120s'
        else:
            msg = 'The signature you provide in request header is invalid'
        return False, msg

    @classmethod
    @auto_log
    def gen_signature(cls, app_name: str)->tuple:
        """
        gen signature info
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
    def gen_signature_by_token(cls, token: str)->tuple:
        md5_key = token
        timestamp = str(int(time.time()))
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return True, dict(signature=tar_str, timestamp=timestamp)

    @classmethod
    @auto_log
    def gen_hook_signature(cls, token: str)->tuple:
        """
        gen hook token signature
        :param token:
        :return:
        """
        timestamp = str(int(time.time()))
        ori_str = timestamp + token
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return True, dict(signature=tar_str, timestamp=timestamp)

    @classmethod
    @auto_log
    def get_model_field(cls, app_name: str, model_name: str)->tuple:
        """
        get model's field list
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

        return True, dict(field_dict=field_dict)

    @classmethod
    @auto_log
    def get_dict_blank_or_false_value_key_list(cls, dict_obj: object)->tuple:
        """
        get blank item value's key list in dict
        :param dict_obj:
        :return:
        """
        result_list = []
        for key, value in dict_obj.items():
            if not value:
                result_list.append(key)
        return True, dict(result_list=result_list)

    @classmethod
    @auto_log
    def check_dict_has_all_same_value(cls, dict_obj: object)->tuple:
        """
        check whether all key are equal in a dict
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


common_service_ins = CommonService()

if __name__ == '__main__':
    print(common_service_ins.check_dict_has_all_same_value({'a': {'a': 1, 'b': 2}, 'b': {'a': 1, 'b': 2}}))
