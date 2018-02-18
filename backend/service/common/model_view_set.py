from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, authentication, permissions, filters
from service import format_response


class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', True),
            "error": args.get('error', 200),
            "data": args.get('data', []),
            "message": args.get('message', 'success')
        }


class LoonModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            # result1 = self.get_paginated_response(serializer.data)
            result = self.get_paginated_response(serializer.data).data

            return format_response.JsonResponse(data=result['results'], code=status.HTTP_200_OK,
                                                msg='',per_page=1, page=1, total=result['count'])
                                                # msg='', per_page=10, page=1, total=result['count'])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'is_deleted': 1}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def finalize_response(self, request, response, *args, **kwargs):
    #     res = super(LoonModelViewSet, self).finalize_response(request, response, *args, **kwargs)
    #     if res.status_code < 400:
    #         aa = response.data
    #         msg, data = "success", response.data['results']
    #     else:
    #         msg, data = response.data, {}
    #
    #     # if response.data.get('count')
    #     try:
    #         response.data.get('count')
    #         res.data = {"code": res.status_code, "msg": msg, "data": {"value": data, "total": response.data['count']}}
    #     except Exception as e:
    #         res.data = {"code": res.status_code, "msg": msg, "data": {"value": data}}
    #
    #     return res
