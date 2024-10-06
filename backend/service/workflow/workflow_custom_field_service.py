import json
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.workflow.models import CustomField
from service.base_service import BaseService
from service.common.log_service import auto_log
from apps.loon_base_model import SnowflakeIDGenerator


class WorkflowCustomFieldService(BaseService):
    @classmethod
    def add_workflow_custom_field(cls, tenant_id: int, workflow_id: int, field_info_list: list):
        """
        add workflow custom field
        :param tenant_id:
        :param workflow_id:
        :param field_info_list:
        :return:
        """
        # todo: need calculate field order
        batch_data = cls.gen_workflow_custom_field_batch_data(tenant_id, workflow_id, 0, field_info_list)
        CustomField.objects.bulk_create(batch_data)
        return True

    @classmethod
    def gen_workflow_custom_field_batch_data(cls, tenant_id: int, workflow_id: int, parent_id: int, field_info_list: list) -> list:
        """
        generate workflow custom field batch insert data
        :param tenant_id:
        :param workflow_id:
        :param workflow_id:
        :param field_info_list:
        :return:
        """
        result_list = []

        for field_info in field_info_list:
            order_id = 0
            new_id = SnowflakeIDGenerator()()

            result_0 = CustomField(tenant_id=tenant_id, workflow_id=workflow_id,
                                   field_type=field_info.get("field_type", ""),
                                   field_key=field_info.get("field_key", ""),
                                   field_name=field_info.get("field_name", ""),
                                   parent_field_id=parent_id,
                                   order_id=order_id,
                                   default_value=field_info.get("default_value", ""),
                                   description=field_info.get("description", ""),
                                   placeholder=field_info.get("placeholder", ""),
                                   props=field_info.get("props", ""),
                                   id=new_id
                                   )
            time.sleep(0.001)  # for SnowflakeIDGenerator's concurrent issue
            order_id += 1
            result_list.append(result_0)
            if field_info.get("children"):
                result_list.extend(cls.gen_workflow_custom_field_batch_data(tenant_id, workflow_id, new_id, field_info.get("children")))

        return result_list

    @classmethod
    def get_workflow_custom_field(cls, workflow_id: int, include_layout: bool=False):
        """

        :param workflow_id:
        :param include_layout:
        :return:
        """
        layout_type_list = ["row", "col"]
        if include_layout is False:
            return CustomField.objects.filter(workflow_id=workflow_id).exclude(field_type__in=layout_type_list)
        else:
            return CustomField.objects.filter(workflow_id=workflow_id)









    @classmethod
    @auto_log
    def get_workflow_custom_field_name_list(cls, workflow_id: int):
        """
        获取工作流自定义字段
        get workflow custom field, field_key list
        :param workflow_id:
        :return:
        """
        custom_field_queryset = CustomField.objects.filter(workflow_id=workflow_id).all()
        return True, dict(
            ticket_custom_field_key_list=[custom_field.field_key for custom_field in custom_field_queryset])

    @classmethod
    @auto_log
    def get_workflow_custom_field_list(cls, workflow_id: int, query_value: str, page: int, per_page: int):
        """
        获取工作流自定义字段的列表
        get workflow custom field restful info list
        :param workflow_id:
        :param query_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False, workflow_id=workflow_id)
        if query_value:
            query_params &= Q(field_key__contains=query_value) | Q(description__contains=query_value) \
                            | Q(field_name__contains=query_value)

        workflow_custom_field_queryset = CustomField.objects.filter(query_params).order_by('id')
        paginator = Paginator(workflow_custom_field_queryset, per_page)
        try:
            workflow_custom_field_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_custom_field_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            workflow_custom_field_result_paginator = paginator.page(paginator.num_pages)

        workflow_custom_field_result_list = workflow_custom_field_result_paginator.object_list
        workflow_custom_field_result_restful_list = []
        for workflow_custom_field_result_object in workflow_custom_field_result_list:
            custom_field_dict = workflow_custom_field_result_object.get_dict()
            custom_field_dict['boolean_field_display'] = json.loads(custom_field_dict['boolean_field_display'])
            custom_field_dict['field_choice'] = json.loads(custom_field_dict['field_choice'])
            custom_field_dict['label'] = json.loads(custom_field_dict['label']) if custom_field_dict['label'] else {}

            workflow_custom_field_result_restful_list.append(custom_field_dict)
        return True, dict(workflow_custom_field_result_restful_list=workflow_custom_field_result_restful_list,
                          paginator_info=dict(per_page=per_page, page=page, total=paginator.count))

    @classmethod
    @auto_log
    def add_record(cls, workflow_id: int, field_type_id: int, field_key: str, field_name: str, order_id: int, default_value: str, description: str, field_template: str,
                   boolean_field_display: str, field_choice: str, label: str, creator: str):
        """
        新增自定义字段记录
        add workflow custom field record
        :param workflow_id:
        :param field_type_id:
        :param field_key:
        :param field_name:
        :param order_id:
        :param default_value:
        :param description:
        :param field_template:
        :param boolean_field_display:
        :param field_choice:
        :param label:
        :param creator:
        :return:
        """
        custom_field_obj = CustomField(workflow_id=workflow_id, field_type_id=field_type_id, field_key=field_key,
                                       field_name=field_name, order_id=order_id, default_value=default_value,
                                       description=description, field_template=field_template,
                                       boolean_field_display=boolean_field_display,
                                       field_choice=field_choice, label=label, creator=creator)
        custom_field_obj.save()
        return True, dict(custom_field_id=custom_field_obj.id)

    @classmethod
    @auto_log
    def edit_record(cls, custom_field_id: int, workflow_id: int, field_type_id: int, field_key: str, field_name: str,
                    order_id: int, default_value: str, description: str, field_template: str,
                    boolean_field_display: str, field_choice: str, label: str)->tuple:
        """
        修改自定义字段记录
        update custom field record
        :param custom_field_id:
        :param workflow_id:
        :param field_type_id:
        :param field_key:
        :param field_name:
        :param order_id:
        :param default_value:
        :param description:
        :param field_template:
        :param boolean_field_display:
        :param field_choice:
        :param label:
        :param creator:
        :return:
        """
        custom_filed_queryset = CustomField.objects.filter(id=custom_field_id)
        if custom_filed_queryset:
            custom_filed_queryset.update(workflow_id=workflow_id, field_type_id=field_type_id, field_key=field_key,
                                         field_name=field_name, order_id=order_id, default_value=default_value,
                                         description=description, field_template=field_template,
                                         boolean_field_display=boolean_field_display,
                                         field_choice=field_choice, label=label)
        return True, ''

    @classmethod
    @auto_log
    def delete_record(cls, custom_field_id: int)->tuple:
        """
        删除记录
        :param custom_field_id:
        :return:
        """
        custom_field_queryset = CustomField.objects.filter(id=custom_field_id)
        if custom_field_queryset:
            custom_field_queryset.update(is_deleted=True)
        return True, ''


workflow_custom_field_service_ins = WorkflowCustomFieldService()
