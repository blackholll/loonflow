from django.contrib import admin

from apps.workflow.models import Workflow, WorkflowAdmin, State, Transition, CustomField, WorkflowScript, CustomNotice, \
    WorkflowUserPermission


class WorkflowModelAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'notices',
        'view_permission_check', 'limit_expression',
        'display_form_str', 'title_template', 'content_template'
    )


class WorkFlowAdminModelAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'username')


class StateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'workflow_id', 'is_hidden',
        'order_id', 'type_id', 'enable_retreat',
        'remember_last_man_enable', 'participant_type_id',
        'participant', 'distribute_type_id', 'state_field_str',
        'label'
    )


class TransitionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'workflow_id', 'transition_type_id',
        'timer', 'source_state_id', 'destination_state_id',
        'condition_expression', 'attribute_type_id', 'field_require_check',
        'alert_enable', 'alert_text'
    )


class CustomFieldAdmin(admin.ModelAdmin):
    list_display = (
        'workflow_id', 'field_type_id',
        'field_key', 'field_name',
        'order_id', 'default_value'
    )


class WorkflowScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'saved_name')


class CustomNoticeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type_id', 'corpid')


class WorkFlowUserPermissionAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'permission', 'user_type', 'user')


admin.site.register(Workflow, WorkflowModelAdmin)
admin.site.register(WorkflowAdmin, WorkFlowAdminModelAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(WorkflowScript, WorkflowScriptAdmin)
admin.site.register(CustomNotice, CustomNoticeAdmin)
admin.site.register(WorkflowUserPermission, WorkFlowUserPermissionAdmin)
