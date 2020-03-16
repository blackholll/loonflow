from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.loon_base_model import BaseModel


class LoonDept(BaseModel):
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

    def get_dict(self):
        dept_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            dept_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias)
        else:
            dept_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        if self.parent_dept_id:
            parent_dept_obj = LoonDept.objects.filter(id=self.parent_dept_id, is_deleted=0).first()
            if parent_dept_obj:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name=parent_dept_obj.name)
            else:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='未知')
        else:
            parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='')
        dept_dict_info['parent_dept_info'] = parent_dept_info

        if self.leader:
            leader_obj = LoonUser.objects.filter(username=self.leader).first()
            if leader_obj:
                dept_dict_info['leader_info'] = {
                    'leader_username': leader_obj.username,
                    'leader_alias': leader_obj.alias,
                    'leader_id': leader_obj.id,
                }
            else:
                dept_dict_info['leader_info'] = {
                    'leader_username': self.leader,
                    'leader_alias': self.leader,
                    'leader_id': 0,
                }
        else:
            dept_dict_info['leader_info'] = {
                'leader_username': '',
                'leader_alias': '',
                'leader_id': 0,
            }

        if self.approver:
            approver_list = self.approver.split(',')
            approver_info_list = []
            for approver in approver_list:
                approver_obj = LoonUser.objects.filter(username=approver).first()
                if approver_obj:
                    approver_info_list.append({
                        'approver_name': approver_obj.username,
                        'approver_alias': approver_obj.alias,
                        'approver_id': approver_obj.id,
                    })
                else:
                    approver_info_list.append({
                        'approver_name': approver,
                        'approver_alias': approver,
                        'approver_id': 0,
                    })
            dept_dict_info['approver_info'] = approver_info_list
        else:
            dept_dict_info['approver_info'] = []

        return dept_dict_info


class LoonRole(BaseModel):
    """
    角色
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=50, default='')

    label = models.CharField('标签', max_length=50, blank=True, default='{}', help_text='因为角色信息也可能是从别处同步过来， 为保证对应关系，同步时可以在此字段设置其他系统中相应的唯一标识,字典的json格式')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        return role_dict_info


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
    is_workflow_admin = models.BooleanField('工作流管理员', default=False)  # 只可以操作自己有权限的工作流、工单

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

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            elif attr == 'dept_id':
                dept_obj = LoonDept.objects.filter(id=getattr(self, attr), is_deleted=0).first()
                dept_name = dept_obj.name if dept_obj else ''
                dict_result['dept_info'] = dict(dept_id=getattr(self, attr), dept_name=dept_name)
            elif attr == 'password':
                pass
            elif attr == 'creator':
                creator_obj = LoonUser.objects.filter(username=getattr(self, attr)).first()
                if creator_obj:
                    dict_result['creator_info'] = dict(creator_id= creator_obj.id, creator_alias=creator_obj.alias, creator_username=creator_obj.username)
                else:
                    dict_result['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, attr))
            else:
                dict_result[attr] = getattr(self, attr)

        return dict_result

    def get_json(self):
        import json
        dict_result = self.get_dict()
        return json.dumps(dict_result)


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class LoonUserRole(BaseModel):
    """
    用户角色
    """
    user_id = models.IntegerField('用户id')
    role_id = models.IntegerField('角色id')

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'


class AppToken(BaseModel):
    """
    App token,用于api调用方授权
    """
    app_name = models.CharField('应用名称', max_length=50)
    token = models.CharField('签名令牌', max_length=50, help_text='后端自动生成')
    workflow_ids = models.CharField('工作流权限id', default='', blank=True, max_length=2000, help_text='有权限的工作流ids,逗号隔开,如1,2,3')
    ticket_sn_prefix = models.CharField('工单流水号前缀', default='loonflow', max_length=20, help_text='工单流水号前缀，如设置为loonflow,则创建的工单的流水号为loonflow_201805130013')
    
    class Meta:
        verbose_name = '调用token'
        verbose_name_plural = '调用token'

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        return role_dict_info
