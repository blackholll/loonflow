from tests.base import LoonflowTest
from apps.account.models import LoonUser


class TestBaseModel(LoonflowTest):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@test.com"
        self.alias = "test"
        self.password = "test_password"
        self.test_user = LoonUser(username=self.username, email=self.email, alias=self.alias)
        self.test_user.save()

    def test_get_dict(self):
        """
        获取mode的字典格式返回
        :return:
        """
        dict_result = self.test_user.get_dict()
        assert isinstance(dict_result, dict)
