from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WorkflowConfig(AppConfig):
    name = 'apps.workflow'
    verbose_name = _('workflow')
