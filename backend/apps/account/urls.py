from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.account import views as my_user_views


urlpatterns = [
    path('', my_user_views.MyUserList.as_view()),
    re_path(r'^(\d+)/$', my_user_views.MyUserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)