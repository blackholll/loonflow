from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from apps.workflowjob.models import JobType
from service.base_service import BaseService


class JobTypeService(BaseService):
    """
    工单类别操作
    """
    def __init__(self):
        pass

    @staticmethod
    def get_job_types(query_value='', per_page=10, page=1):
        """
        获取工单类别列表
        :param query_value:
        :param per_page:
        :param page:
        :return:
        """
        if query_value:
            query_params = Q(name__contains=query_value) | Q(description__contains=query_value) & Q(is_deleted=False)
        else:
            query_params = Q(is_deleted=False)

        job_type_objects = JobType.objects.filter(query_params).order_by('id')
        paginator = Paginator(job_type_objects, per_page)
        try:
            job_type_result = paginator.page(page)
        except PageNotAnInteger:
            job_type_result = paginator.page(1)
        except EmptyPage:
            job_type_result = paginator.page(paginator.num_pages)
        return job_type_result, dict(per_page=per_page, page=page, total=paginator.count)

    def get_format_job_types(self, query_value='', per_page=10, page=1):
        """
        获取支持新建的工单类型
        :param query_value:
        :param per_page:
        :param page:
        :return:
        """
        if query_value:
            query_params = Q(name__contains=query_value) | Q(description__contains=query_value) & Q(is_deleted=False) & ~Q(workflow_id=0)
        else:
            query_params = Q(is_deleted=False) & Q(workflow_id=9)

        job_type_objects = JobType.objects.filter(query_params).order_by('id')

        # 格式化工单类型:
        for job_type_object in job_type_objects:
            job_type_object.format_name = self.get_format_job_types_name(job_type_object)

        paginator = Paginator(job_type_objects, per_page)
        try:
            job_type_result = paginator.page(page)
        except PageNotAnInteger:
            job_type_result = paginator.page(1)
        except EmptyPage:
            job_type_result = paginator.page(paginator.num_pages)
        return job_type_result, dict(per_page=per_page, page=page, total=paginator.count)

    def get_format_job_types_name(self, obj):
        """
        获取格式化名称
        :param obj:
        :return:
        """
        if not obj.parent_type_id:
            return obj.name
        parent_type_obj = JobType.objects.filter(id=obj.parent_type_id, is_deleted=False).first()
        return self.get_format_job_types_name(parent_type_obj) + '->' + obj.name


JOB_TYPE_SERVICE = JobTypeService()

