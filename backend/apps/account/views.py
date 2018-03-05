from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from apps.account.models import LoonUser
from apps.account.serializers import LoonUserSerializer


class LoonUserListPagination(pagination.PageNumberPagination):
    """
    自定义用户列表分页
    """
    max_page_size = 50
    page_size = 10
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'total_pages':self.page.paginator.num_pages,
            'page_size':self.page_size,
            'count':self.page.paginator.count,
            'current_page':self.page.number,
            'value': data

        })

class LoonUserViewSet(viewsets.ModelViewSet):
    """
    用户列表及用户详情
    """
    queryset = LoonUser.objects.filter(is_deleted=False)
    serializer_class = LoonUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LoonUserListPagination

    def finalize_response(self, request, response, *args, **kwargs):
        res = super(LoonUserViewSet, self).finalize_response(request, response, *args, **kwargs)
        if res.status_code < 400:
            res.data = {"code": 200, "msg": "success", "data": response.data}
        elif res.status_code > 400:
            res.data = {"code": res.status_code, "msg": response.data['detail'], "data": {}}
        elif res.status_code == 400:
            res.data = {"code": res.status_code, "msg": response.data, "data": {}}
        return res

