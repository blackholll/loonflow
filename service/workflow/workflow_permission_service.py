import time
from apps.loon_base_model import SnowflakeIDGenerator
from apps.workflow.models import WorkflowPermission
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException


class WorkflowPermissionService(BaseService):

    @classmethod
    def add_workflow_permission(cls, tenant_id: int, workflow_id: int, operator_id: int, permission_info: dict):
        """
        add workflow permission
        :param tenant_id:
        :param workflow_id:
        :param operator_id:
        :param permission_info:
        :return:
        """
        permission_create_list = []
        admin_id_list = permission_info.get("admin_id_list")
        intervener_id_list = permission_info.get("intervener_id_list")
        viewer_id_list = permission_info.get("viewer_id_list")
        viewer_dept_id_list = permission_info.get("viewer_dept_id_list")
        for admin_id in admin_id_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            permission_id = SnowflakeIDGenerator()()
            permission_create = WorkflowPermission(id=permission_id, tenant_id=tenant_id, workflow_id=workflow_id,
                                                   permission="admin", target_type="user", target=admin_id,
                                                   creator_id=operator_id
                                                   )
            permission_create_list.append(permission_create)

        for intervener_id in intervener_id_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            permission_id = SnowflakeIDGenerator()()
            permission_create = WorkflowPermission(id=permission_id, tenant_id=tenant_id, workflow_id=workflow_id,
                                                   permission="intervene", target_type="user", target=str(intervener_id),
                                                   creator_id=operator_id
                                                   )
            permission_create_list.append(permission_create)

        for viewer_id in viewer_id_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            permission_id = SnowflakeIDGenerator()()
            permission_create = WorkflowPermission(id=permission_id, tenant_id=tenant_id, workflow_id=workflow_id,
                                                   permission="view", target_type="user", target=str(viewer_id),
                                                   creator_id=operator_id)
            permission_create_list.append(permission_create)

        for viewer_dept_id in viewer_dept_id_list:
            time.sleep(0.01)  # SnowflakeIDGenerator has bug will, just workaround provisionally
            permission_id = SnowflakeIDGenerator()()
            permission_create = WorkflowPermission(id=permission_id, tenant_id=tenant_id, workflow_id=workflow_id,
                                                   permission="view", target_type="dept", target=str(viewer_dept_id))
            permission_create_list.append(permission_create)
        WorkflowPermission.objects.bulk_create(permission_create_list)
        return True

    @classmethod
    def get_user_permission_workflow_id_list(cls, user_id: int) -> list:
        """
        get user permission workflow id list
        :param user_id:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(permission="admin", user_type="user", target=str(user_id))
        result = [permission.id for permission in permission_queryset]
        return result

    @classmethod
    def app_workflow_permission_check(cls, tenant_id: int, workflow_id: int, app_name: str) -> bool:
        """
        check whether app has permission for workflow
        :param tenant_id:
        :param workflow_id:
        :param app_name:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, permission="api", target=app_name).all()
        if permission_queryset:
            return True
        raise CustomCommonException("app has no permission to this workflow")


workflow_permission_service_ins = WorkflowPermissionService()
