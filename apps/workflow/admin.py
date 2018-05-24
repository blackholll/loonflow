from django.contrib import admin

# Register your models here.
from apps.loon_model_base_admin import LoonModelBaseAdmin
from apps.workflow.models import Workflow, State, Transition, CustomField, WorkflowScript


class WorkflowAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description') + LoonModelBaseAdmin.list_display


class StateAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'order_id', 'type_id', 'workflow_id', 'sub_workflow_id', 'distribute_type_id', 'is_hidden', ) + LoonModelBaseAdmin.list_display


class TransitionAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'workflow_id', 'transition_type_id', 'source_state_id', 'destination_state_id', 'alert_enable') + LoonModelBaseAdmin.list_display


class CustomFieldAdmin(LoonModelBaseAdmin):
    search_fields = ('workflow_id',)
    list_display = ('id', 'workflow_id', 'field_type_id', 'field_key', 'field_name', 'order_id') + LoonModelBaseAdmin.list_display


class WorkflowScriptAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'description', 'is_active') + LoonModelBaseAdmin.list_display


# class CustomNoticeAdmin(LoonModelBaseAdmin):
#     search_fields = ('name',)
#     list_display = ('name', 'description') + LoonModelBaseAdmin.list_display


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(WorkflowScript, WorkflowScriptAdmin)
# admin.site.register(CustomNotice, CustomNoticeAdmin)
