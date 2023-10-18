from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.loon_base_model import BaseModel, BaseCommonModel
from django.utils.translation import gettext_lazy as _

from apps.workflow.models import Workflow


class Tenant(BaseModel):
    """
    tenant
    """
    LANG_CHOICE = [
        ("zh-cn", "simple chinese"),
        ("en", "English")
    ]
    name = models.CharField("name", max_length=100, null=False, default="", help_text="tenant's name")
    domain = models.CharField("domain", max_length=100, null=False, default="", help_text="the domain of the tenant, such as xxx.com")
    icon = models.CharField("icon", max_length=100, null=False, default="", help_text="the icon name of the tenant, such as xxx.jpg")
    lang = models.CharField("lang", choices=LANG_CHOICE, default="zh-cn", null=False, max_length=100)
    workflow_limit = models.BigIntegerField("workflow_limit", null=False, default=0)
    ticket_limit = models.BigIntegerField("ticket_limit", null=False, default=0)


class UserDept(BaseCommonModel):
    """
    user's dept
    """
    user = models.ForeignKey("User", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)
    dept = models.ForeignKey("Dept", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)


class UserRole(BaseCommonModel):
    """
    user's dept
    """
    user = models.ForeignKey("User", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)
    role = models.ForeignKey("Role", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)


class DeptApprover(BaseCommonModel):
    """
    department's approver
    """
    dept = models.ForeignKey("Dept", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)
    user = models.ForeignKey("User", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)



class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        if not email:
            raise ValueError('User must have an email address')

        # create a new tenant if there is no tenant with id=1
        tenant_queryset = Tenant.objects.filter(id=1).first()
        if not tenant_queryset:
            # default_tenant = Tenant(id=1, name="loonflow", domain="loonapp.com")
            default_tenant = Tenant(name="loonflow", domain="loonapp.com")
            default_tenant.save(using=self._db)
            Tenant.objects.filter(domain="loonapp.com").update(id=1)
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.tenant_id = 1
        user.type = "admin"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseCommonModel):
    """
    User
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
    LANG_CHOICE = [
        ("zh-cn", "simple chinese"),
        ("en", "English")
    ]
    USERNAME_FIELD = "email"
    name = models.CharField("name", max_length=50, null=False, default='')
    alias = models.CharField("alias", max_length=50, null=False, default='')
    tenant = models.ForeignKey(Tenant, db_constraint=False, null=False, on_delete=models.DO_NOTHING)
    dept = models.ManyToManyField("Dept", through=UserDept)
    role = models.ManyToManyField("Role", through=UserRole)

    email = models.EmailField("email", max_length=255, null=False, unique=True)
    phone = models.CharField("phone", max_length=50, null=False, default='')
    status = models.CharField("status", max_length=50, null=False, choices=STATUS_CHOICE)
    type = models.CharField("type", max_length=50, null=False, choices=TYPE_CHOICE)
    avatar = models.CharField("avatar", max_length=500, null=False, default="")
    lang = models.CharField("lang", choices=LANG_CHOICE, null=False, default="zh-cn", max_length=100)

    objects = UserManager()
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_active

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



    def get_json(self):
        import json
        dict_result = self.get_dict()
        return json.dumps(dict_result)


class Dept(BaseCommonModel):
    """
    department
    """
    tenant = models.ForeignKey(Tenant, to_field='id', db_constraint=False, on_delete=models.DO_NOTHING)
    name = models.CharField('name', max_length=50, null=False, default="", help_text='department name')
    parent_dept = models.ForeignKey('self', db_constraint=False, null=False, default=0, on_delete=models.DO_NOTHING)
    leader = models.ForeignKey(User, db_constraint=False, null=False, on_delete=models.DO_NOTHING, related_name="dept_leader")

    def get_dict(self):
        dept_dict_info = super().get_dict()
        creator_obj = User.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            dept_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias)
        else:
            dept_dict_info['creator_info'] = dict(creator_id=0, creator_alias='',
                                                  creator_username=getattr(self, 'creator'))
        if self.parent_dept_id:
            parent_dept_obj = Dept.objects.filter(id=self.parent_dept_id).first()
            if parent_dept_obj:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name=parent_dept_obj.name)
            else:
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='未知')
        else:
            parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='')
        dept_dict_info['parent_dept_info'] = parent_dept_info

        if self.leader:
            leader_obj = User.objects.filter(username=self.leader).first()
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
                approver_obj = User.objects.filter(username=approver).first()
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


class Role(BaseCommonModel):
    """
    role
    """
    name = models.CharField("role name", max_length=50, null=False, default="")
    description = models.CharField("role description", max_length=50, null=False, default='')
    label = models.CharField("label", max_length=50, blank=True, default="",
                             help_text="label info,you can use set a json data include role info id in your internal system")

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = User.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='',
                                                  creator_username=getattr(self, 'creator'))
        return role_dict_info


class ApplicationWorkflow(BaseCommonModel):
    """application permissioned workflow list"""
    app = models.ForeignKey("Application", db_constraint=False, on_delete=models.DO_NOTHING)
    workflow = models.ForeignKey(Workflow, db_constraint=False, on_delete=models.DO_NOTHING)


class Application(BaseCommonModel):
    """
    Application which can call loonflow's api
    """
    name = models.CharField("name", max_length=50, null=False, default="")
    token = models.CharField("token", max_length=50, null=False, default="", help_text='token, generated by server')

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = User.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
        return role_dict_info

