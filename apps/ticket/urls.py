from django.urls import path
from apps.ticket.views import TicketListView, ticketlist
from apps.ticket import views as ticket_views


urlpatterns = [
    path('', TicketListView.as_view()),
    path('/s', ticketlist),
]