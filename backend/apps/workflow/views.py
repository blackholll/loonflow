# Create your views here.
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.workflow.serializers import WorkflowSerializer, WorkflowStateSerializer
from service import format_response
from rest_framework import status
from service.workflow.workflow_base_service import WorkflowBaseService
from django.conf import settings

from service.workflow.workflow_state_service import WorkflowStateService


class WorkflowsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        request_data = request.GET

        query_value = request_data.get('query_value', '')
        page = int(request_data.get('page', 1)) if request_data.get('page', 0) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10

        workflows, msg = WorkflowBaseService.get_workflows(query_value, per_page, page)

        if workflows is not False:
            workflow_serializer_list = [WorkflowSerializer(workflow) for workflow in workflows]
            workflow_serializer_list = [workflow_serializer.data for workflow_serializer in workflow_serializer_list]
            return format_response.JsonResponse(data=workflow_serializer_list, code=status.HTTP_200_OK,
                                                per_page=msg.get('per_page', ''), page=msg.get('page', ''),
                                                total=msg.get('total', ''))
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg)

    def post(self, request):
        serializer = WorkflowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return format_response.JsonResponse(data=serializer.data, code=status.HTTP_201_CREATED, msg='')
        else:

            return format_response.JsonResponse(data='', code=status.HTTP_400_BAD_REQUEST, msg=serializer._errors)


class WorkflowAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, workflow_id):
        workflow, msg = WorkflowBaseService.get_workflow_by_id(workflow_id)
        workflow_serializer = WorkflowSerializer(workflow).data
        return format_response.JsonResponse(data=workflow_serializer, code=status.HTTP_200_OK, msg=msg)

    def delete(self, request, workflow_id):
        result, msg = WorkflowBaseService.del_workflow_by_id(workflow_id)
        if result:
            return format_response.JsonResponse(data='', code=status.HTTP_200_OK, msg=msg)


class WorkflowUploadChartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            flowchart = request.FILES.get('flowchart', None)
            if not flowchart:
                return format_response.JsonResponse(data='', code=status.HTTP_400_BAD_REQUEST, msg='请选择文件上传')
            import os
            file_name = flowchart.name
            real_name, ext = os.path.splitext(file_name)
            if ext not in ['.jpg', '.jpeg', '.png']:
                return format_response.JsonResponse(data='', code=status.HTTP_400_BAD_REQUEST, msg='仅支持jpg,jpeg,png格式图片上传')

            import time

            new_file_path = os.path.join(settings.MEDIA_ROOT, 'flowchart')
            new_file_name = real_name + '_' + time.strftime('%Y%m%d%H%M%S') + ext
            new_file_path_name = os.path.join(new_file_path, new_file_name)
            if not os.path.exists(new_file_path):
                os.makedirs(new_file_path)

            f = open(new_file_path_name, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in flowchart.chunks():  # 分块写入文件
                f.write(chunk)
            f.close()
            return format_response.JsonResponse(data={'file_name': new_file_name}, code=status.HTTP_200_OK, msg='')
        except Exception as e:
            import logging
            import traceback
            logging.error(traceback.format_exc())
            return format_response.JsonResponse(data='', code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=e.__str__())


class WorkflowStatesAPIView(APIView):
    """
    工单状态s
    """
    permission_classes = [AllowAny]

    def get(self, request, workflow_id):
        states, msg = WorkflowStateService.get_workflow_states(workflow_id)
        if states is not False:
            workflow_state_serializer_list = [WorkflowStateSerializer(state) for state in states]
            workflow_state_serializer_list = [workflow_state_serializer.data for workflow_state_serializer in workflow_state_serializer_list]
            return format_response.JsonResponse(data=workflow_state_serializer_list, code=status.HTTP_200_OK)
        else:
            return format_response.JsonResponse(data='', code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg)


class WorkflowStateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, workflow_id, state_id):
        state, msg = WorkflowStateService.get_workflow_state_by_id(state_id)
        if state:
            result = WorkflowStateSerializer(state).data
            return format_response.JsonResponse(data=result, code=status.HTTP_200_OK)
        if state is None:
            return format_response.JsonResponse(data=[], code=status.HTTP_200_OK)
        if state is False:
            return format_response.JsonResponse(data='', code=status.HTTP_500_INTERNAL_SERVER_ERROR, msg=msg)

