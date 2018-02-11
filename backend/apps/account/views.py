from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from apps.account.models import LoonUser
from apps.account.serializers import LoonUserSerializer


class LoonUserListPagination(PageNumberPagination):
    """
    自定义用户列表分页
    """
    max_page_size = 100
    page_size = 10


class LoonUserListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户列表及用户详情
    """
    queryset = LoonUser.objects.filter(is_deleted=False)
    serializer_class = LoonUserSerializer
    permission_classes = [AllowAny]
    pagination_class = LoonUserListPagination

    def finalize_response(self, request, response, *args, **kwargs):
        res = super(LoonUserListViewSet, self).finalize_response(request, response, *args, **kwargs)
        if res.status_code < 400:
            res.data = {"code": 1, "msg": "success", "data": response.data}
        elif res.status_code > 400:
            res.data = {"code": res.status_code, "msg": response.data['detail'], "data": {}}
        elif res.status_code == 400:
            res.data = {"code": res.status_code, "msg": response.data, "data": {}}
        return res
