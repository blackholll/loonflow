import logging
import time
import traceback

import requests
from apps.workflow.models import Hook as WorkflowHook
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins

logger = logging.getLogger("django")
class WorkflowHookService(BaseService):
    @classmethod
    def add_workflow_hook(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, hook_info_list) -> bool:
        """
        add workflow hook
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param hook_info_list:
        :return:
        """
        hook_create_list = []
        for hook_info in hook_info_list:
            hook_create = WorkflowHook(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, creator_id=operator_id,
                                       name=hook_info.get("name"), description=hook_info.get("description"),
                                       url=hook_info.get("url"), token=hook_info.get("token"), events=','.join(hook_info.get("event_list"))
                                       )
            hook_create_list.append(hook_create)
        WorkflowHook.objects.bulk_create(hook_create_list)
        return True

    @classmethod
    def get_workflow_fd_hook_list(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow full definition hook
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        workflow_hook_queryset = WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        workflow_hook_result_list = []
        for workflow_hook_obj in workflow_hook_queryset:
            workflow_hook_result_list.append(
                dict(
                    id=str(workflow_hook_obj.id),
                    name=workflow_hook_obj.name,
                    description=workflow_hook_obj.description,
                    url=workflow_hook_obj.url,
                    token=workflow_hook_obj.token,
                    event_list=workflow_hook_obj.events.split(','),
                )
            )
        return workflow_hook_result_list

    
    @classmethod
    def update_workflow_hook(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, hook_info_list) -> bool:
        """
        update workflow hook
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param hook_info_list:
        :return:
        """
        # need delete removed hook
        exist_hook_queryset = WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        for hook_obj in exist_hook_queryset:
            if hook_obj.name not in [hook_info.get("name") for hook_info in hook_info_list]:
                archive_service_ins.archive_record('workflow_hook', hook_obj, operator_id)
        # need update existed hook
        for hook_info in hook_info_list:
            if WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, id=hook_info.get("id")).exists():
                WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, name=hook_info.get("id")).update(
                    description=hook_info.get("description"),
                    url=hook_info.get("url"),
                    events=','.join(hook_info.get("event_list"))
                )
        # need add new hook
        for hook_info in hook_info_list:
            if not WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, id=hook_info.get("id")).exists():
                WorkflowHook.objects.create(
                    tenant_id=tenant_id,
                    workflow_id=workflow_id,
                    version_id=version_id,
                    name=hook_info.get("name"))
        return True


    @classmethod
    def get_workflow_hook_by_event(cls, tenant_id: str, workflow_id: str, version_id: str, event: str) -> list:
        """
        get workflow's hook filter by event
        :param tenant_id:
        :param workflow_id:
        :param hook_type:
        :return:
        """
        result_list = []
        hook_queryset = WorkflowHook.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        for hook_obj in hook_queryset:
            if event in hook_obj.events.split(","):
                result_list.append(hook_obj)
        return result_list

    @classmethod
    def pre_create_hook(cls, tenant_id: str, operator_id: str, workflow_id: str, version_id: str, request_data_dict: dict) -> bool:
        """
        pre create hook check, to decide whether operator can create a ticket
        :param tenant_id:
        :param operator_id:
        :param workflow_id:
        :param version_id:
        :param request_data_dict:
        :return: {true, ""}, first element is whether user can create ticket, another is the message
        """
        # todo: query workflow info  to get hook info
        result_list = cls.get_workflow_hook_by_event(tenant_id, workflow_id, version_id, "pre_create")
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
