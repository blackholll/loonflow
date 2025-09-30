from django.urls import path
from apps.ticket.views import TicketListView,TicketDetailFormView, TicketDetailActionsView, TicketHandleView, TicketFlowHistoryView, TicketCurrentNodeInfosView

urlpatterns = [
    path('', TicketListView.as_view()),
    path('/<str:ticket_id>/ticket_detail_form', TicketDetailFormView.as_view()),
    path('/<str:ticket_id>/ticket_detail_actions', TicketDetailActionsView.as_view()),
    path('/<str:ticket_id>/handle', TicketHandleView.as_view()),
    path('/<str:ticket_id>/ticket_flow_history', TicketFlowHistoryView.as_view()),
    path('/<str:ticket_id>/current_node_infos', TicketCurrentNodeInfosView.as_view()),
]
