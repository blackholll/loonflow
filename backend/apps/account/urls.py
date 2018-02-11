from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.account import views as loon_user_views


urlpatterns = [
    path('', loon_user_views.LoonUserList.as_view()),
    re_path(r'^(\d+)/$', loon_user_views.LoonUserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)