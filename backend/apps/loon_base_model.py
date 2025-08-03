import os
import time
import datetime
import uuid


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter

machine_id = settings.MACHINE_ID
base_dir = settings.BASE_DIR



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
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    label = models.JSONField('label', blank=True, default=dict)
    creator_id = models.UUIDField( 'creator_id', default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)

    def get_dict(self):
        dict_result = {}
        for field in self._meta.fields:
            if field.name == "creator_id":
                if getattr(self, "creator_id"):
                    from apps.account.models import User
                    user_queryset = User.objects.filter(id=getattr(self, "creator_id")).first()
                    if user_queryset:
                        creator_info = dict(id=str(user_queryset.id), name=user_queryset.name, alias=user_queryset.alias)
                    else:
                        creator_info = dict(id=str(getattr(self, "creator_id")), name="", alias="")
                    dict_result["creator_info"] = creator_info
                else:
                    dict_result["creator_info"] = {}
            elif field.is_relation:
                pass
            elif field.name == "password":
                pass
            elif isinstance(getattr(self, field.name), datetime.datetime):
                dict_result[field.name] = getattr(self, field.name).strftime('%Y-%m-%d %H:%M:%S %z')
            elif isinstance(getattr(self, field.name), datetime.date):
                dict_result[field.name] = getattr(self, field.name).strftime('%Y-%m-%d %z')
            else:
                if isinstance(getattr(self, field.name), uuid.UUID):
                    dict_result[field.name] = str(getattr(self, field.name))
                else:
                    dict_result[field.name] = getattr(self, field.name)

        return dict_result



        # fields = []
        # for field in self._meta.fields:
        #     fields.append(field.name)
        #
        # dict_result = {}
        # import datetime
        # for attr in fields:
        #     if attr == "creator_id":
        #         from apps.account.models import User
        #         user_queryset = User.objects.filter(id=getattr(self, attr)).first()
        #         if user_queryset:
        #             creator_info = dict(id=user_queryset.id, name=user_queryset.name, alias=user_queryset.alias)
        #         else:
        #             creator_info = dict(id=getattr(self, attr), name="", alias="")
        #         dict_result["creator"] = creator_info
        #     elif if field.is_relation
        #     elif attr == "tenant":
        #         pass
        #     elif attr == "password":
        #         pass
        #
        #     elif isinstance(getattr(self, attr), datetime.datetime):
        #         dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S %z')
        #     elif isinstance(getattr(self, attr), datetime.date):
        #         dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %z')
        #     else:
        #         dict_result[attr] = getattr(self, attr)
        # return dict_result

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
    tenant_id = models.UUIDField("tenant_id", default='00000000-0000-0000-0000-000000000001')

    class Meta:
        abstract = True





# class DecimalSerializer(BaseSerializer):
#     def serialize(self):
#         return repr(self.value), {"from decimal import Decimal"}
#
#
# MigrationWriter.register_serializer(SnowflakeIDGenerator, DecimalSerializer)



