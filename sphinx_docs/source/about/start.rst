==============
如何运行
==============

-------------
开发环境
-------------
- 将settings/dev.py.simple在settings目录下复制一份并重命名为config.py
- 创建数据库并修改settings/config.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 创建python虚拟环境: python3.6.x(python3.6最新稳定版)
- 安装依赖包: pip install -r requirements/dev.txt
- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、状态hook、通知hook])
- 初始化数据库

::

  python manage.py makemigrations
  python manage.py migrate
  # 如果只是本地测试，无需二次开发，也可以直接参考生产环境部署中直接导入初始sql(初始sql中包含admin用户)

- 创建初始账户: python manage.py createsuperuser
- 启动开发环境: python manage.py runserver 如果需要启动在其他端口:python manage.py runserver 8888
- 启动celery任务: celery -A tasks worker -l info -Q loonflow (用于执行任务脚本、触发任务hook、通知hook。本地开发二次开发如果不需要这些功能时可以不启动)


-------------
生产环境
-------------
- 生产环境建议使用nginx+uwsgi的方式部署(nginx及uwsgi配置文件可参考 https://github.com/blackholll/loonflow-helper/tree/master/deploy)
- 将settings/pro.py.simple在settings目录下复制一份并重命名为config.py
- 创建数据库并修改settings/pro.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 创建python虚拟环境: python3.6.x(python3.6最新稳定版)
- 安装依赖包: pip install -r requirements/pro.txt
- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、状态hook、通知hook]，centos7下redis service配置文件可参考https://github.com/blackholll/loonflow-helper/tree/master/deploy)
- 初始化数据库，导入初始化sql， 命令如下

::

  mysql -uroot -p  loonflow_1_0 < loonflow_init.sql # 生产环境不建议使用migrate. 用户名及数据库需要根据你的实际情况也即config.py中的配置做相应修改

- 初始admin账号密码为admin/loonflow123 (用于登录管理后台，管理用户及配置工作流等)
- 启动celery任务: celery multi start -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid # -c参数为启动的celery进程数， logfile为日志文件路径, pidfile为pid文件路径，可自行视情况调整
- 启动uwsgi
- 启动nginx


