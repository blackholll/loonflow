FROM centos:7
LABEL maintainer blackholll@163.com

# 安装基础包
RUN mkdir -p /var/log/shutongflow & \
    rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm & \
    yum install -y wget mysql-devel gcc gcc-devel python3 python3-pip python3-dev python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git

WORKDIR /opt
# 安装npm
RUN wget -c https://mirror.tuna.tsinghua.edu.cn/nodejs-release/v8.9.1/node-v8.9.1-linux-x64.tar.xz
RUN tar -xvf node-v8.9.1-linux-x64.tar.xz
RUN mv node-v8.9.1-linux-x64 nodejs
RUN ln -s /opt/nodejs/bin/node /usr/local/bin/node
RUN ln -s /opt/nodejs/bin/npm /usr/local/bin/npm

# 安装cnpm
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN ln -s /opt/nodejs/bin/cnpm /usr/local/bin/cnpm

RUN git clone -b v0.2.1 https://gitee.com/shihowcom/shutongFlow_ro.git shutongFlow
WORKDIR /opt/shutongFlow/apps

RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com

WORKDIR /opt/shutongFlow/fronted
RUN cnpm i
WORKDIR /opt
RUN git clone -b v1.0.2 https://gitee.com/shihowcom/loonflow_ro loonflow
RUN python3 /opt/loonflow/docker_compose_deploy/loonflow_shutongflow/setup_shutongflow.py
