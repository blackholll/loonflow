from apps.account.models import Tenant
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException


class AccountTenantService(BaseService):

    @classmethod
    def get_tenant_detail(cls, tenant_id):
        """
        get tenant detail info
        :param tenant_id:
        :return:
        """
        try:
            tenant_obj = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist as e:
            raise CustomCommonException("tenant is not exist or has been deleted")
        except:
            raise
        result = tenant_obj.get_dict()
        result.pop("creator_info")
        return result


account_tenant_service_ins = AccountTenantService()
