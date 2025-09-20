from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.loon_base_model import BaseModel, BaseCommonModel
from django.utils.translation import gettext_lazy as _

from apps.workflow.models import Record as WorkflowRecord


class Tenant(BaseModel):
    """
    tenant
    """
    LANG_CHOICE = [
        ("zh-cn", "simple chinese"),
        ("en", "English")
    ]
    parent_tenant = models.ForeignKey("self", db_constraint=False, null=False, default='00000000-0000-0000-0000-000000000000', on_delete=models.DO_NOTHING)
    name = models.CharField("name", max_length=100, null=False, default="", help_text="tenant's name")
    domain = models.CharField("domain", max_length=100, null=False, default="", help_text="the domain of the tenant, such as xxx.com")
    logo_path = models.CharField("logo_path", max_length=100, null=False, default="", help_text="the logo image of the tenant to be displayed on website, such as logo.jpg")
    workflow_limit = models.BigIntegerField("workflow_limit", null=False, default=0)
    ticket_limit = models.BigIntegerField("ticket_limit", null=False, default=0)
    is_active = models.BooleanField("is_active", null=False, default=True)


class UserDept(BaseCommonModel):
    """
    user's dept, if user belong to multiple dept, must have one primary dept
    """
    user = models.ForeignKey("User", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)
    dept = models.ForeignKey("Dept", to_field="id", db_constraint=False, on_delete=models.DO_NOTHING)
    is_primary = models.BooleanField("is_primary", null=False, default=True)


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
        user.tenant_id = '00000000-0000-0000-0000-000000000001'
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
        ("normal", "normal")
    ]
    LANG_CHOICE = [
        ("zh-cn", "Simple Chinese"),
        ("en", "English")
    ]
    USERNAME_FIELD = "email"
    name = models.CharField("name", max_length=50, null=False, default='')
    alias = models.CharField("alias", max_length=50, null=False, default='')
    dept = models.ManyToManyField("Dept", through=UserDept)
    role = models.ManyToManyField("Role", through=UserRole)

    email = models.EmailField("email", max_length=255, null=False, unique=True)
    phone = models.CharField("phone", max_length=50, null=False, default='')
    is_active = models.BooleanField("is_active", null=False, default=True)
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
    parent_dept = models.ForeignKey('self', db_constraint=False, null=False, default='00000000-0000-0000-0000-000000000000', on_delete=models.DO_NOTHING, help_text='default value 00000000-0000-0000-0000-000000000000 means no parent department')
    leader = models.ForeignKey(User, db_constraint=False, null=False, on_delete=models.DO_NOTHING, related_name="dept_leader")

    def get_dict(self):
        dept_dict_info = super().get_dict()
        # Convert UUID fields to string for JSON serialization
        if 'parent_dept_id' in dept_dict_info:
            dept_dict_info['parent_dept_id'] = str(dept_dict_info['parent_dept_id'])

        if self.parent_dept_id and str(self.parent_dept_id) != '00000000-0000-0000-0000-000000000000':
            parent_dept_obj = Dept.objects.filter(id=self.parent_dept_id).first()
            if parent_dept_obj:
                parent_dept_info = dict(id=str(self.parent_dept_id), name=parent_dept_obj.name)
            else:
                parent_dept_info = dict(id=str(self.parent_dept_id), name='未知')
        else:
            parent_dept_info = None
        dept_dict_info['parent_dept_info'] = parent_dept_info

        if self.leader_id:
            leader_obj = User.objects.filter(id=self.leader_id).first()
            if leader_obj:
                dept_dict_info['leader_info'] = {
                    'name': leader_obj.name,
                    'alias': leader_obj.alias,
                    'id': str(leader_obj.id),
                }
            else:
                dept_dict_info['leader_info'] = {
                    'name': "",
                    'alias': "",
                    'id': str(self.leader_id),
                }
        else:
            dept_dict_info['leader_info'] = {
            }

        dept_approver_queryset = DeptApprover.objects.filter(dept_id=self.id, tenant_id=self.tenant_id).all()
        approver_id_list = [dept_approver.user_id for dept_approver in dept_approver_queryset]
        approver_list = []
        if approver_id_list:
            approver_queryset = User.objects.filter(id__in=approver_id_list).all()
            for approver_obj in approver_queryset:
                approver_dict = dict()
                approver_dict["id"] = str(approver_obj.id)
                approver_dict["name"] = approver_obj.name
                approver_dict["alias"] = approver_obj.alias
                approver_list.append(approver_dict)
        dept_dict_info["approver_info_list"] = approver_list
        return dept_dict_info


class Role(BaseCommonModel):
    """
    role
    """
    name = models.CharField("role name", max_length=50, null=False, default="")
    description = models.CharField("role description", max_length=200, null=False, default='')
    label = models.CharField("label", max_length=50, blank=True, default="",
                             help_text="label info,you can use set a json data include role info id in your internal system")


class ApplicationWorkflow(BaseCommonModel):
    """application permissioned workflow list"""
    application = models.ForeignKey("Application", db_constraint=False, on_delete=models.DO_NOTHING)
    workflow = models.ForeignKey(WorkflowRecord, db_constraint=False, on_delete=models.DO_NOTHING)


class Application(BaseCommonModel):
    """
    Application which can call loonflow's api. admin type can manage user and manage all workflow
    """
    TYPE_CHOICE = [("admin", "admin"),
                   ("workflow_admin", "workflow_admin")]

    name = models.CharField("name", max_length=50, null=False, default="")
    description = models.CharField("description", max_length=200, null=False, default="")
    token = models.CharField("token", max_length=50, null=False, default="", help_text='token, generated by server')
    type = models.CharField("type", choices=TYPE_CHOICE, max_length=50, null=False, default="admin")

