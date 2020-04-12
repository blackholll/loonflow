FROM centos:7
LABEL maintainer blackholll@163.com

# 安装基础包
RUN mkdir -p /var/log/shutongflow & \
    rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm & \
    yum install -y wget mysql-devel gcc gcc-devel python3 python3-pip python3-dev python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git

WORKDIR /opt
# 安装npm
RUN wget -c https://nodejs.org/dist/v8.9.1/node-v8.9.1-linux-x64.tar.xz
RUN tar -xvf node-v8.9.1-linux-x64.tar.xz
RUN mv node-v8.9.1-linux-x64 nodejs
RUN ln -s /opt/nodejs/bin/node /usr/local/bin/node
RUN ln -s /opt/nodejs/bin/npm /usr/local/bin/npm


RUN git clone https://github.com/youshutong2080/shutongFlow.git
WORKDIR /opt/shutongFlow
RUN git checkout v0.2.0
WORKDIR /opt

WORKDIR /opt/shutongFlow/apps

RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com


# 修改数据库配置
RUN sed -i "s/'NAME': 'loonflownew'/'NAME': 'shutongflow'/g" /opt/shutongFlow/apps/apps/settings.py
RUN sed -i "s/'USER': 'loonflownew'/'USER': 'shutongflow'/g" /opt/shutongFlow/apps/apps/settings.py
RUN sed -i "s/'PASSWORD': '123456'/'PASSWORD': 'shutongflow123,.Ly'/g" /opt/shutongFlow/apps/apps/settings.py
RUN sed -i "s/'HOST': '127.0.0.1'/'HOST': 'shutongflow-db'/g" /opt/shutongFlow/apps/apps/settings.py


WORKDIR /opt/shutongFlow/fronted
RUN npm install .

WORKDIR /opt/shutongFlow/apps
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

