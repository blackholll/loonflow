import os
import time
import datetime
import uuid


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter

base_dir = settings.BASE_DIR



class BaseModel(models.Model):
    """
    basic tenant' model
    """
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    label = models.JSONField('label', blank=True, default=dict)
    creator_id = models.UUIDField( 'creator_id', default=uuid.uuid4, editable=False, null=True)
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


    def get_raw_dict(self):
        """
        raw dict, do not convert ForeignKey and manytomanyfield
        :return:
        """
        pass

    class Meta:
        abstract = True


class BaseCommonModel(BaseModel):
    """
    basic model
    """
    tenant_id = models.UUIDField("tenant_id", default='00000000-0000-0000-0000-000000000001')

    class Meta:
        abstract = True

