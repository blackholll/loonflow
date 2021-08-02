"""定义learning_logs的URL模式"""

from django.conf.urls import url
from django.urls import path

from . import views  # 其中的句点让Python从当前的urls.py模块所在的文件夹中导入视图。

app_name = 'student'

urlpatterns = [
                  # 主页
                  url(r'^$', views.index, name='index'),
                  url(r'^new_ask/$', views.new_ask, name='new_ask'),
                  url(r'^lists/$', views.lists, name='lists'),
                  url(r'^postform/$', views.postform, name='postform'),
                  path('flowsteps/<path:id>/', views.flowsteps, name='flowsteps'),
                  path('info/<path:id>/', views.info, name='info'),
                  path('states/<path:id>/', views.states, name='states'),
                  path('setup/<path:id>/', views.setup, name='setup'),
                  path('accept_tickets_submit/<path:id>/', views.accept_tickets_submit, name='accept_tickets_submit'),
                  path('close_tickets/<path:id>/', views.close_tickets, name='close_tickets'),
                    path('ueditor_fileup', views.ueditor_uploadfile),
    path('ueditor_imgup', views.ueditor_uploadimage)

]
