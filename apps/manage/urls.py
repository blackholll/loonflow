from django.urls import path
from apps.manage.views import *

urlpatterns = [
    path('', index),
]
