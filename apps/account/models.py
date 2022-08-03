from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from apps.loon_base_model import BaseModel
from apps.workflow.models import Workflow
from django.utils.translation import gettext_lazy as _


class LoonDept(BaseModel):
    """
    Department
    """
    name = models.CharField(_('name'), max_length=50, help_text=_('Department name'))
    parent_dept_id = models.IntegerField(_('parent_dept_id'), blank=True, default=0)
    leader = models.CharField(
        _('leader'), max_length=50, blank=True, default='',
        help_text=_('The leader of the department, the username in the loonuser table')
    )

    approver = models.CharField(
        _('approver'), max_length=100, blank=True, default='',
        help_text=_('The username in the loonuser table, with commas separating multiple users.'
                    ' When the workflow is set to leader approval, the approver shall prevail.'
                    ' If the approver is empty, the leader shall be selected.')
    )

    label = models.CharField(
        _('label'), max_length=50, blank=True, default='',
        help_text=_('Because the department information is generally synchronized from other places,'
                    ' in order to ensure the corresponding relationship,'
                    ' you can set the corresponding unique identifier in other systems'
                    ' in this field during synchronization.')
    )

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
                parent_dept_info = dict(parent_dept_id=self.parent_dept_id, parent_dept_name='unknown')
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
    Role
    """
    name = models.CharField(_('name'), max_length=50)
    description = models.CharField(_('description'), max_length=50, default='')
    label = models.CharField(
        _('label'), max_length=50, blank=True, default='{}',
        help_text=_('Because the role information may also be synchronized from other places,'
                    ' in order to ensure the corresponding relationship,'
                    ' you can set the corresponding unique identifier'
                    ' in other systems in this field during synchronization, and the json format of the dictionary')
    )

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


class LoonUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, dep=0):
        if not email:
            raise ValueError(_('Users must have an email address'))
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.type_id = 2
        user.save(using=self._db)
        return user


class LoonUser(AbstractBaseUser, BaseModel):
    """
    User
    """
    username = models.CharField(_('username'), max_length=50, unique=True)
    alias = models.CharField(_('alias'), max_length=50, default='')
    email = models.EmailField(_('email'), max_length=255)
    phone = models.CharField(_('phone'), max_length=13, default='')
    is_active = models.BooleanField(_('is_active'), default=True)
    type_id = models.IntegerField(_('type_id'), default=0)  # 见service.common.constant_service中定义

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
        user_dept_queryset = LoonUserDept.objects.filter(user_id=self.id, is_deleted=0).all()
        user_dept_name_list = []
        for user_dept in user_dept_queryset:
            user_dept_name_list.append(user_dept.dept.name)
        return ','.join(user_dept_name_list)

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
                    dict_result['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                       creator_username=creator_obj.username)
                else:
                    dict_result['creator_info'] = dict(creator_id=0, creator_alias='',
                                                       creator_username=getattr(self, attr))
            else:
                dict_result[attr] = getattr(self, attr)

        return dict_result

    def get_json(self):
        import json
        dict_result = self.get_dict()
        return json.dumps(dict_result)


class LoonUserDept(BaseModel):
    """
    User department
    """
    user = models.ForeignKey(LoonUser, to_field='id', db_constraint=False, on_delete=False)
    dept = models.ForeignKey(LoonDept, to_field='id', db_constraint=False, on_delete=False)


class LoonUserRole(BaseModel):
    """
    user role
    """
    user_id = models.IntegerField(_('user_id'))
    role_id = models.IntegerField(_('role_id'))


class AppToken(BaseModel):
    """
    App token,for api caller authorization
    """
    app_name = models.CharField('app_name', max_length=50)
    token = models.CharField(
        'token', max_length=50,
        help_text=_('Automatic backend generation')
    )
    ticket_sn_prefix = models.CharField(
        'ticket_sn_prefix', default='loonflow', max_length=20,
        help_text=_('Work order serial number prefix, if set to loonflow,'
                    ' the serial number of the created work order is loonflow_201805130013')
    )

    def get_dict(self):
        role_dict_info = super().get_dict()
        creator_obj = LoonUser.objects.filter(username=getattr(self, 'creator')).first()
        if creator_obj:
            role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
                                                  creator_username=creator_obj.username)
        else:
            role_dict_info['creator_info'] = dict(
                creator_id=0, creator_alias='',
                creator_username=getattr(self, 'creator')
            )
        return role_dict_info
