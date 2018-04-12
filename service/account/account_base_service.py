from apps.account.models import AppToken
from service.base_service import BaseService
from service.common.log_service import auto_log


class AccountBaseService(BaseService):
    """
    账户
    """
    @classmethod
    @auto_log
    def get_token_by_app_name(cls, app_name):
        """
        获取应用token
        :param app_name:
        :return:
        """
        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        return app_token_obj, ''
