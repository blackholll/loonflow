from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def add_version(_input):
    """
    加上版本信息?v=xxx，主要是为了避免静态文件缓存
    :param _input:
    :return:
    """
    return '?v=%s' % settings.STATIC_FILES_VERSION
