# 准备工作
- 准备一台linux系统(建议centos7)的服务器,建议4G以上内存
- 安装好python3(请自行百度或者google)
- 安装好docker-compose(请自行百度或者google)
- 配置容器镜像加速(请自行百度或者google)

# 部署及启动服务
## 使用容器mysql
```
# 启动服务
cd docker_compose_deploy
docker compose -f docker-compse.yml up -d

# 停止服务
docker compose -f docker-compse.yml stop
```

## 使用自己的mysql

```
# 进入mysql后创建数据库并授权
mysql> create database loonflow character set utf8mb4;  # 注意要使用utf8mb4字符集
mysql> grant all privileges on loonflow.* to loonflow@'%' identified by '123456';

# 移除及更新docker-compose.yml中mysql相关配置
移除loonflow-mysql服务
移除loonflow-task和loonflow-web服务中depends_on的oonflow-mysql
修改loonflow-task和loonflow-web服务中的mysql地址、用户、密码

# 启动服务
cd docker_compose_deploy
docker compose -f docker-compse.yml up -d

# 停止服务
docker compose -f docker-compse.yml stop
```

# 常见问题
- 如何修改mysql的密码

容器mysql服务的root密码:docker_compose_deploy/docker-compose.yml中MYSQL_ROOT_PASSWORD(需要第一次启动服务之前修改)

容器mysql服务loonflow的密码: docker_compose_deploy/loonflow-mysql/init/create_database.sql(需要第一次启动服务之前修改)

- 如何修改redis的密码

docker_compose_deploy/docker-compose.yml中loonflow-redis中requirepass及其他服务环境变量中的密码

- 支持ARM架构下docker方式启动么

开发环境直参考https://loonflow.readthedocs.io 直接启动. 生成环境别折腾了，找个linux服务器吧