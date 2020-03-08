==============
如何运行
==============

-------------
开发环境
-------------

- 创建数据库并修改settings/dev.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 修改tasks.py中DJANGO_SETTINGS_MODULE对应的配置文件为实际使用的配置文件
- 创建python虚拟环境: python3.5
- 安装依赖包: pip install -r requirements/dev.txt
- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、通知脚本])
- 初始化数据库
::

  python manage.py makemigrations
  python manage.py migrate

- 创建初始账户: python manage.py createsuperuser
- 启动开发环境: python manage.py runserver 如果需要启动在其他端口:python manage.py runserver 8888
- 启动celery任务: celery -A tasks worker -l info -Q loonflow

-------------
生产环境
-------------
- 生产环境建议使用nginx+uwsgi的方式部署
- 创建数据库并修改settings/pro.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 修改tasks.py中DJANGO_SETTINGS_MODULE对应的配置文件为实际使用的配置文件
- 创建python虚拟环境:python3.5
- 安装依赖包: pip install -r requirements/pro.txt
- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、通知脚本])
- 初始化数据库:
::

  python manage.py makemigrations
  python manage.py migrate

- 创建初始账户: python manage.py createsuperuser
- 启动celery任务: celery multi start -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid # -c参数为启动的celery进程数， logfile为日志文件路径, pidfile为pid文件路径，可自行视情况调整