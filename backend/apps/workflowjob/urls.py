from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.workflowjob import views as workflow_job_views


urlpatterns = [
    url(r'^job_types/$', workflow_job_views.JobTypeAPIView.as_view()),
    url(r'^format_job_types/$', workflow_job_views.FormatJobTypeAPIView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)