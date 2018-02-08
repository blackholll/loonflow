from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.account import views as my_user_views


urlpatterns = [
    url(r'^$', my_user_views.MyUserList.as_view()),
    url(r'^(\d+)/$', my_user_views.MyUserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)