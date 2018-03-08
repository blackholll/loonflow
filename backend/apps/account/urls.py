from django.urls import path, re_path,include
from rest_framework.routers import DefaultRouter

from apps.account import views


router = DefaultRouter()
router.register('users', views.LoonUserViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]
