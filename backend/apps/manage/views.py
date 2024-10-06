import json
import logging
import traceback

from django.http import HttpResponse
from schema import Schema, Optional, And

from apps.loon_base_view import BaseView
from service.exception.custom_common_exception import CustomCommonException
from service.format_response import api_response
from service.manage.common_config_service import common_config_service_ins
from service.manage.notice_service import notice_service_ins
from service.permission.user_permission import user_permission_check

logger = logging.getLogger('django')


def index(request):
    """
    overview
    :param request:
    :return:
    """
    return HttpResponse("This is loonflow's api server, please view frontend page, reference: http://loonflow.readthedocs.io/")


class CommonConfigView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get common config info
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')
        try:
            result = common_config_service_ins.get_common_config(tenant_id, operator_id)
            return api_response(0, "", dict(common_config=result))
        except CustomCommonException as e:
            return api_response(-1, {}, str(e))
        except Exception as e:
            logger.error(traceback.format_exc())
            return api_response(-1, {}, "Internal Server Error")


class NoticeView(BaseView):
    post_schema = Schema({
        "name": str,
        Optional("description"): str,
        "type": And(str, lambda n: n in ["dingtalk", "wecom", "feishu", "hook"], error="type should be dingtalk, wecom, feishu, hook"),
        "extra": dict
    })
    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get notice list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = request.META.get('HTTP_TENANTID')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        search_value = request.GET.get('search_value', '')
        try:
            result = notice_service_ins.get_notice_list(tenant_id, search_value, page, per_page)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, traceback.format_exc(), {})
        return api_response(0, "", result)

    @user_permission_check("admin")
    def post(self, request, *args, **kwargs):
        """
        add notice
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        operator_id = request.META.get('HTTP_USERID')
        tenant_id = request.META.get('HTTP_TENANTID')

        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name', '')
        description = request_data_dict.get('description', '')
        type = request_data_dict.get('type', '')
        extra = request_data_dict.get('extra', '')
        try:
            result = notice_service_ins.add_notice(tenant_id, operator_id, name, description, type, extra)
        except Exception as e:
            return api_response(-1, str(e), {})
        except Exception:
            return api_response(0, "Internal Server Error")
        return api_response(0, "", dict(notice_id=result))

class SimpleNoticeView(BaseView):
    def get(self, request, *args, **kwargs):
        """
        get simple notice list. only return basic info. can be used for select as notice for workflow
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tenant_id = request.META.get('HTTP_TENANTID')
        request_data = request.GET
        page = int(request_data.get('page', 1)) if request_data.get('page', 1) else 1
        per_page = int(request_data.get('per_page', 10)) if request_data.get('per_page', 10) else 10
        search_value = request.GET.get('search_value', '')
        try:
            result = notice_service_ins.get_notice_list(tenant_id, search_value, page, per_page, True)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, traceback.format_exc(), {})
        return api_response(0, "", result)

class NoticeDetailView(BaseView):
    patch_schema = Schema({
        "name": str,
        Optional("description"): str,
        "type": And(str, lambda n: n in ["dingtalk", "wecom", "feishu", "hook"],
                    error="type should be dingtalk, wecom, feishu, hook"),
        "extra": dict
    })

    @user_permission_check("admin")
    def get(self, request, *args, **kwargs):
        """
        get notice list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        notice_id = kwargs.get('notice_id')
        try:
            result = notice_service_ins.get_notice_detail(notice_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "", dict(notice_info=result))

    @user_permission_check("admin")
    def patch(self, request, *args, **kwargs):
        """
        update notice record
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        notice_id = kwargs.get('notice_id')
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        name = request_data_dict.get('name', '')
        description = request_data_dict.get('description', '')
        type = request_data_dict.get('type', '')
        extra = request_data_dict.get('extra', '')
        try:
            notice_service_ins.update_notice(notice_id, name, description, type, extra)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "updated", {})

    @user_permission_check("admin")
    def delete(self, request, *args, **kwargs):
        """
        delete notice
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        notice_id = kwargs.get('notice_id')
        operator_id = request.META.get('HTTP_USERID')
        try:
            notice_service_ins.delete_notice(operator_id, notice_id)
        except CustomCommonException as e:
            return api_response(-1, str(e), {})
        except Exception:
            logger.error(traceback.format_exc())
            return api_response(-1, "Internal Server Error")
        return api_response(0, "deleted", {})