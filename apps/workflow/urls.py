from django.urls import path

from apps.workflow.views import StateView, WorkflowView

urlpatterns = [
    path('', WorkflowView.as_view()),
    path('/states/<int:state_id>', StateView.as_view()),

]