from django.urls import path
from apps.manage.views import *

urlpatterns = [
    path("", index),
    path("/common", CommonConfigView.as_view()),
    path("/notifications", NotificationView.as_view()),
    path("/simple_notifications", SimpleNotificationView.as_view()),
    path("/notifications/<int:notification_id>", NotificationDetailView.as_view())
]
