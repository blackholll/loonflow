import functools
import logging
import traceback

logger = logging.getLogger('django')


def auto_log(func):
    """
    auto write log decorator
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc())
            return False, e.__str__()
    return _deco
