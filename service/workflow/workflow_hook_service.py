import time
from apps.loon_base_model import SnowflakeIDGenerator
from apps.workflow.models import WorkflowHook
from service.base_service import BaseService


class WorkflowHookService(BaseService):
    @classmethod
    def add_workflow_hook(cls, tenant_id: int, workflow_id: int, operator_id: int, hook_info_list) -> bool:
        """
        add workflow hook
        :param tenant_id:
        :param workflow_id:
        :param operator_id:
        :param hook_info_list:
        :return:
        """
        hook_create_list = []
        for hook_info in hook_info_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            hook_id = SnowflakeIDGenerator()()
            hook_create = WorkflowHook(id=hook_id, tenant_id=tenant_id, workflow_id=workflow_id, creator_id=operator_id,
                                       name=hook_info.get("name"), description=hook_info.get("description"),
                                       url=hook_info.get("url"), token=hook_info.get("token"), type=hook_info.get("type")
                                       )
            hook_create_list.append(hook_create)
        WorkflowHook.objects.bulk_create(hook_create_list)
        return True


workflow_hook_service_ins = WorkflowHookService()
