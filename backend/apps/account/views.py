from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.account.models import LoonUser
from apps.account.serializers import LoonUserSerializer
from apps.account.filters import LoonUserFilter


class LoonUserListPagination(pagination.PageNumberPagination):
    """
    自定义用户列表分页
    page:
        当前页码
    per_page:
        每页记录数
    """
    max_page_size = 50
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response({
            'per_page': int(self.request.query_params['per_page']),  # 每页记录数
            'page': self.page.number,  # 当前页码
            # 'count':self.page.paginator.count,  #总记录数
            # 'total':self.page.paginator.num_pages, #总页数
            'value': data

        })

class LoonUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户列表及用户详情
    """
    queryset = LoonUser.objects.filter(is_deleted=False)
    serializer_class = LoonUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LoonUserListPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = LoonUserFilter

    def finalize_response(self, request, response, *args, **kwargs):
        res = super(LoonUserViewSet, self).finalize_response(request, response, *args, **kwargs)
        if res.status_code < 400:
            res.data = {"code": 200, "msg": "success", "data": response.data}
        elif res.status_code > 400:
            res.data = {"code": res.status_code, "msg": response.data, "data": {}}
        elif res.status_code == 400:
            res.data = {"code": res.status_code, "msg": response.data, "data": {}}
        return res

