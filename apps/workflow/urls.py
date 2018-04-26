from django.urls import path

from apps.workflow.views import StateView

urlpatterns = [
    path('/states/<int:state_id>', StateView.as_view()),
]