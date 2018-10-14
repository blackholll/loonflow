from apps.account.models import AppToken, LoonUser, LoonUserRole, LoonDept, LoonRole
from service.base_service import BaseService
from service.common.log_service import auto_log


class AccountBaseService(BaseService):
    """
    账户
    """
    @classmethod
    @auto_log
    def get_token_by_app_name(cls, app_name):
        """
        获取应用token
        :param app_name:
        :return:
        """
        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        return app_token_obj, ''

    @classmethod
    @auto_log
    def get_user_by_username(cls, username):
        """
        获取用户信息
        :return:
        """
        result = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if result:
            return result, ''
        else:
            return False, '用户不存在'

    @classmethod
    @auto_log
    def get_user_role_id_list(cls, username):
        """
        获取用户角色id list
        :param username:
        :return:
        """
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, '用户信息不存在'

        user_role_queryset = LoonUserRole.objects.filter(user_id=user_obj.id, is_deleted=0).all()
        user_role_id_list = [user_role.role_id for user_role in user_role_queryset]
        return user_role_id_list, ''

    @classmethod
    @auto_log
    def get_user_up_dept_id_list(cls, username):
        """
        获取用户部门id list,包括上级部门
        :param username:
        :return:
        """
        dept_id_list = []
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, '用户信息不存在'

        def iter_dept(dept_id):
            dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                dept_id_list.append(dept_obj.id)
                if dept_obj.parent_dept_id:
                    iter_dept(dept_obj.parent_dept_id)

        iter_dept(user_obj.dept_id)
        return dept_id_list, ''

    @classmethod
    @auto_log
    def get_user_dept_approver(cls, username):
        """
        获取用户的所在部门的审批人，优先获取审批人，如果没有取tl
        :param username:
        :return:
        """
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0).first()
        loon_dept_obj = LoonDept.objects.filter(id=user_obj.dept_id).first()
        if loon_dept_obj.approver:
            return loon_dept_obj.approver, ''
        else:
            return loon_dept_obj.leader, ''

    @classmethod
    @auto_log
    def get_dept_sub_dept_id_list(cls, dept_id):
        """
        部门所有子部门
        :param dept_id:
        :return:
        """
        dept_id_list = []
        dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
        if dept_obj:
            dept_id_list.append(dept_obj.id)
        else:
            return [], ''

        def iter_dept_id_list(dept_id):
            dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                sub_dept_queryset = LoonDept.objects.filter(parent_dept_id=dept_obj.id, is_deleted=0).all()
                for sub_dept in sub_dept_queryset:
                    if sub_dept:
                        dept_id_list.append(sub_dept.id)
                        iter_dept_id_list(sub_dept.id)

        iter_dept_id_list(dept_id)
        return dept_id_list, ''

    @classmethod
    @auto_log
    def get_dept_username_list(cls, dept_id):
        """
        部门下属用户的username_list:先获取部门的所有下属部门,然后或所有部门下属的人
        """
        sub_dept_id_list, msg = cls.get_dept_sub_dept_id_list(dept_id)
        user_name_list = []
        if sub_dept_id_list:
            user_queryset = LoonUser.objects.filter(dept_id__in = sub_dept_id_list).all()
            for user in user_queryset:
                user_name_list.append(user.username)
        return user_name_list, ''

    @classmethod
    @auto_log
    def get_role_username_list(cls, role_id):
        """
        获取角色对应的username_list
        :param role_id:
        :return:
        """
        user_role_queryset = LoonUserRole.objects.filter(role_id=role_id).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return [], ''
        username_queryset = LoonUser.objects.filter(id__in=(user_id_list)).all()
        username_list = []
        for username_obj in username_queryset:
            username_list.append(username_obj.username)
        return username_list, ''

    @classmethod
    @auto_log
    def get_dept_by_id(cls, dept_id):
        """
        获取部门信息
        :param dept_id:
        :return:
        """
        return LoonDept.objects.filter(id=dept_id, is_deleted=False).first(), ''

    @classmethod
    @auto_log
    def get_role_by_id(cls, role_id):
        """
        获取角色信息
        :param role_id:
        :return:
        """
        return LoonRole.objects.filter(id=role_id, is_deleted=False).first(), ''

    @classmethod
    @auto_log
    def app_workflow_permission_list(cls, app_name):
        """
        应用有权限的workflow_id list
        :param app_name:
        :return:
        """
        app_token_obj = AppToken.objects.filter(app_name=app_name, is_deleted=0).first()
        if not app_token_obj:
            return False, 'app is invalid'
        workflow_ids = app_token_obj.workflow_ids
        if workflow_ids:
            workflow_id_list = workflow_ids.split(',')
            workflow_id_list = [int(workflow_id) for workflow_id in workflow_id_list]
            return workflow_id_list, ''
        else:
            return [], ''

    @classmethod
    @auto_log
    def app_workflow_permission_check(cls, app_name, workflow_id):
        """
        app是否有某类工作流的相关权限的校验
        :param app_name:
        :param workflow_id:
        :return:
        """
        app_workflow_permission_list, msg = cls.app_workflow_permission_list(app_name)
        if app_workflow_permission_list and workflow_id in app_workflow_permission_list:
            return True, ''
        else:
            return False, 'the app has no permission to the workflow_id'

    @classmethod
    @auto_log
    def app_ticket_permission_check(cls, app_name, ticket_id):
        """
        获取调用app是否有某个工单的权限
        :param app_name:
        :param ticket_id:
        :return:
        """
        from service.ticket.ticket_base_service import TicketBaseService
        ticket_obj, msg = TicketBaseService.get_ticket_by_id(ticket_id)
        if not ticket_obj:
            return False, msg
        workflow_id = ticket_obj.workflow_id
        permission_check, msg = cls.app_workflow_permission_check(app_name, workflow_id)
        if not permission_check:
            return False, msg
        return True, ''
