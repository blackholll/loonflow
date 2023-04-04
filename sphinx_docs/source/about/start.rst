==============
如何运行
==============

-------------
开发环境
-------------
- 将settings/dev.py.sample在settings目录下复制一份并重命名为config.py
- 创建数据库并修改settings/config.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 创建python虚拟环境: python3.10.x(python3.10最新稳定版)
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
- 创建python虚拟环境: python3.10.x(python3.10最新稳定版)
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

- 准备工作:

::

  准备一台linux服务器
  安装好python3(请自行百度或者google)
  安装好docker-compose(请自行百度或者google)
  配置容器镜像加速(请自行百度或者google)

- 启动/停止服务
::

  # 启动服务
  cd docker_compose_deploy
  docker compose -f docker-compose.yml up -d

  # 停止服务
  docker compose -f docker-compose.yml stop

- 启动/停止服务(使用已有mysql)
::

  # 进入mysql后创建数据库并授权
  mysql> create database loonflow character set utf8mb4;  # 注意要使用utf8mb4字符集
  mysql> grant all privileges on loonflow.* to loonflow@'%' identified by '123456';

  # 移除及更新docker-compose.yml中mysql相关配置
  移除loonflow-mysql服务
  移除loonflow-task和loonflow-web服务中depends_on的oonflow-mysql
  修改loonflow-task和loonflow-web服务中的mysql地址、用户、密码

  # 启动服务
  cd docker_compose_deploy
  docker compose -f docker-compose.yml up -d

  # 停止服务
  docker compose -f docker-compose.yml stop

- 访问服务

http://{service's ip}



-------------
常见问题
-------------
- 部署完后访问用户及密码是多少

docker compose方式会自动导入初始数据，用户及密码为admin/123456,其他已经用户的密码应该也是123456。

- docker-compose方式如何修改mysql的密码

容器mysql服务的root密码:docker_compose_deploy/docker-compose.yml中MYSQL_ROOT_PASSWORD(需要第一次启动服务之前修改)

容器mysql服务loonflow的密码: docker_compose_deploy/loonflow-mysql/init/create_database.sql(需要第一次启动服务之前修改)

- docker-compose方式如何修改redis的密码

docker_compose_deploy/docker-compose.yml中loonflow-redis中requirepass及其他服务环境变量中的密码

- docker-compose方式支持ARM架构下启动么

别折腾了，找个linux服务器吧， 我搞了一整天没成功build所有的arm image。