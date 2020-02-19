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
    def get_run_script_list(cls, query_value: str, page: int, per_page: int)->tuple:
        """
        获取执行脚本列表
        get run script list
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
            run_script_result_restful_list.append(dict(
                id=run_script_result_object.id, name=run_script_result_object.name,
                description=run_script_result_object.description, saved_name=run_script_result_object.saved_name.name,
                is_active=run_script_result_object.is_active, creator=run_script_result_object.creator,
                gmt_created=str(run_script_result_object.gmt_created)[:19]))
        return True, dict(run_script_result_restful_list=run_script_result_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_run_script(cls, name: str, saved_name: str, description: str, is_active: int, creator: str)->tuple:
        """
        新增工作流脚本
        add run script
        :param name:
        :param saved_name:
        :param description:
        :param is_active:
        :param creator:
        :return:
        """
        script_obj = WorkflowScript(name=name, saved_name=saved_name, description=description, is_active=is_active,
                                    creator=creator)
        script_obj.save()
        return True, dict(script_id=script_obj.id)

    @classmethod
    @auto_log
    def edit_run_script(cls, run_script_id: int, name: str, saved_name: str, description: str, is_active: int)->tuple:
        """
        更新工作流脚本
        edit run script
        :param run_script_id:
        :param name:
        :param saved_name:
        :param description:
        :param is_active:
        :return:
        """
        script_obj = WorkflowScript.objects.filter(id=run_script_id, is_deleted=0)
        if saved_name:
            script_obj.update(name=name, saved_name=saved_name, description=description, is_active=is_active)
        else:
            script_obj.update(name=name, description=description, is_active=is_active)
        return True, {}

    @classmethod
    @auto_log
    def del_run_script(cls, run_script_id: int)->tuple:
        """
        删除脚本
        delete run script
        :id: 
        :return:
        """
        script_obj = WorkflowScript.objects.filter(id=run_script_id, is_deleted=0)
        if script_obj:
            script_obj.update(is_deleted=True)
            return True, ''
        else:
            return False, 'the record is not exist or has been deleted'

    @classmethod
    @auto_log
    def get_run_script_by_id(cls, run_script_id: int)->tuple:
        """
        根据id获取执行脚本
        get script by id
        :param run_script_id:
        :return:
        """
        script_obj = WorkflowScript.objects.filter(id=run_script_id, is_deleted=0).first()
        return True, dict(script_obj=script_obj)


workflow_run_script_service_ins = WorkflowRunScriptService()
