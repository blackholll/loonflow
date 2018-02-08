import functools
import logging
import traceback


def auto_log(func):
    """
    自动记录日志的装饰器：
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logging.error(traceback.format_exc())
            return False, e.__str__()
    return _deco
