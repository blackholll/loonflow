from django.contrib import admin

from apps.account.models import LoonDept, LoonRole, LoonUser, LoonUserDept, LoonUserRole, AppToken


class LoonDepAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'parent_dept_id', 'leader',
        'approver', 'label', 'creator'
    )


class LoonRoleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'label', 'creator'
    )


class LoonUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'alias', 'email', 'phone', 'is_active', 'type_id'
    )


class LoonUserDeptAdmin(admin.ModelAdmin):
    list_display = ('user', 'dept')


class LoonUserRoleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role_id')


class AppTokenAdmin(admin.ModelAdmin):
    list_display = (
        'app_name', 'token', 'ticket_sn_prefix'
    )


admin.site.register(LoonDept, LoonDepAdmin)
admin.site.register(LoonRole, LoonRoleAdmin)
admin.site.register(LoonUser, LoonUserAdmin)
admin.site.register(LoonUserDept, LoonUserDeptAdmin)
admin.site.register(LoonUserRole, LoonUserRoleAdmin)
admin.site.register(AppToken, AppTokenAdmin)
