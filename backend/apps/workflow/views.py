import json
import logging
import traceback

from django.views import View
from schema import Schema, Regex, And, Or, Use, Optional
from urllib3 import request

from apps.loon_base_view import BaseView
from service.account.account_base_service import account_base_service_ins
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from service.permission.user_permission import user_permission_check
from service.workflow.workflow_base_service import workflow_base_service_ins
from service.workflow.workflow_component_service import workflow_component_service_ins
from service.workflow.workflow_permission_service import workflow_permission_service_ins

logger = logging.getLogger("django")


class WorkflowView(BaseView):
    @user_permission_check("admin, workflow_admin")
    def get(self, request, *args, **kwargs):
        """
        get workflow list api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = workflow_base_service_ins.get_workflow_list(tenant_id, operator_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(workflow_info_list=result.get("workflow_info_list"), page=
                                        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))

    @user_permission_check('workflow_admin,admin')
    def post(self, request, *args, **kwargs):
        """
        new workflow. include all workflow info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            workflow_id = workflow_base_service_ins.add_workflow(operator_id, tenant_id, request_data_dict)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(workflow_id=workflow_id))

class WorkflowSimpleView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get simple workflow list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = workflow_base_service_ins.get_workflow_list(tenant_id, operator_id, search_value, page, per_page, simple=True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(workflow_info_list=result.get("workflow_info_list"), page=
        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))


class WorkflowInitNodeView(BaseView):
    """
    workflow's init node info
    """
    def get(self, request, *args, **kwargs):
        """
        get workflow's init node info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get("workflow_id")
        try:
            result = workflow_base_service_ins.get_workflow_init_node_rest(workflow_id=workflow_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", result)




class WorkflowVersionsView(BaseView):
    @user_permission_check("admin, workflow_admin")
    def get(self, request, *args, **kwargs):
        workflow_id = kwargs.get("workflow_id")
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        search_value = request.GET.get('search_value', '')
        per_page = int(request.GET.get('per_page', 10)) if request.GET.get('per_page', 10) else 10
        page = int(request.GET.get('page', 1)) if request.GET.get('page', 1) else 1
        try:
            result = workflow_base_service_ins.get_workflow_version_list(workflow_id, tenant_id, operator_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, "", dict(version_info_list=result.get("version_info_list"), page=
                                        result.get("page"), per_page=result.get("per_page"), total=result.get("total")))




class WorkflowDetailView(BaseView):
    @user_permission_check('workflow_admin,admin', workflow_id_source='url')
    def get(self, request, *args, **kwargs):
        """
        获取工作流详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        version_name = request.GET.get('version_name', '')
        
        try:
            workflow_result = workflow_base_service_ins.get_full_definition_info_by_id(tenant_id, workflow_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        
        return api_response(0, '', {'workflow_full_defination':  workflow_result})

    @user_permission_check('workflow_admin,admin', workflow_id_source='url')
    def patch(self, request, *args, **kwargs):
        """
        修改工作流
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_id = kwargs.get('workflow_id')
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')

        try:
            workflow_base_service_ins.update_workflow(operator_id, tenant_id, workflow_id, request_data_dict)
            return api_response(0, "", dict(workflow_id=workflow_id))
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")


        

    @user_permission_check('workflow_admin')
    def delete(self, request, *args, **kwargs):
        """
        删除工作流
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_name = request.META.get('HTTP_APPNAME')
        workflow_id = kwargs.get('workflow_id')
        # 判断是否有工作流的权限
        app_permission, msg = account_base_service_ins.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        flag, result = workflow_base_service_ins.delete_workflow(workflow_id)
        if flag is False:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {}
        return api_response(code, msg, data)
    

class WorkflowTicketCreationFormView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket creation form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        version_name = request.GET.get('version_name', '')
        try:
            result, workflow_metadata = workflow_base_service_ins.get_ticket_creation_form(workflow_id, tenant_id, operator_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, '', dict(form_schema={'component_info_list': result, 'workflow_metadata': workflow_metadata}))
    

class WorkflowTicketCreationActionsView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get ticket creation actions
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        operator_id = request.META.get('HTTP_USERID')
        version_name = request.GET.get('version_name', '')
        try:
            result = workflow_base_service_ins.get_ticket_creation_actions(workflow_id, tenant_id, operator_id, version_name)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, '', dict(actions=result))



class WorkflowProcessSingleSchemaView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get workflow diagram
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        tenant_id = request.META.get('HTTP_TENANTID')
        version_id = request.GET.get('version_id', '')

        try:
            result = workflow_base_service_ins.get_process_single_schema(workflow_id, tenant_id, version_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internel Server Error", {})
        return api_response(0, '', dict(process_schema=result))