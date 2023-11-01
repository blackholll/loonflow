from apps.account.models import Tenant, User
from service.base_service import BaseService


class CommonConfigService(BaseService):
    def __init__(self):
        pass

    @classmethod
    def get_common_config(cls, tenant_id, user_id):
        """
        get common config
        :param tenant_id:
        :param user_id:
        :return:
        """
        result = dict()
        tenant_record = Tenant.objects.get(id=tenant_id)
        result["tenant_name"] = tenant_record.name
        result["tenant_icon"] = tenant_record.icon
        result["tenant_domain"] = tenant_record.domain
        result["lang"] = tenant_record.lang
        if user_id:
            user_record = User.objects.ge(id=user_id)
            result["lang"] = user_record.lang
        return result


common_config_service_ins = CommonConfigService()
