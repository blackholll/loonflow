# -*- coding:utf-8 -*-
__author__ = 'wzz'
__date__ = '2018/3/8 8:24'
from django_filters import rest_framework as filters
from apps.account.models import LoonUser


class LoonUserFilter(filters.FilterSet):
    username = filters.CharFilter('username',lookup_expr='icontains')
    alias = filters.CharFilter('alias',lookup_expr='icontains')
    class Meta:
        model = LoonUser
        fields = ['username','alias']
