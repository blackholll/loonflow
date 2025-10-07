from django.urls import path

from apps.workflow.views import WorkflowView, WorkflowInitNodeView, WorkflowVersionsView, WorkflowDetailView, WorkflowTicketCreationFormView, WorkflowTicketCreationActionsView, WorkflowProcessSingleSchemaView

urlpatterns = [
    path('', WorkflowView.as_view()),
    path('/<str:workflow_id>', WorkflowDetailView.as_view()),
    path('/<str:workflow_id>/init_node', WorkflowInitNodeView.as_view()),
    path('/<str:workflow_id>/versions', WorkflowVersionsView.as_view()),
    path('/<str:workflow_id>/ticket_creation_form', WorkflowTicketCreationFormView.as_view()),
    path('/<str:workflow_id>/ticket_creation_actions', WorkflowTicketCreationActionsView.as_view()),
    path('/<str:workflow_id>/process_single_schema', WorkflowProcessSingleSchemaView.as_view()),
]