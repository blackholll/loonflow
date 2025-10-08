from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Archived(BaseModel):
    """archived record"""
    model_name = models.CharField("model name", max_length=100)
    data = JSONField(_('archived data'))

    class Meta:
        app_label = 'archived'

