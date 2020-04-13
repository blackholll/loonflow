本目录下提供多种docker compose方式部署方式

# 准备工作
- 准备一台linux服务器
- 安装好python3(请自行百度或者google)
- 安装好docker-compose(请自行百度或者google)
- 配置容器镜像加速(请自行百度或者google)

# loonflow_only
此启动方式将只会部署loonflow(包括nginx、redis)。为了方便的数据的持久化以及升级操作,请事先准备好数据库
(注意创建库的使用使用utf-8字符集)。只部署loonflow(包括nginx、redis),启动时将连接到你提供的数据库
(保证持久化数据),此方式可以直接用于生产环境

### 准备好数据库，授予权限
```
# 进入mysql后创建数据库并授权
mysql> create database loonflow character set utf8;  # 注意要使用utf8字符集
mysql> grant all privileges on loonflow.* to loonflow@'%' identified by '123456';

```

#### 启动方式
确保已经安装了python3后。 cd 到 docker_compose_deploy/loonflow_only目录后,执行以下命令

```
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
```

# loonflow_shutongflow

暂未支持

# loonflow_workflowdemo

暂未支持