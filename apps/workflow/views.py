import json

from django.views import View
from service.format_response import api_response
from service.workflow.workflow_base_service import WorkflowBaseService
from service.workflow.workflow_custom_field_service import WorkflowCustomFieldService
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')

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
        query_value = request_data.get('search_value', '')
        # if not username:
        #     return api_response(-1, '请提供username', '')
        result, msg = WorkflowTransitionService.get_transitions_serialize_by_workflow_id(workflow_id, per_page, page, query_value)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增流转
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
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        transition_type_id = int(request_data_dict.get('transition_type_id', 0))
        timer = int(request_data_dict.get('timer', 0))
        source_state_id = int(request_data_dict.get('source_state_id', 0))
        destination_state_id = int(request_data_dict.get('destination_state_id', 0))
        condition_expression = request_data_dict.get('condition_expression', '')
        attribute_type_id = int(request_data_dict.get('attribute_type_id', 0))
        field_require_check = int(request_data_dict.get('field_require_check', 0))
        alert_enable = int(request_data_dict.get('alert_enable', 0))
        alert_text = request_data_dict.get('alert_text', '')
        result, msg = WorkflowTransitionService.add_workflow_transition(workflow_id, name, transition_type_id, timer, source_state_id,
                                               destination_state_id, condition_expression, attribute_type_id,
                                               field_require_check, alert_enable, alert_text, username)
        if result is not False:
            data = dict(value=dict(transition_id=result))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowTransitionDetailView(View):
    def patch(self, request, *args, **kwargs):
        """
        编辑
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
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        transition_type_id = int(request_data_dict.get('transition_type_id', 0))
        timer = int(request_data_dict.get('timer', 0))
        source_state_id = int(request_data_dict.get('source_state_id', 0))
        destination_state_id = int(request_data_dict.get('destination_state_id', 0))
        condition_expression = request_data_dict.get('condition_expression', '')
        attribute_type_id = int(request_data_dict.get('attribute_type_id', 0))
        field_require_check = int(request_data_dict.get('field_require_check', 0))
        alert_enable = int(request_data_dict.get('alert_enable', 0))
        alert_text = request_data_dict.get('alert_text', '')
        transition_id = kwargs.get('transition_id')
        result, msg = WorkflowTransitionService.edit_workflow_transition(transition_id, workflow_id, name, transition_type_id, timer,
                                                                        source_state_id,
                                                                        destination_state_id, condition_expression,
                                                                        attribute_type_id,
                                                                        field_require_check, alert_enable, alert_text,
                                                                        )
        if result is not False:
            data = dict(value=dict(transition_id=result))
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        transition_id = kwargs.get('transition_id')
        result, msg = WorkflowTransitionService.del_workflow_transition(transition_id)
        if result is not False:
            data = dict(value=dict(transition_id=result))
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        # if not username:
        #     return api_response(-1, '请提供username', '')
        result, msg = WorkflowStateService.get_workflow_states_serialize(workflow_id, per_page, page, search_value)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg,  = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增状态
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
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        sub_workflow_id = request_data_dict.get('sub_workflow_id', 0)
        is_hidden = request_data_dict.get('is_hidden', 0)
        order_id = int(request_data_dict.get('order_id', 0))
        type_id = int(request_data_dict.get('type_id', 0))
        remember_last_man_enable = int(request_data_dict.get('remember_last_man_enable', 0))
        participant_type_id = int(request_data_dict.get('participant_type_id', 0))

        participant = request_data_dict.get('participant', '')
        distribute_type_id = int(request_data_dict.get('distribute_type_id', 1))
        state_field_str = request_data_dict.get('state_field_str', '')
        label = request_data_dict.get('label', '')
        workflow_id = kwargs.get('workflow_id')

        result, msg = WorkflowStateService.add_workflow_state(workflow_id, name, sub_workflow_id, is_hidden, order_id, type_id, remember_last_man_enable,
                           participant_type_id, participant, distribute_type_id, state_field_str, label, username)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'workflow_id': result}
        return api_response(code, msg, data)

class WorkflowStateDetailView(View):
    def patch(self, request, *args, **kwargs):
        """
        编辑状态
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
        username = request.META.get('HTTP_USERNAME')
        name = request_data_dict.get('name', '')
        sub_workflow_id = request_data_dict.get('sub_workflow_id', 0)
        is_hidden = request_data_dict.get('is_hidden', 0)
        order_id = int(request_data_dict.get('order_id', 0))
        type_id = int(request_data_dict.get('type_id', 0))
        remember_last_man_enable = int(request_data_dict.get('remember_last_man_enable', 0))
        participant_type_id = int(request_data_dict.get('participant_type_id', 0))

        participant = request_data_dict.get('participant', '')
        distribute_type_id = int(request_data_dict.get('distribute_type_id', 1))
        state_field_str = request_data_dict.get('state_field_str', '')
        label = request_data_dict.get('label', '')
        workflow_id = kwargs.get('workflow_id')
        state_id = kwargs.get('state_id')

        result, msg = WorkflowStateService.edit_workflow_state(state_id, workflow_id, name, sub_workflow_id, is_hidden,
                                                               order_id, type_id, remember_last_man_enable,
                                                               participant_type_id, participant, distribute_type_id,
                                                               state_field_str, label, username)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'workflow_id': result}
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """
        删除状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_name = request.META.get('HTTP_APPNAME')
        state_id = kwargs.get('state_id')
        result, msg = WorkflowStateService.del_workflow_state(state_id)
        if not result:
            code, msg, data = -1, msg, {}
        else:
            code, msg, data = 0, '', {'state_id': result}
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
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
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
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


class WorkflowCustomFieldView(View):
    def get(self, request, *args, **kwargs):
        """
        获取工作流自定义字段列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        # username = request_data.get('username', '')  # 后续会根据username做必要的权限控制
        username = request.META.get('HTTP_USERNAME')
        if not username:
            username = request.user.username
        search_value = request_data.get('search_value', '')
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        if not username:
            return api_response(-1, '请提供username', '')
        result, msg = WorkflowCustomFieldService.get_workflow_custom_field_list(kwargs.get('workflow_id'), search_value, page, per_page)

        if result is not False:
            data = dict(value=result, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增工作流自定义字段
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        workflow_id = kwargs.get('workflow_id')
        # 判断是否有工作流的权限
        from service.account.account_base_service import AccountBaseService
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        field_key = request_data_dict.get('field_key', '')
        field_name = request_data_dict.get('field_name', '')
        field_type_id = request_data_dict.get('field_type_id', '')
        order_id = int(request_data_dict.get('order_id', 0))
        label = request_data_dict.get('label', '')
        description = request_data_dict.get('description', '')
        field_template = request_data_dict.get('field_template', '')
        default_value = request_data_dict.get('default_value', '')
        boolean_field_display = request_data_dict.get('boolean_field_display', '')
        field_choice = request_data_dict.get('field_choice', '')
        result, msg = WorkflowCustomFieldService.add_record(workflow_id, field_type_id, field_key, field_name, order_id,
                                                            default_value, description, field_template,
                                                            boolean_field_display, field_choice, label, username)

        if result is not False:
            data = dict(value={'custom_field_id': result})
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)


class WorkflowCustomFieldDetailView(View):
    def patch(self, request, *args, **kwargs):
        """
        更新自定义字段
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        custom_field_id = kwargs.get('custom_field_id')
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        workflow_id = kwargs.get('workflow_id')
        # 判断是否有工作流的权限
        from service.account.account_base_service import AccountBaseService
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        json_str = request.body.decode('utf-8')
        if not json_str:
            return api_response(-1, 'post参数为空', {})
        request_data_dict = json.loads(json_str)
        field_key = request_data_dict.get('field_key', '')
        field_name = request_data_dict.get('field_name', '')
        field_type_id = request_data_dict.get('field_type_id', '')
        order_id = int(request_data_dict.get('order_id', 0))
        label = request_data_dict.get('label', '')
        description = request_data_dict.get('description', '')
        field_template = request_data_dict.get('field_template', '')
        default_value = request_data_dict.get('default_value', '')
        boolean_field_display = request_data_dict.get('boolean_field_display', '')
        field_choice = request_data_dict.get('field_choice', '')
        result, msg = WorkflowCustomFieldService.edit_record(custom_field_id, workflow_id, field_type_id, field_key, field_name, order_id,
                                                            default_value, description, field_template,
                                                            boolean_field_display, field_choice, label, username)

        if result is not False:
            data = dict(value={'custom_field_id': result})
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)

    def delete(self, request, *args, **kwargs):
        """删除记录"""
        app_name = request.META.get('HTTP_APPNAME')
        username = request.META.get('HTTP_USERNAME')
        workflow_id = kwargs.get('workflow_id')
        custom_field_id = kwargs.get('custom_field_id')
        # 判断是否有工作流的权限
        from service.account.account_base_service import AccountBaseService
        app_permission, msg = AccountBaseService.app_workflow_permission_check(app_name, workflow_id)
        if not app_permission:
            return api_response(-1, 'APP:{} have no permission to get this workflow info'.format(app_name), '')
        result, msg = WorkflowCustomFieldService.delete_record(custom_field_id)
        if result is not False:
            data = dict(value={'custom_field_id': result})
            code, msg, = 0, ''
        else:
            code, data = -1, ''
        return api_response(code, msg, data)