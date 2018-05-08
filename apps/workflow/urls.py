from django.urls import path

from apps.workflow.views import StateView, WorkflowView, WorkflowInitView

urlpatterns = [
    path('', WorkflowView.as_view()),
    path('/<int:workflow_id>/init_state', WorkflowInitView.as_view()),
    path('/states/<int:state_id>', StateView.as_view()),

]