from django.db import models
from apps.loon_base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField


class LoonArchived(BaseModel):
    """archived record"""
    table_name = models.CharField(_('table name'), max_length=100)
    data = JSONField(_('archived data'))

