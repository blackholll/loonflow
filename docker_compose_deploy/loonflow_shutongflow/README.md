模块作者： 逆寒刀(children1987@qq.com)

## 0. 安装前必读
- 强烈建议基于一台新装的CentOS 7安装。因为其它场景可能会触发一些未被测到的问题。
- 这只是一个为了方便快速展示代码的demo，考虑到安全等因素，请勿直接用于生产。
- 至少需要2G内存，推荐4G

## 1.安装前准备

### 1.1 firewalld已关闭
```
systemctl stop firewalld.service
```
检查防火墙状态，确保其为dead状态
```
systemctl status firewalld
```
### 1.2 selinux已关闭
    - 建议永久关闭，而非临时关闭。
    - learn more: https://blog.csdn.net/zhoushengtao12/article/details/95346903
### 1.3. 如下端口未被占用
    - 3306 (mysql)
    - 6060 (loonflow)
    - 6061 (shutongFlow_frontend)
    - 6062 (shutongFlow_backend)
    - 6379 (redis)

## 2.开始安装
```
cd /opt && yum install -y git && git clone -b v1.0.5 https://gitee.com/shihowcom/loonflow_ro loonflow

# 在如下文件完成必要配置，重点是ip
vi loonflow/docker_compose_deploy/loonflow_shutongflow/config.json

cd loonflow && python ./docker_compose_deploy/loonflow_shutongflow/setup_all.py
```

## 3.安装完成后
看到docker容器们启动之后，就可以通过以下方式访问了：
### loonflow
- http://`ip`:6060/
- admin
- loonflow123

### shutongflow
- http://`ip`:6061/
- admin
- yxuqtr
