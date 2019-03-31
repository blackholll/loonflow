import json

from django.views import View
from service.format_response import api_response
from service.workflow.workflow_base_service import WorkflowBaseService
from service.workflow.workflow_custom_notice_service import WorkflowCustomNoticeService
from service.workflow.workflow_runscript_service import WorkflowRunScriptService
from service.workflow.workflow_state_service import WorkflowStateService
from service.workflow.workflow_transition_service import WorkflowTransitionService


class WorkflowView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        name = request_data.get('name', '')
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        app_name = request.META.get('HTTP_APPNAME')

        from service.account.account_base_service import AccountBaseService
        permission_workflow_id_list, msg = AccountBaseService.app_workflow_permission_list(app_name)

        workflow_result_restful_list, msg = WorkflowBaseService.get_workflow_list(name, page, per_page, permission_workflow_id_list)
        if workflow_result_restful_list is not False:
            data = dict(value=workflow_result_restful_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增工作流
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        workflow_data = {}
        app_name = request.META.get('HTTP_APPNAME')
        name = request_data_dict.get('name', '')
        description = request_data_dict.get('description', '')
        notices = request_data_dict.get('notices', '')
        view_permission_check = request_data_dict.get('view_permission_check', 1)
        limit_expression = request_data_dict.get('limit_expression', '')
        display_form_str = request_data_dict.get('display_form_str', '')
        creator = request.META.get('HTTP_USERNAME', '')
        result, msg = WorkflowBaseService.add_workflow(name, description, notices, view_permission_check, limit_expression,
                                                       display_form_str, creator)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'workflow_id': result}
        return api_response(code, msg, data)



class WorkflowInitView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流初始状态信息，包括状态详情以及允许的transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制

        app_name = request.META.get('HTTP_APPNAME')
        from service.account.account_base_service import AccountBaseService
        # 判断是否有工作流的权限
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')

        if not (workflow_id and username):
            return api_response(-1, '请提供username', '')
        state_result, msg = WorkflowStateService.get_workflow_init_state(workflow_id)
        if state_result is not False:
            code, msg, data = 0, '', state_result
        else:
            code, msg, data = -1, msg, ''
        return api_response(code, msg, data)


class WorkflowDetailView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        app_name = request.META.get('HTTP_APPNAME')
        from service.account.account_base_service import AccountBaseService
        # 判断是否有工作流的权限
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        workflow_result, msg = WorkflowBaseService.get_by_id(workflow_id)
        if not workflow_result:
            code, msg, data = -1, msg, {}
        else:
            data = dict(name=workflow_result.name, description=workflow_result.description,
                        notices=workflow_result.notices, view_permission_check=workflow_result.view_permission_check,
                        limit_expression=workflow_result.limit_expression,
                        display_form_str=workflow_result.display_form_str, creator=workflow_result.creator,
                        gmt_created=str(workflow_result.gmt_created)[:19])
            code = 0
        return api_response(code, msg, data)

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
        app_name = request.META.get('HTTP_APPNAME')
        workflow_id = kwargs.get('workflow_id')
        from service.account.account_base_service import AccountBaseService
        # 判断是否有工作流的权限
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        name = request_data_dict.get('name', '')
        description = request_data_dict.get('description', '')
        notices = request_data_dict.get('notices', '')
        view_permission_check = request_data_dict.get('view_permission_check', 1)
        limit_expression = request_data_dict.get('limit_expression', '')
        display_form_str = request_data_dict.get('display_form_str', '')

        result, msg = WorkflowBaseService.edit_workflow(workflow_id, name, description, notices, view_permission_check,
                                                        limit_expression, display_form_str)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'workflow_id': result}
        return api_response(code, msg, data)

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
        from service.account.account_base_service import AccountBaseService
        # 判断是否有工作流的权限
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        result, msg = WorkflowBaseService.delete_workflow(workflow_id)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'workflow_id': result}
        return api_response(code, msg, data)


class WorkflowTransitionView(View):
    def get(self, request, *args, **kwargs):
        """
        获取流转
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        # if not username:
        #     return api_response(-1, '请提供username', '')
        result, msg = WorkflowTransitionService.get_transitions_serialize_by_workflow_id(workflow_id, per_page, page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class StateView(View):
    def get(self, request, *args, **kwargs):
        """
        获取状态详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        state_id = kwargs.get('state_id')
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        if not username:
            return api_response(-1, '请提供username', '')

        result, msg = WorkflowStateService.get_restful_state_info_by_id(state_id)
        if result is not False:
            code, data = 0, result
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowStateView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流拥有的state列表信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('workflow_id')
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        # if not username:
        #     return api_response(-1, '请提供username', '')
        result, msg = WorkflowStateService.get_workflow_states_serialize(workflow_id, per_page, page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowRunScriptView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流执行脚本列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        if not username:
            username = request.user.username
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        if not username:
            return api_response(-1, '请提供username', '')
        result, msg = WorkflowRunScriptService.get_run_script_list(search_value, page, per_page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增脚本
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_obj = request.FILES.get('file')
        if file_obj:  # 处理附件上传到方法
            import os
            import uuid
            from django.conf import settings
            script_file_name = "workflow_script/{}.py".format(str(uuid.uuid1()))
            upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
        script_name = request.POST.get('script_name', '')
        script_desc = request.POST.get('script_desc', '')
        is_active = request.POST.get('is_active', '0')
        result, msg = WorkflowRunScriptService.add_run_script(script_name, script_file_name, script_desc, is_active, request.user.username)
        if result is not False:
            data = {}
            code, msg,  = 0, ''
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class WorkflowRunScriptDetailView(View):
    def post(self, request, *args, **kwargs):
        """
        修改脚本,本来准备用patch的。但是发现非json提交过来获取不到数据(因为要传文件，所以不能用json)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_obj = request.FILES.get('file')
        if file_obj:  # 处理附件上传到方法
            import os
            import uuid
            from django.conf import settings
            script_file_name = "workflow_script/{}.py".format(str(uuid.uuid1()))
            upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
        else:
            script_file_name = None
        run_script_id = kwargs.get('run_script_id')
        script_name = request.POST.get('script_name', '')
        script_desc = request.POST.get('script_desc', '')
        is_active = request.POST.get('is_active', '0')
        result, msg = WorkflowRunScriptService.edit_run_script(run_script_id, script_name, script_file_name, script_desc, is_active)
        if result is not False:
            code, msg, data = 0, '', {}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除脚本，本操作不删除对应的脚本文件，只标记记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        run_script_id = kwargs.get('run_script_id')
        result, msg = WorkflowRunScriptService.del_run_script(run_script_id)
        if result is not False:
            code, msg, data = 0, '', {}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class WorkflowCustomNoticeView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流执行脚本列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        if not username:
            username = request.user.username
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        if not username:
            return api_response(-1, '请提供username', '')
        result, msg = WorkflowCustomNoticeService.get_notice_list(search_value, page, per_page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        编辑脚本
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_obj = request.FILES.get('file')
        if file_obj:  # 处理附件上传到方法
            import os
            import uuid
            from django.conf import settings
            script_file_name = "notice_script/{}.py".format(str(uuid.uuid1()))
            upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
        notice_name = request.POST.get('notice_name', '')
        notice_desc = request.POST.get('notice_desc', '')
        title_template = request.POST.get('title_template', '')
        content_template = request.POST.get('content_template', '')
        result, msg = WorkflowCustomNoticeService.add_custom_notice(notice_name, script_file_name, notice_desc, title_template, content_template, request.user.username)
        if result is not False:
            data = {}
            code, msg,  = 0, ''
        else:
            code, data = -1, {}
        return api_response(code, msg, data)


class WorkflowCustomNoticeDetailView(View):
    def post(self, request, *args, **kwargs):
        """
        修改通知脚本,本来准备用patch的。但是发现非json提交过来获取不到数据(因为要传文件，所以不能用json)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_obj = request.FILES.get('file')
        if file_obj:  # 处理附件上传到方法
            import os
            import uuid
            from django.conf import settings
            script_file_name = "notice_script/{}.py".format(str(uuid.uuid1()))
            upload_file = os.path.join(settings.MEDIA_ROOT, script_file_name)
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
        else:
            script_file_name = None
        notice_id = kwargs.get('notice_id')

        notice_name = request.POST.get('notice_name', '')
        notice_desc = request.POST.get('notice_desc', '')
        title_template = request.POST.get('title_template', '')
        content_template = request.POST.get('content_template', '')
        result, msg = WorkflowCustomNoticeService.edit_custom_notice(notice_id, notice_name, script_file_name, notice_desc, title_template, content_template)
        if result is not False:
            code, msg, data = 0, '', {}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除脚本，本操作不删除对应的脚本文件，只标记记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        notice_id = kwargs.get('notice_id')
        result, msg = WorkflowCustomNoticeService.del_custom_notice(notice_id)
        if result is not False:
            code, msg, data = 0, '', {}
        else:
            code, data = -1, {}
        return api_response(code, msg, data)
