from django.db import models
from apps.loon_base_model import BaseModel


# Create your models here.
class Archive(BaseModel):
    """archived record"""
    model_name = models.CharField("model name", max_length=100)
    data = models.JSONField("archived data")
