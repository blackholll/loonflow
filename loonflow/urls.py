"""loonflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from apps.account.views import LoonJwtLoginView


urlpatterns = [
    path('', include('apps.manage.urls')),
    path('manage', include('apps.manage.urls')),
    path('api/v1.0/login', LoonJwtLoginView.as_view()),
    path('api/v1.0/accounts', include('apps.account.urls')),
    path('api/v1.0/tickets', include('apps.ticket.urls')),
    path('api/v1.0/workflows', include('apps.workflow.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
