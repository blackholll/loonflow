from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apps.ticket import views as ticket_views


urlpatterns = [
    path('ticket_types/', ticket_views.TicketTypeAPIView.as_view()),
    path('format_ticket_types/', ticket_views.FormatTicketTypeAPIView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)