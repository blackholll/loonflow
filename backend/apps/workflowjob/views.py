from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from service import format_response
from service.workflowjob.job_type_service import JOB_TYPE_SERVICE, JobTypeService
from apps.workflowjob.serializers import JobTypeSerializer, FormatJobTypeSerializer
from rest_framework import status


class JobTypeAPIView(APIView):
    """
    工单类别
    """
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = request.GET
        query_value = request_data.get('query_value', '')
        page = int(request_data.get('page', 1)) if request_data.get('page', 0) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10

        job_types, msg = JobTypeService.get_job_types(query_value, per_page, page)

        if job_types is not False:
            job_type_serializer_list = [JobTypeSerializer(job_type) for job_type in job_types]

            job_type_serializer_list = [JobTypeSerializer.data for JobTypeSerializer in
                                        job_type_serializer_list]

            return format_response.JsonResponse(data=job_type_serializer_list, code=status.HTTP_200_OK,
                                                per_page=msg.get('per_page', ''), page=msg.get('page', ''),
                                                total=msg.get('total', ''))
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_OK, msg=msg)


class FormatJobTypeAPIView(APIView):
    """
    新建工单选择项目
    """
    permission_classes = [AllowAny]

    def get(self, request):
        request_data = request.GET
        query_value = request_data.get('query_value', '')
        page = int(request_data.get('page', 1)) if request_data.get('page', 0) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10

        job_types, msg = JOB_TYPE_SERVICE.get_format_job_types(query_value, per_page, page)

        if job_types is not False:
            job_type_serializer_list = [FormatJobTypeSerializer(job_type) for job_type in job_types]

            job_type_serializer_list = [JobTypeSerializer.data for JobTypeSerializer in
                                        job_type_serializer_list]

            return format_response.JsonResponse(data=job_type_serializer_list, code=status.HTTP_200_OK,
                                                per_page=msg.get('per_page', ''), page=msg.get('page', ''),
                                                total=msg.get('total', ''))
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_OK, msg=msg)

