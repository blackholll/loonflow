from django.urls import path
from apps.ticket.views import TicketListView, ticketlist, TicketView
from apps.ticket import views as ticket_views


urlpatterns = [
    path('', TicketListView.as_view()),
    path('/<int:ticket_id>', TicketView.as_view()),
    path('s', ticketlist),
]