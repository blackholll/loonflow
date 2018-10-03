from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class LoonDept(models.Model):
    """
    部门
    """
    name = models.CharField('名称', max_length=50, help_text='部门名称')
    parent_dept_id = models.IntegerField('上级部门id', blank=True, default=0)
    leader = models.CharField('部门leader', max_length=50, blank=True, default='', help_text='部门的leader, loonuser表中的用户名')
    approver = models.CharField('审批人', max_length=100, blank=True, default='', help_text='loonuser表中的用户名, 逗号隔开多个user。当工作流设置为leader审批时， 优先以审批人为准，如果审批人为空，则取leader')
    label = models.CharField('标签', max_length=50, blank=True, default='', help_text='因为部门信息一般是从别处同步过来， 为保证对应关系，同步时可以在此字段设置其他系统中相应的唯一标识')

    creator = models.CharField('创建人', max_length=50, help_text='loonuser表中的用户名')
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


class LoonRole(models.Model):
    """
    角色
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=50, default='')

    label = models.CharField('标签', max_length=50, blank=True, default='', help_text='因为角色信息也可能是从别处同步过来， 为保证对应关系，同步时可以在此字段设置其他系统中相应的唯一标识')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'


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
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
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

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def dept_name(self):
        dept_id = self.dept_id
        dept_object = LoonDept.objects.filter(id=dept_id)
        if dept_object:
            return dept_object[0].name
        else:
            return '部门id不存在'

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class LoonUserRole(models.Model):
    """
    用户角色
    """
    user_id = models.IntegerField('用户id')
    role_id = models.IntegerField('角色id')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'


class AppToken(models.Model):
    """
    App token,用于api调用方授权
    """
    app_name = models.CharField('应用名称', max_length=50)
    token = models.CharField('签名令牌', max_length=50, help_text='后端自动生成')
    workflow_ids = models.CharField('工作流权限id', default='', blank=True, max_length=2000, help_text='有权限的工作流ids,逗号隔开,如1,2,3')
    ticket_sn_prefix = models.CharField('工单流水号前缀', default='loonflow', max_length=20, help_text='工单流水号前缀，如设置为loonflow,则创建的工单的流水号为loonflow_201805130013')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '调用token'
        verbose_name_plural = '调用token'
