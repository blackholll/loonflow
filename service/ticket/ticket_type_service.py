from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from service.base_service import BaseService


class TicketTypeService(BaseService):
    """
    工单类别操作
    """
    def __init__(self):
        pass

    @staticmethod
    def get_ticket_types(query_value='', per_page=10, page=1):
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

        ticket_type_objects = TicketType.objects.filter(query_params).order_by('id')
        paginator = Paginator(ticket_type_objects, per_page)
        try:
            ticket_type_result = paginator.page(page)
        except PageNotAnInteger:
            ticket_type_result = paginator.page(1)
        except EmptyPage:
            ticket_type_result = paginator.page(paginator.num_pages)
        return ticket_type_result, dict(per_page=per_page, page=page, total=paginator.count)

    def get_format_ticket_types(self, query_value='', per_page=10, page=1):
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

        ticket_type_objects = TicketType.objects.filter(query_params).order_by('id')

        # 格式化工单类型:
        for ticket_type_object in ticket_type_objects:
            ticket_type_object.format_name = self.get_format_ticket_types_name(ticket_type_object)

        paginator = Paginator(ticket_type_objects, per_page)
        try:
            ticket_type_result = paginator.page(page)
        except PageNotAnInteger:
            ticket_type_result = paginator.page(1)
        except EmptyPage:
            ticket_type_result = paginator.page(paginator.num_pages)
        return ticket_type_result, dict(per_page=per_page, page=page, total=paginator.count)

    def get_format_ticket_types_name(self, obj):
        """
        获取格式化名称
        :param obj:
        :return:
        """
        if not obj.parent_type_id:
            return obj.name
        parent_type_obj = TicketType.objects.filter(id=obj.parent_type_id, is_deleted=False).first()
        return self.get_format_ticket_types_name(parent_type_obj) + '->' + obj.name


TICKET_TYPE_SERVICE = TicketTypeService()

