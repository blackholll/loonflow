import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.workflow.models import WorkflowScript
from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowRunScriptService(BaseService):
    """
    工作流执行脚本服务
    """
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_run_script_list(cls, query_value, page, per_page):
        """
        获取执行脚本列表
        :param query_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False)
        if query_value:
            query_params &= Q(name__contains=query_value) | Q(description__contains=query_value)

        run_script_querset = WorkflowScript.objects.filter(query_params).order_by('id')
        paginator = Paginator(run_script_querset, per_page)
        try:
            run_script_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            run_script_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            run_script_result_paginator = paginator.page(paginator.num_pages)
        run_script_result_object_list = run_script_result_paginator.object_list
        run_script_result_restful_list = []
        for run_script_result_object in run_script_result_object_list:
            run_script_result_restful_list.append(dict(id=run_script_result_object.id, name=run_script_result_object.name, description=run_script_result_object.description,
                                                       saved_name=run_script_result_object.saved_name.name, is_active=run_script_result_object.is_active, creator=run_script_result_object.creator, gmt_created=str(run_script_result_object.gmt_created)[:19]))
        return run_script_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)
