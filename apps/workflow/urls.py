from django.urls import path

from apps.workflow.views import StateView, WorkflowView, WorkflowInitView, WorkflowStateView, WorkflowRunScriptView, \
    WorkflowRunScriptDetailView, WorkflowCustomNoticeView, WorkflowCustomNoticeDetailView
from service.workflow.workflow_custom_notice_service import WorkflowCustomNoticeService

urlpatterns = [
    path('', WorkflowView.as_view()),
    path('/<int:workflow_id>/init_state', WorkflowInitView.as_view()),
    path('/<int:workflow_id>/states', WorkflowStateView.as_view()),
    path('/states/<int:state_id>', StateView.as_view()),
    path('/run_scripts', WorkflowRunScriptView.as_view()),
    path('/run_scripts/<int:run_script_id>', WorkflowRunScriptDetailView.as_view()),
    path('/custom_notices', WorkflowCustomNoticeView.as_view()),
    path('/custom_notices/<int:custom_notice_id>', WorkflowCustomNoticeDetailView.as_view()),


]