# -*- coding: utf-8 -*-
# 全局变量、常量
#
from django.conf import settings


def global_variables(request):
    return {'VERSION': settings.VERSION}
