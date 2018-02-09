from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns
from apps.workflow import views as workflow_views


urlpatterns = [
    path('', workflow_views.WorkflowsAPIView.as_view()),
    re_path(r'^(\d+)/$', workflow_views.WorkflowAPIView.as_view()),
    re_path(r'^(\d+)/states/$', workflow_views.WorkflowStatesAPIView.as_view()),
    re_path(r'^(\d+)/states/(\d+)/$', workflow_views.WorkflowStateView.as_view()),
    re_path(r'^upload_chart/$', workflow_views.WorkflowUploadChartView.as_view()),


]
urlpatterns = format_suffix_patterns(urlpatterns)