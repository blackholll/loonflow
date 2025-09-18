from django.urls import path

from apps.workflow.views import WorkflowView, WorkflowSimpleView, WorkflowInitNodeView, WorkflowVersionsView, WorkflowDetailView, WorkflowTicketCreationFormView, WorkflowTicketCreationActionsView, WorkflowProcessSingleSchemaView

urlpatterns = [
    path('', WorkflowView.as_view()),
    path('/<str:workflow_id>', WorkflowDetailView.as_view()),
    path('/<str:workflow_id>/init_node', WorkflowInitNodeView.as_view()),
    path('/<str:workflow_id>/versions', WorkflowVersionsView.as_view()),
    path('/<str:workflow_id>/ticket_creation_form', WorkflowTicketCreationFormView.as_view()),
    path('/<str:workflow_id>/ticket_creation_actions', WorkflowTicketCreationActionsView.as_view()),
    path('/<str:workflow_id>/process_single_schema', WorkflowProcessSingleSchemaView.as_view()),

    # path('/user_admin', WorkflowUserAdminView.as_view()),
    # path('/<int:workflow_id>/init_state', WorkflowInitView.as_view()),
    # path('/<int:workflow_id>', WorkflowDetailView.as_view()),
    # path('/<int:workflow_id>/states', WorkflowStateView.as_view()),
    # path('/<int:workflow_id>/simple_states', WorkflowSimpleStateView.as_view()),
    # path('/<int:workflow_id>/can_intervene', WorkflowCanInterveneView.as_view()),
    # path('/<int:workflow_id>/states/<int:state_id>', WorkflowStateDetailView.as_view()),
    # path('/<int:workflow_id>/transitions', WorkflowTransitionView.as_view()),
    # path('/<int:workflow_id>/transitions/<int:transition_id>', WorkflowTransitionDetailView.as_view()),
    # path('/<int:workflow_id>/custom_fields', WorkflowCustomFieldView.as_view()),
    # path('/<int:workflow_id>/custom_fields/<int:custom_field_id>', WorkflowCustomFieldDetailView.as_view()),
    # path('/<int:workflow_id>/simple_description', WorkflowSimpleDescriptionView.as_view()),
    # path('/<int:workflow_id>/statistics', WorkflowStatisticsView.as_view()),
    #
    # path('/states/<int:state_id>', StateView.as_view()),
    # path('/run_scripts', WorkflowRunScriptView.as_view()),
    # path('/run_scripts/<int:run_script_id>', WorkflowRunScriptDetailView.as_view()),
    # path('/custom_notices', WorkflowCustomNoticeView.as_view()),
    # path('/simple_custom_notices', SimpleWorkflowCustomNoticeView.as_view()),
    # path('/custom_notices/<int:notice_id>', WorkflowCustomNoticeDetailView.as_view()),


]