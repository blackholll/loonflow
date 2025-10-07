
from apps.workflow.models import Permission as WorkflowPermission
from service.account.account_user_service import account_user_service_ins
from service.base_service import BaseService
from service.exception.custom_common_exception import CustomCommonException
from service.util.archive_service import archive_service_ins


class WorkflowPermissionService(BaseService):

    @classmethod
    def add_workflow_permission(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, permission_info: dict):
        """
        add workflow permission
        :param tenant_id:
        :param workflow_id:
        :param operator_id:
        :param permission_info:
        :return:
        """
        permission_create_list = []
        admin_id_list = permission_info.get("admin_id_list", [])
        dispatcher_id_list = permission_info.get("dispatcher_id_list", [])
        viewer_id_list = permission_info.get("viewer_id_list", [])
        viewer_dept_id_list = permission_info.get("viewer_dept_id_list", [])
        
        for admin_id in admin_id_list:
            permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="admin", target_type="user", target=admin_id,
                                                   creator_id=operator_id
                                                   )
            permission_create_list.append(permission_create)

        for dispatcher_id in dispatcher_id_list:
            permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="dispatcher", target_type="user", target=str(dispatcher_id),
                                                   creator_id=operator_id
                                                   )
            permission_create_list.append(permission_create)

        for viewer_id in viewer_id_list:
            permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="view", target_type="user", target=str(viewer_id),
                                                   creator_id=operator_id)
            permission_create_list.append(permission_create)

        for viewer_dept_id in viewer_dept_id_list:
            permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="view", target_type="dept", target=str(viewer_dept_id))
            permission_create_list.append(permission_create)
        WorkflowPermission.objects.bulk_create(permission_create_list)
        return True

    @classmethod
    def add_workflow_app_permission(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, authorized_app_id_list:list): 
        """
        add workflow app permission
        :param tenant_id:
        :param workflow_id:
        :param operator_id:
        :param authorized_app_id_list:
        :return:
        """
        permission_create_list = []
        for authorized_app_id in authorized_app_id_list:
            permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="api", target_type="app", target=authorized_app_id,
                                                   creator_id=operator_id)
            permission_create_list.append(permission_create)
        WorkflowPermission.objects.bulk_create(permission_create_list)
        return True
    @classmethod
    def get_workflow_fd_permission(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow full definition permission
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        if permission_queryset:
            permission_result = dict(
                admin_id_list=[permission.target for permission in permission_queryset if permission.permission == 'admin'],
                dispatcher_id_list=[permission.target for permission in permission_queryset if permission.permission == 'dispatcher'],
                viewer_id_list=[permission.target for permission in permission_queryset if permission.permission == 'view'],
                viewer_dept_id_list=[permission.target for permission in permission_queryset if permission.permission == 'view' and permission.target_type == 'dept'],
            )
        else:
            permission_result = dict(
                admin_id_list = [],
                dispatcher_id_list = [],
                viewer_id_list = [],
                viewer_dept_id_list = []
            )
        return permission_result
    
    @classmethod
    def get_workflow_fd_authorized_app_id_list(cls, tenant_id: str, workflow_id: str, version_id: str):
        """
        get workflow full definition permission list
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="api").all()
        authorized_app_id_list = [permission.target for permission in permission_queryset]
        return authorized_app_id_list

    @classmethod
    def get_user_permission_workflow_id_list(cls, user_id: str) -> list:
        """
        get user permission workflow id list
        :param user_id:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(permission="admin", target_type="user", target=user_id, version__type='default')
        result = [permission.id for permission in permission_queryset]
        return result

    @classmethod
    def app_workflow_permission_check(cls, tenant_id: str, workflow_id: str, version_id: str, app_name: str) -> bool:
        """
        check whether app has permission for workflow
        :param tenant_id:
        :param workflow_id:
        :param app_name:
        :return:
        """
        from service.workflow.workflow_base_service import workflow_base_service_ins

        if app_name == "loonflow" and workflow_base_service_ins.get_workflow_record_by_id(tenant_id, workflow_id):
            return True
        permission_queryset = WorkflowPermission.objects.filter(workflow_id=workflow_id, tenant_id=tenant_id, version_id=version_id, permission="api", target=app_name).all()
        if permission_queryset:
            return True
        raise CustomCommonException("app has no permission to this workflow")

    @classmethod
    def user_workflow_permission_check(cls, tenant_id: str, workflow_id: str, version_id: str, user_id: str, permission: str):
        """
        check user whether have permission to special workflow's ticket
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param user_id:
        :param permission:
        :return:
        """
        if permission == 'admin':
            return len(WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, 
                                                         version_id=version_id, permission="admin", target_type="user", target=user_id)) > 0
        elif permission == 'dispatcher':
            return len(WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, 
                                                         version_id=version_id, permission="dispatcher", target_type="user", target=user_id)) > 0
        elif permission == 'view':
            if  len(WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, 
                                                         version_id=version_id, permission="view", target_type="user", target=user_id)) > 0:
                return True
            parent_department_id_list = account_user_service_ins.get_user_parent_dept_id_list(tenant_id, user_id)
            for parent_department_id in parent_department_id_list:
                if len(WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, 
                                                         version_id=version_id, permission="view", target_type="dept", target=parent_department_id)) > 0:
                    return True
            return False
        else:
            return False

    @classmethod
    def get_workflow_id_list_by_permission(cls, permission:str, user_type:str, user:str):
        if user_type not in ['app', 'user', 'department']:
            return False, 'user type is invalid'

        if not user:
            if user_type == 'app':
                raise CustomCommonException('app_name is not provided')
            if user_type == 'user':
                raise CustomCommonException('user is not provided')
            if user_type == 'department':
                raise CustomCommonException('department is not provided')

        if user == 'loonflow':
            from apps.workflow.models import Record as WorkflowRecord
            workflow_query_set = WorkflowRecord.objects.filter().all()
            workflow_id_list = []
            for workflow_obj in workflow_query_set:
                workflow_id_list.append(workflow_obj.id)
            return workflow_id_list
        result_queryset = WorkflowPermission.objects.filter(permission=permission, target_type=user_type,
                                                                target__in=user.split(',')).all()
        workflow_id_list = [result.workflow_id for result in result_queryset]
        workflow_id_list = list(set(workflow_id_list))
        return workflow_id_list

    @classmethod
    def update_workflow_permission(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, permission_info: dict):
        """
        update workflow permission
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param permission_info:
        :return:
        """
        admin_id_list = permission_info.get("admin_id_list", [])
        dispatcher_id_list = permission_info.get("dispatcher_id_list", [])
        viewer_id_list = permission_info.get("viewer_id_list", [])
        viewer_dept_id_list = permission_info.get("viewer_dept_id_list", [])

        ## for deleted
        exist_permission_queryset = WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id).all()
        for permission_obj in exist_permission_queryset:
            if permission_obj.permission == 'admin' and permission_obj.target not in admin_id_list:
                archive_service_ins.archive_record('workflow_permission', permission_obj, operator_id)
            if permission_obj.permission == 'dispatcher' and permission_obj.target not in dispatcher_id_list:
                archive_service_ins.archive_record('workflow_permission', permission_obj, operator_id)
            if permission_obj.permission == 'view' and permission_obj.target not in viewer_id_list:
                archive_service_ins.archive_record('workflow_permission', permission_obj, operator_id)
            if permission_obj.permission == 'view' and permission_obj.target_type == 'dept' and permission_obj.target not in viewer_dept_id_list:
                archive_service_ins.archive_record('workflow_permission', permission_obj, operator_id)


        ## for added
        permission_create_list = []
        for admin_id in admin_id_list:
            if not WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="admin", target_type="user", target=admin_id).exists():
                permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="admin", target_type="user", target=admin_id,
                                                   creator_id=operator_id
                                                   )
                permission_create_list.append(permission_create)
        
        for dispatcher_id in dispatcher_id_list:
            if not WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="dispatcher", target_type="user", target=dispatcher_id).exists():
                permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="dispatcher", target_type="user", target=dispatcher_id,
                                                   creator_id=operator_id
                                                   )
                permission_create_list.append(permission_create)
        for viewer_id in viewer_id_list:
            if not WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="view", target_type="user", target=viewer_id).exists():
                permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="view", target_type="user", target=viewer_id,
                                                   creator_id=operator_id
                                                   )
                permission_create_list.append(permission_create)
        for viewer_dept_id in viewer_dept_id_list:
            if not WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="view", target_type="dept", target=viewer_dept_id).exists():
                permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="view", target_type="dept", target=viewer_dept_id,
                                                   creator_id=operator_id
                                                   )
                permission_create_list.append(permission_create)

        WorkflowPermission.objects.bulk_create(permission_create_list)
        return True

    @classmethod
    def update_workflow_app_permission(cls, tenant_id: str, workflow_id: str, version_id: str, operator_id: str, authorized_app_id_list: list):
        """
        update workflow app permission
        :param tenant_id:
        :param workflow_id:
        :param version_id:
        :param operator_id:
        :param authorized_app_id_list:
        :return:
        """
        # todo: need delete removed permission
        exist_permission_queryset = WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="api").all()
        for permission_obj in exist_permission_queryset:
            if permission_obj.target not in authorized_app_id_list:
                archive_service_ins.archive_record('workflow_permission', permission_obj, operator_id)

        # todo: need add new permission
        permission_create_list = []
        for authorized_app_id in authorized_app_id_list:
            if not WorkflowPermission.objects.filter(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id, permission="api", target_type="app", target=authorized_app_id).exists():
                permission_create = WorkflowPermission(tenant_id=tenant_id, workflow_id=workflow_id, version_id=version_id,
                                                   permission="api", target_type="app", target=authorized_app_id,
                                                   creator_id=operator_id)
                permission_create_list.append(permission_create)
        WorkflowPermission.objects.bulk_create(permission_create_list)
        return True

    @classmethod
    def get_workflow_info_list_by_app_id(cls, tenant_id: str, app_id: str, search_value: str, page: int, per_page: int):
        """
        get workflow id list by app id
        :param tenant_id:
        :param app_name:
        :param search_value:
        :param page:
        :param per_page:
        :return:
        """
        permission_queryset = WorkflowPermission.objects.filter(tenant_id=tenant_id, permission="api", target_type="app", target=app_id).all()
        paginator = Paginator(permission_queryset, per_page)
        try:
            permission_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            permission_result_paginator = paginator.page(1)
        except EmptyPage:
            permission_result_paginator = paginator.page(paginator.num_pages)
        permission_result_list = permission_result_paginator.object_list
        workflow_info_list = []
        for permission_result in permission_result_list:
            workflow_info_list.append(permission_result.workflow.get_dict())
        return dict(workflow_info_list=workflow_info_list, per_page=per_page, page=page, total=paginator.count)


workflow_permission_service_ins = WorkflowPermissionService()
