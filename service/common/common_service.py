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

