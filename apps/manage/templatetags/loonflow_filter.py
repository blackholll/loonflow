from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def add_version(_input):
    """
    Plus version information?v=xxx, mainly to avoid static file caching
    :param _input:
    :return:
    """
    return '?v=%s' % settings.STATIC_FILES_VERSION
