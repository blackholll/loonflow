from django.urls import path
from apps.manage.views import *

urlpatterns = [
    path('', index),
    path('/login', user_login_view),
    path('/doc', doc_view),
    path('/user_manage', user_manage_view),
    path('/role_manage', role_manage_view),
    path('/dept_manage', dept_manage_view),
    path('/app_token_manage', app_token_manage_view),
    path('/ticket_manage', ticket_manage_view),
    path('/ticket_manage/<int:ticket_id>', ticket_manage_detail_view),
    path('/workflow_manage', workflow_manage_view),
    path('/workflow_manage/<int:workflow_id>', workflow_manage_edit_view),

    path('/run_script_manage', run_script_manage_view),
    path('/notice_manage', notice_manage_view),
    path('/workflow_flow_chart/<int:workflow_id>', workflow_flow_chart_view),
    # path('workflow_flow_chart', workflow_flow_chart_view),
]
