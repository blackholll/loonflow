from django.contrib import admin
from django.contrib.auth.models import Group
from apps.account.models import LoonUser, LoonDept, LoonRole, LoonUserRole, AppToken
# Register your models here.
from apps.loon_model_base_admin import LoonModelBaseAdmin


class LoonUserAdmin(LoonModelBaseAdmin):
    list_display = ('id', 'username', 'alias', 'email', 'phone', 'dept_id', 'is_active', 'is_admin') + LoonModelBaseAdmin.list_display
    readonly_fields = ['creator', 'last_login']
    search_fields = ('username',)

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user.username
            # 可用于生成密码，晚点修改下
            obj.set_password(form.cleaned_data['password'])
        obj.save()


class LoonDeptAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'parent_dept_id', 'leader', 'approver') + LoonModelBaseAdmin.list_display


class LoonRoleAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description', 'label') + LoonModelBaseAdmin.list_display


class LoonUserRoleAdmin(LoonModelBaseAdmin):
    search_fields = ('user_id',)
    list_display = ('id', 'user_id', 'role_id') + LoonModelBaseAdmin.list_display


class AppTokenAdmin(LoonModelBaseAdmin):
    search_fields = ('app_name',)
    readonly_fields = ['token', 'creator']
    list_display = ('id', 'app_name', 'token') + LoonModelBaseAdmin.list_display

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user.username
            import uuid
            obj.token = uuid.uuid1()
        obj.save()

admin.site.register(LoonUser, LoonUserAdmin)
admin.site.register(LoonDept, LoonDeptAdmin)
admin.site.register(LoonRole, LoonRoleAdmin)
admin.site.register(LoonUserRole, LoonUserRoleAdmin)
admin.site.register(AppToken, AppTokenAdmin)

admin.site.unregister(Group)
