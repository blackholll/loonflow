import json
from django.db import models
from django.utils.translation import  ugettext_lazy as _


class BaseModel(models.Model):
    """
    basic model
    """
    creator = models.CharField(_('creator'), max_length=50)
    gmt_created = models.DateTimeField(_('gmt_created'), auto_now_add=True)
    gmt_modified = models.DateTimeField(_('gmt_modified'), auto_now=True)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)
    
    def get_dict(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        dict_result = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                dict_result[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                dict_result[attr] = getattr(self, attr)
        return dict_result

    class Meta:
        abstract = True



