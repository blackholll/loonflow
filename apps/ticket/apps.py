from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TicketConfig(AppConfig):
    name = 'apps.ticket'
    verbose_name = _('ticket')
