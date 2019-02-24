from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    总览
    :param request:
    :return:
    """
    return render(request, 'overview.html', {'active_nav': 'overview'})


@login_required
def doc_view(request):
    """
    文档
    :param request:
    :return:
    """
    return render(request, 'doc/index.html', {'active_nav': 'doc'})


@login_required
def user_manage_view(request):
    """
    用户管理
    :param request:
    :return:
    """
    return render(request, 'user_and_permission/user_manage.html', {'active_nav': 'user_manage'})