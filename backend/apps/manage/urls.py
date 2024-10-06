from django.urls import path
from apps.manage.views import *

urlpatterns = [
    path("", index),
    path("/common", CommonConfigView.as_view()),
    path("/notices", NoticeView.as_view()),
    path("/simple_notices", SimpleNoticeView.as_view()),
    path("/notices/<int:notice_id>", NoticeDetailView.as_view())
]
