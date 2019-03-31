import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.workflow.models import CustomField
from service.base_service import BaseService
from service.common.log_service import auto_log


class WorkflowCustomFieldService(BaseService):
    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_workflow_custom_field(cls, workflow_id):
        """
        获取工作流的自定义字段信息
        :param workflow_id:
        :return:
        """
        custom_field_queryset = CustomField.objects.filter(workflow_id=workflow_id, is_deleted=0).all()
        format_custom_field_dict = {}
        for custom_field in custom_field_queryset:
            if custom_field.label:
                label = custom_field.label
            else:
                label = '{}'
            format_custom_field_dict[custom_field.field_key] = dict(workflow_id=custom_field.workflow_id, field_type_id=custom_field.field_type_id,
                                                                    field_name=custom_field.field_name,order_id=custom_field.order_id,
                                                                    default_value=custom_field.default_value, description=custom_field.description,
                                                                    field_template=custom_field.field_template, boolean_field_display=custom_field.boolean_field_display,
                                                                    field_choice=custom_field.field_choice, label=label)
        return format_custom_field_dict, ''

    @classmethod
    @auto_log
    def get_workflow_custom_field_name_list(cls, workflow_id):
        """
        获取工作流自定义字段list
        :param workflow_id:
        :return:
        """
        custom_field_queryset = CustomField.objects.filter(workflow_id=workflow_id, is_deleted=0).all()
        return [custom_field.field_key for custom_field in custom_field_queryset], ''

    @classmethod
    @auto_log
    def get_workflow_custom_field_list(cls, workflow_id, query_value, page, per_page):
        """
        获取工作流自定义字段的列表
        :param workflow_id:
        :param query_value:
        :param page:
        :param per_page:
        :return:
        """
        query_params = Q(is_deleted=False, workflow_id=workflow_id)
        if query_value:
            query_params &= Q(field_key__contains=query_value) | Q(description__contains=query_value) |Q(field_name__contains=query_value)

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
            workflow_custom_field_result_restful_list.append(dict(id=workflow_custom_field_result_object.id,
                                                                  field_type_id=workflow_custom_field_result_object.field_type_id,
                                                                  field_key=workflow_custom_field_result_object.field_key,
                                                                  field_name=workflow_custom_field_result_object.field_name,
                                                                  order_id=workflow_custom_field_result_object.order_id,
                                                                  default_value=workflow_custom_field_result_object.default_value,
                                                                  description=workflow_custom_field_result_object.description,
                                                                  field_template=workflow_custom_field_result_object.field_template,
                                                                  boolean_field_display=json.loads(workflow_custom_field_result_object.boolean_field_display),
                                                                  field_choice=json.loads(workflow_custom_field_result_object.field_choice),
                                                                  label=json.loads(workflow_custom_field_result_object.label) if workflow_custom_field_result_object.label else {},
                                                                  creator=workflow_custom_field_result_object.creator,
                                                                  gmt_created=str(workflow_custom_field_result_object.gmt_created)[:19]
                                                                  ))
        return workflow_custom_field_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def add_record(cls, workflow_id, field_type_id, field_key, field_name, order_id, default_value, description, field_template,
                   boolean_field_display, field_choice, label, creator):
        """
        新增记录
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
        return custom_field_obj.id, ''

    @classmethod
    @auto_log
    def edit_record(cls, custom_field_id, workflow_id, field_type_id, field_key, field_name, order_id, default_value, description, field_template,
                   boolean_field_display, field_choice, label, creator):
        """
        新增记录
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
        custom_filed_queryset = CustomField.objects.filter(id=custom_field_id, is_deleted=0)
        if custom_filed_queryset:
            custom_filed_queryset.update(workflow_id=workflow_id, field_type_id=field_type_id, field_key=field_key,
                                         field_name=field_name, order_id=order_id, default_value=default_value,
                                         description=description, field_template=field_template,
                                         boolean_field_display=boolean_field_display,
                                         field_choice=field_choice, label=label)
        return custom_field_id, ''

    @classmethod
    @auto_log
    def delete_record(cls, custom_field_id):
        """
        删除记录
        :param custom_field_id:
        :return:
        """
        custom_field_queryset = CustomField.objects.filter(id=custom_field_id, is_deleted=0)
        if custom_field_queryset:
            custom_field_queryset.update(is_deleted=True)
        return custom_field_id, ''

