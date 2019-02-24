from django.urls import path
from apps.manage.views import *

urlpatterns = [
    path('', index),
    path('doc', doc_view),
    path('user_manage', user_manage_view),
    path('role_manage', role_manage_view),
    path('dept_manage', dept_manage_view),
]
