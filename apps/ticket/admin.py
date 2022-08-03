from django.contrib import admin

from apps.ticket.models import TicketRecord, TicketFlowLog, TicketCustomField, TicketUser


class TicketRecordAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'workflow_id', 'sn', 'state_id',
        'parent_ticket_id', 'parent_ticket_state_id',
        'participant_type_id', 'participant', 'relation',
        'in_add_node', 'add_node_man', 'script_run_last_result',
        'act_state_id', 'multi_all_person'
    )


class TicketFlowLogAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_id', 'transition_id', 'suggestion', 'participant_type_id',
        'participant', 'state_id', 'intervene_type_id',
        'ticket_data'
    )


class TicketCustomFieldAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'field_key', 'ticket_id', 'field_type_id',
        'char_value', 'int_value', 'float_value', 'bool_value',
        'date_value', 'datetime_value', 'time_value', 'radio_value',
        'checkbox_value', 'select_value', 'multi_select_value',
        'text_value', 'username_value', 'multi_username_value'
    )


class TicketUserAdmin(admin.ModelAdmin):
    list_display = (
        'ticket', 'username', 'in_process', 'worked'
    )


admin.site.register(TicketRecord, TicketRecordAdmin)
admin.site.register(TicketFlowLog, TicketFlowLogAdmin)
admin.site.register(TicketCustomField, TicketCustomFieldAdmin)
admin.site.register(TicketUser, TicketUserAdmin)

