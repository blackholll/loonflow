from django.urls import path, re_path,include
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from apps.account import views
from apps.account import views as loon_user_views

# router = DefaultRouter()
# router.register('', views.LoonUserListViewSet)
#
# urlpatterns = [
#     path(r'', include(router.urls))
# ]
urlpatterns = [
    path('users/', loon_user_views.LoonUserList.as_view()),
    re_path(r'^users/(\d+)/$', loon_user_views.LoonUserDetail.as_view()),
]
