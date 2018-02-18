from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class LoonPermission(models.Model):
    """
    所有权限
    """
    name = models.CharField('权限名称', max_length=50)
    permission_key = models.CharField('权限标识', max_length=50)
    parent_permission_id = models.IntegerField('父级权限id', default=0)
    description = models.CharField('描述', max_length=100, default='')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class LoonDept(models.Model):
    """
    部门
    """
    name = models.CharField('名称', max_length=50)
    parent_dept_id = models.IntegerField('上级部门id', default=0)
    leader = models.CharField('部门leader', max_length=50, default='')  # user表中的用户名,
    approver = models.CharField('审批人', max_length=100, default='')  # user表中的用户名, 逗号隔开多个user。设置为leader审批时， 优先以审批人为准，如果审批人为空，则取leader

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class LoonDeptPermission(models.Model):
    """
    部门拥有权限
    """
    my_dept_id = models.IntegerField('部门id')
    Permission_id = models.IntegerField('权限id')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class LoonRole(models.Model):
    """
    角色
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=50, default='')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class LoonRolePermission(models.Model):
    """
    角色权限
    """
    role_id = models.IntegerField('角色id')
    permission_id = models.IntegerField('权限id')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)


class LoonUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, dep=0):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class LoonUser(AbstractBaseUser):
    """
    用户
    """
    username = models.CharField('用户名', max_length=50, unique=True)
    alias = models.CharField('姓名', max_length=50, default='')
    email = models.EmailField('邮箱', max_length=255)
    phone = models.CharField('电话', max_length=13, default='')
    dept_id = models.IntegerField('部门id', default=0)
    is_active = models.BooleanField('已激活', default=True)
    is_admin = models.BooleanField('超级管理员', default=False)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    objects = LoonUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        return self.is_active

    def get_short_name(self):
        return self.username

    def get_alias_name(self):
        return self.alias

    def has_perms(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    @property
    def dept_name(self):
        dept_id = self.dept_id
        dept_object = LoonDept.objects.filter(id=dept_id)
        if dept_object:
            return dept_object[0].name
        else:
            return '部门id不存在'


class LoonUserRole(models.Model):
    """
    用户角色
    """
    user_id = models.IntegerField('用户id')
    role_id = models.IntegerField('角色id')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)










