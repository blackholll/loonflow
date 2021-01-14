from apps.workflow.models import WorkflowUserPermission
from service.base_service import BaseService


class WorkflowPermissionService(BaseService):
    """
    流程服务
    """
    def __init__(self):
        pass

    def get_workflow_id_list_by_permission(self, permission, user_type, user):
        """
        获取操作权限
        :param permission:
        :param user_type:
        :param user:
        :return:
        """
        if user_type not in ['app', 'user', 'department']:
            return False, 'user type is invalid'

        if not user:
            if user_type == 'app':
                return False, 'app_name is not provided'
            if user_type == 'user':
                return False, 'user is not provided'
            if user_type == 'department':
                return False, 'department is not provided'

        if user == 'loonflow':
            from apps.workflow.models import Workflow
            workflow_query_set = Workflow.objects.filter(is_deleted=0).all()
            workflow_id_list = []
            for workflow_obj in workflow_query_set:
                workflow_id_list.append(workflow_obj.id)
            return True, dict(workflow_id_list=workflow_id_list)
        result_queryset = WorkflowUserPermission.objects.filter(permission=permission, user_type=user_type, user=user, is_deleted=0).all()
        workflow_id_list = [result.workflow_id for result in result_queryset]
        workflow_id_list = list(set(workflow_id_list))
        return True, dict(workflow_id_list=workflow_id_list)

    def workflow_id_permission_check(self, workflow_id, permission, user_type, user):
        """
        检查是否有某workflow_id的权限
        :param workflow_id:
        :param permission:
        :param user_type:
        :param user:
        :return:
        """
        workflow_query_set = WorkflowUserPermission.objects.filter(
            is_deleted=0, workflow_id=workflow_id, permission=permission, user_type=user_type, user=user).first()
        if workflow_query_set:
            return True, ''
        else:
            return False, 'no permission'


workflow_permission_service_ins = WorkflowPermissionService()
