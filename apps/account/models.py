from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import gettext_lazy as _

from apps.workflow.models import Workflow


class LoonTenant(BaseModel):
    """
    tenant， timezone: https://blog.csdn.net/whatday/article/details/109856495
    """
    LANG_CHOICE = [("zh-cn", "simple chinese"),
                   ("en", "English")
                   ]
    name = models.CharField(_('name'), max_length=100)
    domain = models.CharField(_('domain'), max_length=100, help_text='the domain of the tenant, such as xxx.com')
    icon = models.CharField(_('icon'), max_length=100, help_text='the icon name of the tenant, such as xxx.jpg')
    timezone = models.CharField(_('timezone'), default="CST", max_length=100)
    lang = models.CharField(_("lang"), choices=LANG_CHOICE, default="zh-cn", max_length=100)
    workflow_limit = models.IntegerField(_("workflow_limit"), default=0),
    ticket_limit = models.IntegerField(_("ticket_limit"), default=0)



class LoonUserDept(BaseModel):
    """
    user's dept
    """
    user = models.ForeignKey("LoonUser", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    dept = models.ForeignKey("LoonDept", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)


class LoonUserRole(BaseModel):
    """
    user's dept
    """
    user = models.ForeignKey("LoonUser", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    role = models.ForeignKey("LoonRole", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)


class DeptApprover(BaseModel):
    """
    department's approver
    """
    dept = models.ForeignKey("LoonDept", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    user = models.ForeignKey("LoonUser", to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)


class LoonUserManager(BaseUserManager):

    # def create_user(self, email, password=None, dep=0):
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     user = self.model(email=self.normalize_email(email))
    #     user.set_password(password)
    #     user.tenant_id = "0"
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.tenant_id = "0"
        user.type = "admin"
        user.save(using=self._db)
        return user


class LoonUser(AbstractBaseUser, BaseModel):
    """
    用户
    """
    TYPE_CHOICE = [
        ("admin", "admin"),
        ("workflow_admin", "workflow_admin"),
        ("common", "common")
    ]
    STATUS_CHOICE = [
        ("in_post", "in_post"),
        ("resigned", "resigned"),
    ]
    USERNAME_FIELD = "email"
    name = models.CharField('name', max_length=50, default='')
    alias = models.CharField('alias', max_length=50, default='')
    tenant = models.ForeignKey(LoonTenant, db_constraint=False, on_delete=models.DO_NOTHING)
    dept = models.ManyToManyField('LoonDept', through=LoonUserDept)
    role = models.ManyToManyField('LoonRole', through=LoonUserRole)

    email = models.EmailField('email', max_length=255, unique=True)
    phone = models.CharField('phone', max_length=13, default='')
    status = models.CharField('status', choices=STATUS_CHOICE)
    type = models.CharField(_("type"), choices=TYPE_CHOICE)
    timezone = models.CharField(_("timezone"), blank=True, default="", null=False)

    objects = LoonUserManager()
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_active

    @property
    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.alias

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


class LoonDept(BaseModel):
    """
    department
    """
    tenant = models.ForeignKey(LoonTenant, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    name = models.CharField('name', max_length=50, help_text='department name')
    parent_dept = models.ForeignKey('self', db_constraint=False, on_delete=models.DO_NOTHING)
    leader = models.ForeignKey(LoonUser, db_constraint=False, on_delete=models.DO_NOTHING)
    label = models.CharField('label', max_length=500, blank=True, default='',
                             help_text='you can use this field for saving some custom info. such as dept id in you internal system')

    def get_dict(self):
        dept_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            dept_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias)
        else:
            dept_dict_info['creator_info'] = dict(creator_id=0, creator_alias='',
                                                  creator_username=getattr(self, 'creator'))
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
    role
    """
    name = models.CharField('role name', max_length=50)
    description = models.CharField('role description', max_length=50, default='')
    label = models.CharField('label', max_length=50, blank=True, default='',
                             help_text='label info,you can use set a json data include role info id in your internal system')

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='',
                                                  creator_username=getattr(self, 'creator'))
        return role_dict_info


class ApplicationWorkflow(BaseModel):
    """application permissioned workflow list"""
    app = models.ForeignKey("Application", db_constraint=False, on_delete=models.DO_NOTHING)
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)


class Application(BaseModel):
    """
    Application which can call loonflow's api
    """
    name = models.CharField('name', max_length=50)
    token = models.CharField('token', max_length=50, help_text='token, generated by server')

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        return role_dict_info

