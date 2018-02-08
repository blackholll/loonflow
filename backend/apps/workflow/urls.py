from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.workflow import views as workflow_views


urlpatterns = [
    url(r'^$', workflow_views.WorkflowsAPIView.as_view()),
    url(r'^(\d+)/$', workflow_views.WorkflowAPIView.as_view()),
    url(r'^(\d+)/states/$', workflow_views.WorkflowStatesAPIView.as_view()),
    url(r'^(\d+)/states/(\d+)/$', workflow_views.WorkflowStateView.as_view()),
    url(r'^upload_chart/$', workflow_views.WorkflowUploadChartView.as_view()),


]
urlpatterns = format_suffix_patterns(urlpatterns)