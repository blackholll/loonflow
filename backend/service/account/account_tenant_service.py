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

    @classmethod
    def get_tenant_by_domain(cls, domain):
        """
        get tenant detail info by domain
        :param domain: domain name
        :return: tenant info dict
        """
        try:
            tenant_obj = Tenant.objects.get(domain=domain)
        except Tenant.DoesNotExist:
            # If tenant not found by domain, return default tenant with id '00000000-0000-0000-0000-000000000001'
            try:
                tenant_obj = Tenant.objects.get(id='00000000-0000-0000-0000-000000000001')
            except Tenant.DoesNotExist:
                raise CustomCommonException("Default tenant not found")
            except Exception:
                raise
        except Exception:
            raise
        result = tenant_obj.get_dict()
        res_result = {
            'id': result['id'],
            'name': result['name'],
            'domain': result['domain'],
            'logo_path': result['logo_path'],
        }
        return res_result


account_tenant_service_ins = AccountTenantService()
