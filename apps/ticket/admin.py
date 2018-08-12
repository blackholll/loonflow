from django.contrib import admin

from apps.loon_model_base_admin import LoonModelBaseAdmin
from apps.ticket.models import TicketRecord, TicketFlowLog, TicketCustomField


# Register your models here.


class TicketRecordAdmin(LoonModelBaseAdmin):
    search_fields = ('sn', 'title')
    list_display = ('id', 'sn', 'title', 'workflow_id', 'state_id', 'parent_ticket_id', 'participant_type_id', 'participant') + LoonModelBaseAdmin.list_display


class TicketFlowLogAdmin(LoonModelBaseAdmin):
    search_fields = ('ticket_id',)
    list_display = ('id', 'ticket_id', 'transition_id', 'suggestion', 'participant_type_id', 'participant', 'state_id') + LoonModelBaseAdmin.list_display


class TicketCustomFieldAdmin(LoonModelBaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'ticket_id', 'name', 'field_key') + LoonModelBaseAdmin.list_display


admin.site.register(TicketRecord, TicketRecordAdmin)
admin.site.register(TicketFlowLog, TicketFlowLogAdmin)
admin.site.register(TicketCustomField, TicketCustomFieldAdmin)

