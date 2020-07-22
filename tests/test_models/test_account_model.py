from django.test import TestCase
from apps.account.models import LoonUser, LoonDept, LoonRole


class TestLoonAccountModel(TestCase):
    fixtures = ['accounts.json']

    def test_loon_user_get_dict(self):
        """
        测试获取字典格式用户信息
        :return:
        """
        test_user1 = LoonUser.objects.get(username='guiji')
        assert isinstance(test_user1.get_dict(), dict)

    def test_loon_user_is_staff(self):
        """
        测试用户staff判断
        :return:
        """
        test_user1 = LoonUser.objects.get(username='guiji')
        assert isinstance(test_user1.is_staff, bool)

    def test_loon_user_get_short_name(self):
        """
        测试获取short_name
        :return:
        """
        test_user1 = LoonUser.objects.get(username='guiji')
        self.assertEqual(test_user1.get_short_name(), 'guiji')

    def test_loon_user_get_alias_name(self):
        """
        测试获取用户昵称
        :return:
        """
        test_user1 = LoonUser.objects.get(username='guiji')
        self.assertEqual(test_user1.get_alias_name(), '轨迹')

    def test_loon_user_dept_name(self):
        """
        测试获取用户部门名称
        :return:
        """
        test_user1 = LoonUser.objects.get(username='admin')
        self.assertEqual(test_user1.dept_name, '总部,技术部')

    def test_loon_user_get_json(self):
        """
        测试获取用户json格式信息
        :return:
        """
        test_user1 = LoonUser.objects.get(username='guiji')
        assert isinstance(test_user1.get_json(), str)

    def test_role_get_dict(self):
        """
        测试获取角色字典信息格式
        :return:
        """
        role = LoonRole.objects.get(name='VPN管理员')
        assert isinstance(role.get_dict(), dict)

    def test_dept_get_dict(self):
        """
        测试获取部门字典信息格式
        :return:
        """
        dept = LoonDept.objects.get(id=1)
        assert isinstance(dept.get_dict(), dict)
