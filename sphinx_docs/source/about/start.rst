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
- 启动celery任务: celery multi start -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid # -c参数为启动的celery进程数，注意logfile和pidfile前面是两个-， logfile为日志文件路径, pidfile为pid文件路径，可自行视情况调整
- 如需优雅停止celery服务: 

::

  celery multi stopwait -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid

- 如需优雅重启celery服务: 

::

  celery multi restart -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid

- 启动uwsgi
- 启动nginx


--------------------------------
生产环境docker compose方式部署
--------------------------------
为了方便的数据的持久化以及升级操作,此方式不会启动数据库,请事先准备好数据库。(注意创建库的使用使用utf-8字符集)。只部署loonflow
(包括nginx、redis),启动时将连接到你提供的数据库(保证持久化数据)。

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


- 启动方式

确保已经安装了python3后。 cd 到 docker_compose_deploy/loonflow_only目录后,执行以下命令

::

  # 修改run.py中数据库相关配置为你准备好的数据库信息
  db_host = ''  # loonflow使用的数据库的ip
  db_port = ''  # loonflow使用的数据库的端口
  db_name = ''  # loonflow使用的数据库的名称
  db_user = ''  # loonflow使用的数据库的用户
  db_password = ''  # loonflow使用的数据库的用户密码
  
  ddl_db_user = ''  # 可以执行ddl(拥有修改表结构权限)的用户
  ddl_db_password = ''  # 可以执行ddl(拥有修改表结构权限)的用户的密码

  # 安装并启动服务
  python3 run.py install # 此命令后修改dockerfile中的数据库配置，然后启动

  # 启动服务
  python3 run.py start  # 此命令直接启动服务，请保证之前install过（也就是dockerfile中数据库配置已被修改）

  # 停止服务， 这种方式对于celery task任务非优雅停止，可以使用flower(celery的监控系统)，将任务消费停止，并且等待所有认为都结束后再执行
  python3 run.py stop


------------------------------
演示环境docker compose方式运行
------------------------------
提供者: 逆寒刀(children1987@qq.com)


安装前必读
>>>>>>>>>
- 本方式会同时安装loonflow及shutongflow(looflow的调用方demo, https://github.com/youshutong2080/shutongFlow), shutongflow功能不够完善，所以仅供大家开发调用方程序时参考
- 强烈建议基于一台新装的CentOS 7安装。因为其它场景可能会触发一些未被测到的问题
- 这只是一个为了方便快速展示代码的demo，考虑到安全、性能等因素，请勿直接用于生产
- 至少需要2G内存，推荐4G

安装前准备
>>>>>>>>>
- 关闭firewalld

::

  # 关闭防火墙
  systemctl stop firewalld.service
  # 检查防火墙状态
  systemctl status firewalld

- 关闭selinux

  建议永久关闭，而非临时关闭,详见  https://blog.csdn.net/zhoushengtao12/article/details/95346903
  
- 保证以下端口未被使用

  ::

    3306 (mysql)
    6060 (loonflow)
    6061 (shutongFlow_frontend)
    6062 (shutongFlow_backend)
    6379 (redis)


开始安装
>>>>>>>>>

::

  cd /opt && yum install -y git && git clone -b v1.0.3 https://gitee.com/shihowcom/loonflow_ro loonflow

  # 在如下文件完成必要配置，重点是ip
  vi loonflow/docker_compose_deploy/loonflow_shutongflow/config.json
  # 各参数含义如下
  {
    "ip": "117.33.233.74",  # 你的centos7服务器的地址
    "mysql": {
      "root_password": "mySql12#4,.De",  # mysql的root密码
    }
  }

  # 启动安装
  cd loonflow && python ./docker_compose_deploy/loonflow_shutongflow/setup_all.py


访问
>>>>>>
docker容器们启动成功后，就可以通过以下方式访问了：

- loonflow管理后台

::

  访问地址: http://ip:6060/   ip为你的centos7服务器的ip地址
  账号/密码: admin/loonflow123

- shutongflow

::

  访问地址: http://ip:6061/  ip为你的centos7服务器的ip地址
  账号/密码: admin/yxuqtr

