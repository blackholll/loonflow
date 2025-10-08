from django.db import models
from apps.loon_base_model import BaseCommonModel


class Notification(BaseCommonModel):
    """
    notice config, need encrypt
    """
    NOTICE_TYPE_CHOICE = [
        ("dingtalk", "dingtalk"),
        ("wecom", "wecom"),
        ("feishu", "feishu"),
        ("hook", "hook")
    ]
    name = models.CharField("name", max_length=50, null=False, default="")
    description = models.CharField("description", max_length=200, null=False, default="")
    type = models.CharField("type", max_length=50, null=False, default="")
    extra = models.JSONField("extra", max_length=1000, null=False)



