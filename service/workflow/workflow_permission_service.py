from apps.workflow.models import WorkflowUserPermission
from service.account.account_base_service import account_base_service_ins
from service.base_service import BaseService
from service.common.common_service import common_service_ins
from service.common.constant_service import constant_service_ins


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
        :param user: 支持多人，多部门
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
        result_queryset = WorkflowUserPermission.objects.filter(permission=permission, user_type=user_type,
                                                                user__in=user.split(','), is_deleted=0).all()
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
        if user_type == 'app' and user == 'loonflow':
            return True, ''
        workflow_query_set = WorkflowUserPermission.objects.filter(
            is_deleted=0, workflow_id=workflow_id, permission=permission, user_type=user_type, user=user).first()
        if workflow_query_set:
            return True, ''
        else:
            if permission == 'api':
                return False, 'app: {} has no api permission for workflow_id: {}'.format(user, workflow_id)
            if permission == 'admin':
                return False, 'user: {} has no admin permission for workflow_id:{}'.format(user, workflow_id)
            if permission == 'intervene':
                return False, 'user: {} has no intervene permission for workflow_id:{}'.format(user, workflow_id)
            if permission == 'view':
                if user_type == 'user':
                    return False, 'user: {} has no view permission for workflow_id:{}'.format(user, workflow_id)
                if user_type == 'department':
                    return False, 'department: {} has no view permission for workflow_id:{}'.format(user, workflow_id)

            return False, 'no permission'

    def get_record_list_by_app_list(self, app_list):
        """
        批量获取应用的workflow权限
        :param app_list:
        :return:
        """
        permission_query_set = WorkflowUserPermission.objects.filter(
            is_deleted=0, permission='api', user_type='app', user__in=app_list).all()
        return True, dict(permission_query_set=permission_query_set)

    def update_app_permission(self, app_name, workflow_ids):
        """
        更新应用的权限
        :param app_name:
        :param workflow_ids:
        :return:
        """
        if workflow_ids:
            workflow_id_list = [int(workflow_id) for workflow_id in workflow_ids.split(',')]
        else:
            workflow_id_list = []
        permission_query_set = WorkflowUserPermission.objects.filter(
            is_deleted=0, permission='api', user_type='app', user=app_name).all()
        exist_workflow_id_list = [permission_query.workflow_id for permission_query in permission_query_set]

        flag, need_add_workflow_list = common_service_ins.list_difference(workflow_id_list, exist_workflow_id_list)

        if flag is False:
            return False, need_add_workflow_list

        flag, need_del_workflow_list = common_service_ins.list_difference(exist_workflow_id_list, workflow_id_list)
        if flag is False:
            return False, need_del_workflow_list

        add_permission_query_list = []
        for workflow_id in need_add_workflow_list:
            add_permission_query_list.append(WorkflowUserPermission(permission='api', user_type='app', user=app_name, workflow_id=workflow_id))
        WorkflowUserPermission.objects.bulk_create(add_permission_query_list)

        WorkflowUserPermission.objects.filter(
            is_deleted=0, permission='api', user_type='app', user=app_name, workflow_id__in=need_del_workflow_list).update(is_deleted=1)

        return True, ''

    def del_app_permission(self, app_name, workflow_ids=None):
        """
        删除应用权限
        :param app_name:
        :param workflow_ids:
        :return:
        """
        if workflow_ids == None:
            WorkflowUserPermission.objects.filter(
                is_deleted=0, permission='api', user_type='app', user=app_name).update(is_deleted=1)
        else:
            WorkflowUserPermission.objects.filter(
                is_deleted=0, permission='api', user_type='app', user=app_name, workflow_id__in=workflow_ids.split(',')).update(is_deleted=1)
        return True, ''

    def manage_workflow_permission_check(self, workflow_id, username, app_name):
        """
        用户是否有管理工作流的权限
        :param workflow_id:
        :param username:
        :param app_name:
        :return:
        """
        # 判断应用是否有工作流的权限
        flag, msg = self.workflow_id_permission_check(workflow_id, 'api', 'app', app_name)
        if flag is False:
            return flag, msg

        # 工作流创建人有管理权限
        from service.workflow.workflow_base_service import workflow_base_service_ins
        flag, workflow_obj = workflow_base_service_ins.get_by_id(workflow_id)
        if workflow_obj.creator == username:
            return True, "creator has workflow's manage permission"
        # 超级管理员拥有所有工作流的管理权限
        flag, user_obj = account_base_service_ins.get_user_by_username(username)
        if flag is False:
            return flag, user_obj
        if user_obj.type_id == constant_service_ins.ACCOUNT_TYPE_SUPER_ADMIN:
            return True, "superuser has all workflow's manage permission"
        flag, msg = self.workflow_id_permission_check(workflow_id, 'admin', 'user', username)
        return flag, msg

workflow_permission_service_ins = WorkflowPermissionService()
