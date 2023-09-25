import os
import time
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter

machine_id = settings.MACHINE_ID
base_dir = settings.BASE_DIR


class SnowflakeIDGenerator:
    def __init__(self):
        self.machine_flag = machine_id
        self.sequence = 0
        # get clock_flag from file
        clock_flag_file = os.path.join(base_dir,'clock_flag.txt')
        if os.path.exists(clock_flag_file):
            with open(clock_flag_file, 'r') as f:
                try:
                    clock_flag = int(f.read())
                    if clock_flag > 7:
                        raise Exception('clock flag larger then 7')
                except Exception as e:
                    clock_flag = 0
                    with open(clock_flag_file, 'w') as f2:
                        f2.write('0')
        else:
            clock_flag = 0
            with open(clock_flag_file, 'w') as f2:
                f2.write('0')
        self.clock_flag = clock_flag
        self.last_timestamp = -1

    def __call__(self):
        timestamp = int(time.time()*1000)
        if timestamp < self.last_timestamp:
            # clock backwards issue. 3bit for clock flag
            self.clock_flag = (self.clock_flag + 1) % 8
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) % 4096
            # if self.sequence == 0:
            #     timestamp = self.wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        # 3bit for clock flag, 7bit for machine id.
        return ((timestamp - 1288834974657) << 22) | (self.clock_flag << 19) | (self.machine_flag << 12) | self.sequence

    # def wait_next_millis(self, last_timestamp):
    #     timestamp = int(time.time()*1000)
    #     while timestamp <= last_timestamp:
    #         timestamp = int(time.time()*1000)
    #     return timestamp


# class UnixTimestampField(models.DateTimeField):
#     """UnixTimestampField: creates a DateTimeField that is represented on the
#     database as a TIMESTAMP field rather than the usual DATETIME field.
#     """
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)
#         self.null = True
#
#     def db_type(self, connection):
#         return "timestamp"
#
#     def to_python(self, value):
#         return datetime.date.fromtimestamp(value)
#
#     def get_db_prep_value(self, value):
#         if value == None:
#             return None
#         return datetime.date.strftime('%Y%m%d%H%M%S', value.timetuple())


class BaseModel(models.Model):
    """
    basic tenant' model
    """
    id = models.BigIntegerField(primary_key=True)
    label = models.CharField('label', max_length=5000, blank=True, default='')
    creator_id = models.BigIntegerField("creator's id", default=0)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)

    def save(self, *args, **kwargs):
        self.id = SnowflakeIDGenerator().__call__()
        super(BaseModel, self).save(*args, **kwargs)

    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if attr == "creator_id":
                from apps.account.models import User
                user_queryset = User.objects.filter(id=getattr(self, attr)).first()
                if user_queryset:
                    creator_info = dict(id=user_queryset.id, name=user_queryset.name, alias=user_queryset.alias)
                else:
                    creator_info = dict(id=getattr(self, attr), name="", alias="")
                dict_result["creator"] = creator_info
            elif attr == "tenant":
                pass
            elif attr == "password":
                pass

            elif isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S %z')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %z')
            else:
                dict_result[attr] = getattr(self, attr)
        return dict_result

    def get_raw_dict(self):
        """
        raw dict, do not convert ForeignKey and manytomanyfield
        :return:
        """
        pass

    # def get_dict(self):
    #     role_dict_info = super().get_dict()
    #     creator_obj = User.objects.filter(username=getattr(self, 'creator')).first()
    #     if creator_obj:
    #         role_dict_info['creator_info'] = dict(creator_id=creator_obj.id, creator_alias=creator_obj.alias,
    #                                               creator_username=creator_obj.username)
    #     else:
    #         role_dict_info['creator_info'] = dict(creator_id=0, creator_alias='', creator_username=getattr(self, 'creator'))
    #     return role_dict_info

    class Meta:
        abstract = True


class BaseCommonModel(BaseModel):
    """
    basic model
    """
    tenant_id = models.BigIntegerField("tenant_id", default=1)

    class Meta:
        abstract = True





# class DecimalSerializer(BaseSerializer):
#     def serialize(self):
#         return repr(self.value), {"from decimal import Decimal"}
#
#
# MigrationWriter.register_serializer(SnowflakeIDGenerator, DecimalSerializer)



