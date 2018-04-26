from django.urls import path
from apps.ticket.views import TicketListView, ticketlist, TicketView, TicketTransition, TicketFlowlog, TicketFlowStep, TicketState, TicketsStates


urlpatterns = [
    path('', TicketListView.as_view()),
    path('/<int:ticket_id>', TicketView.as_view()),
    path('/<int:ticket_id>/transitions', TicketTransition.as_view()),
    path('/<int:ticket_id>/flowlogs', TicketFlowlog.as_view()),
    path('/<int:ticket_id>/flowsteps', TicketFlowStep.as_view()),
    path('/<int:ticket_id>/state', TicketState.as_view()),
    path('/states', TicketsStates.as_view()),  # 批量获取工单状态

    path('s', ticketlist),
]