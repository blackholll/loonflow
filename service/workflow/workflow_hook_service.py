import logging
import time
import traceback

import requests
from apps.loon_base_model import SnowflakeIDGenerator
from apps.workflow.models import WorkflowHook
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.exception.custom_common_exception import CustomCommonException

logger = logging.getLogger("django")
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

    @classmethod
    def get_workflow_hook_by_type(cls, tenant_id: int, workflow_id: int, hook_type: str) -> list:
        """
        get workflow's hook filter by type
        :param tenant_id:
        :param workflow_id:
        :param hook_type:
        :return:
        """
        result_list = []
        hook_queryset = WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id).all()
        for hook_obj in hook_queryset:
            hooks = hook_obj.hooks
            if hook_type in hooks.split(","):
                result_list.append(hook_obj)
        return result_list

    @classmethod
    def pre_create_hook(cls, tenant_id: int, operator_id: int, workflow_id: int, request_data_dict: dict) -> bool:
        """
        pre create hook check, to decide whether operator can create a ticket
        :param tenant_id:
        :param operator_id:
        :param workflow_id:
        :param request_data_dict:
        :return: {true, ""}, first element is whether user can create ticket, another is the message
        """
        # todo: query workflow info  to get hook info
        result_list = cls.get_workflow_hook_by_type(tenant_id, workflow_id, "pre_create")
        for workflow_hook in result_list:
            try:
                request_data_dict['tenant_id'] = tenant_id
                request_data_dict['operator_id'] = operator_id
                request_data_dict['workflow_id'] = workflow_id
                request_data_dict['hook_type'] = "pre_create"
                signature, timestamp = common_service_ins.gen_signature_by_token(workflow_hook.token)
                result = requests.post(workflow_hook.url, json=request_data_dict, timeout=10, headers=dict(signature=signature, timestamp=timestamp)).json()
                if result.get("code") != 0:
                    raise CustomCommonException(result.get("msg"))
            except requests.exceptions.HTTPError as errh:
                logger.error(traceback.format_exc())
                raise CustomCommonException("Pre create hook request exception")
            except requests.exceptions.ConnectionError as errc:
                logger.error(traceback.format_exc())
                raise CustomCommonException("Pre create hook fail: connection error")
            except requests.exceptions.Timeout as errt:
                logger.error(traceback.format_exc())
                raise CustomCommonException("Pre create hook fail: timeout")
            except Exception as e:
                logger.error(traceback.format_exc())
                raise CustomCommonException("Internal Server Error")
        return True





    @classmethod
    def common_hook(cls, tenant_id:int, operator_id:int, workflow_id, request_data_dict)->bool:
        """
        common hook, that mean hook type which will invoke after handle or ticket created
        :param tenant_id:
        :param operator_id:
        :param workflow_id:
        :param request_data_dict:
        :return:
        """
        # todo: finish this hook
        return True








workflow_hook_service_ins = WorkflowHookService()
