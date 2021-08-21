==============
如何运行
==============

-------------
开发环境
-------------
- 将settings/dev.py.sample在settings目录下复制一份并重命名为config.py
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
- 启动开发环境: python manage.py runserver 6060
- 安装node v14
- 安装前端依赖
  进入到frontend目录下执行npm i
- 启动前端开发环境
  进入到frontend目录下执行npm run dev
- 启动celery任务: celery -A tasks worker -l info -Q loonflow (用于执行任务脚本、触发任务hook、通知hook。本地开发二次开发如果不需要这些功能时可以不启动)
- 访问http://127.0.0.1:8000即可


-------------
生产环境源码部署
-------------
- 生产环境建议使用nginx+uwsgi的方式部署
- 将settings/pro.py.sample在settings目录下复制一份并重命名为config.py
- 创建数据库并修改settings/pro.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 创建python虚拟环境: python3.6.x(python3.6最新稳定版)
- 安装依赖包: pip install -r requirements/pro.txt
- 编译前端
  
::

  进入frontend目录下，依次执行npm i 和npm run build （主要需要事先安装好node,建议安装node v14版本）  

- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、状态hook、通知hook]，centos7下redis service配置文件可参考https://github.com/blackholll/loonflow-helper/tree/master/deploy)
- 初始化数据库，导入初始化sql， 命令如下

::

  mysql -uroot -p  loonflow_2_0 < loonflow2.0.0.sql # 生产环境不建议使用migrate. 用户名及数据库需要根据你的实际情况也即config.py中的配置做相应修改

- 初始admin账号密码为admin/123456
- 启动celery任务: celery multi start -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid # -c参数为启动的celery进程数，注意logfile和pidfile前面是两个-， logfile为日志文件路径, pidfile为pid文件路径，可自行视情况调整
- 如需优雅停止celery服务: 

::

  celery multi stopwait -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid

- 如需优雅重启celery服务: 

::

  celery multi restart -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid

- 启动uwsgi
  uwsgi配置文件参考docker_compose_deploy/loonflow-web目录下uwsgi.ini
- 启动nginx
  nginx配置文件参考docker_compose_deploy/loonflow-web目录下nginx.conf


--------------------------------
生产环境docker compose方式部署
--------------------------------
为了方便的数据的持久化以及升级操作,此方式不会启动数据库,请事先准备好数据库。(注意创建库的使用使用utf-8字符集)。只部署loonflow
(包括nginx、redis),启动时将连接到你提供的数据库(保证持久化数据)。
成功启动后，可使用 http://{host} 访问， {host}为你的linux服务器的ip地址，admin账号密码为123456

- 准备工作:

::

  准备一台linux服务器
  安装好python3(请自行百度或者google)
  安装好docker-compose(请自行百度或者google)
  配置容器镜像加速(请自行百度或者google)

- 准备好数据库，授予权限

::

  # 进入mysql后创建数据库并授权
  mysql> create database loonflow character set utf8;  # 注意要使用utf8字符集
  mysql> grant all privileges on loonflow.* to loonflow@'%' identified by '123456';


- 修改相关配置

修改docker_compose_deploy/run.py中的相关配置

::

  # 修改run.py中数据库相关配置为你准备好的数据库信息
  db_host = ''  # loonflow使用的数据库的ip
  db_port = ''  # loonflow使用的数据库的端口
  db_name = ''  # loonflow使用的数据库的名称
  db_user = ''  # loonflow使用的数据库的用户
  db_password = ''  # loonflow使用的数据库的用户密码
  
  ddl_db_user = ''  # 可以执行ddl(拥有修改表结构权限)的用户
  ddl_db_password = ''  # 可以执行ddl(拥有修改表结构权限)的用户的密码

- 安装并启动服务

::

  python3 run.py install # 执行此命令后将修改dockerfile中的数据库配置，构建镜像，然后启动服务

- 启动服务

::

  python3 run.py start  # 此命令直接启动服务，请保证之前install过（也就是dockerfile中数据库配置已被修改）

- 停止服务

::

  python3 run.py stop # 停止服务， 这种方式对于celery task任务非优雅停止，可以使用flower(celery的监控系统)，将任务消费停止，并且等待所有认为都结束后再执行

- 升级并重启服务

::

  python3 run.py update # 仅用于小版本升级如a.b.c-->a.b.d,不涉及数据库表结构变更的升级，执行此命令后将修改数据配置, 然后重新构建镜像并启动, 注意先修改run.py中数据库相关配置
