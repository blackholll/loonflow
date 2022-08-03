from django.urls import path
from apps.manage.views import *
from django.contrib import admin

urlpatterns = [
    path('', index),
    path('loonadmin/', admin.site.urls),

]
