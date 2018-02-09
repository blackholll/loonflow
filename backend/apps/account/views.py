from rest_framework.views import APIView
from apps.account.models import MyUser
from apps.account.serializers import MyUserSerializer
from rest_framework import status
from service import format_response
from rest_framework.permissions import IsAuthenticated,AllowAny


class MyUserDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        print(request.user.username)
        user = MyUser.objects.filter(is_deleted=False, id=pk)
        if user:
            data = MyUserSerializer(user.first())
            msg = ''
        else:
            data = {}
            msg = '不存在或已删除'
        return format_response.JsonResponse(data=data.data, code=status.HTTP_200_OK, msg=msg)


class MyUserList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print(request.COOKIES)
        args = request.GET
        per_page = int(args.get('per_page', 10)) if args.get('per_page', 10) else 10
        page = int(args.get('page', 1)) if args.get('page', 1) else 1

        total = MyUser.objects.filter(is_deleted=False).count()

        user_serializer_list = [MyUserSerializer(user) for user in MyUser.objects.filter(is_deleted=False)]
        user_serializer_list = [user_serializer.data for user_serializer in user_serializer_list]

        return format_response.JsonResponse(data=user_serializer_list, code=status.HTTP_200_OK,
                                            msg='', per_page=per_page, page=page, total=total)

