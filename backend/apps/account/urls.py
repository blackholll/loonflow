from django.urls import path, re_path

from apps.account import views as loon_user_views

urlpatterns = [
    path('users/', loon_user_views.LoonUserList.as_view()),
    re_path(r'^users/(\d+)/$', loon_user_views.LoonUserDetail.as_view()),
]