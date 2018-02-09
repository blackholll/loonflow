from rest_framework import serializers
from apps.account.models import LoonUser


class MyUserSerializer(serializers.ModelSerializer):
    dept_name = serializers.ReadOnlyField()
    gmt_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = LoonUser
        fields = ('id', 'username', 'chinese_name', 'email', 'phone', 'dept_id', 'is_active', 'gmt_modified',
                  'is_deleted', 'dept_name')


