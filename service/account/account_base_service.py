from apps.account.models import AppToken, LoonUser, LoonUserRole, LoonDept
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
        result = LoonUser.objects.filter(username=username, is_deleted=0).filter()
        return result, ''

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
        user_role_id_list = [user_role.id for user_role in user_role_queryset]
        return user_role_id_list, ''

    @classmethod
    @auto_log
    def get_user_sub_dept_id_list(cls, username):
        """
        获取用户的部门id list，包括所有下级部门
        :param username:
        :return:
        """
        dept_id_list = []

        def iter_dept(dept_id):
            dept_obj = LoonDept.objects.filter(id=dept_id, is_deleted=0).first()
            if dept_obj:
                dept_id_list.append(dept_obj.id)
                if dept_obj.parent_dept_id:
                    iter_dept(dept_obj.parent_dept_id)
        user_obj = LoonUser.objects.filter(username=username, is_deleted=0)
        if user_obj:
            iter_dept()
            return dept_id_list, ''
        else:
            return False, '用户信息不存在'

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
