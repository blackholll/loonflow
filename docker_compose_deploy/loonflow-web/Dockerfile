FROM centos:7
LABEL maintainer=blackholll@163.com

# 安装基础包
RUN mkdir -p /var/log/loonflow & \
    rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm & \
    yum install -y wget mysql-devel gcc gcc-devel python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git automake libtool make

# 安装python3.10
RUN wget https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tgz
RUN tar zxvf Python-3.10.9.tgz
RUN cd Python-3.10.9 && ./configure --enable-optimizations && make altinstall
RUN python3.10 -m venv /opt/venv/loonflow


# 复制文件到镜像
COPY . /opt/loonflow/

#WORKDIR /opt
#RUN mv loonflow_ro loonflow
WORKDIR /opt/loonflow/requirements
RUN /opt/venv/loonflow/bin/pip install -r pro.txt -i  http://pypi.douban.com/simple --trusted-host pypi.douban.com
# 复制config.py文件
WORKDIR /opt/loonflow/settings
RUN cp pro.py.sample config.py
# 修改redis配置
RUN sed -i "s/REDIS_HOST = '127.0.0.1'/REDIS_HOST = 'loonflow-redis'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/REDIS_PASSWORD = ''/REDIS_PASSWORD = 'loonflow123'/g" /opt/loonflow/settings/config.py

# 修改数据库配置
RUN sed -i "s/'NAME': 'loonflownew'/'NAME': 'loonflow_1_1test'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'USER': 'loonflownew'/'USER': 'loonflow_1_1test'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'PASSWORD': '123456'/'PASSWORD': '123456'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'HOST': '127.0.0.1'/'HOST': '192.168.50.136'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'PORT': '3306'/'PORT': '3306'/g" /opt/loonflow/settings/config.py

# 修改日志路径
RUN sed -i "/HOMEPATH = os.environ/c\    HOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py



# 前端
WORKDIR /opt
## 安装nodejs
RUN wget -c https://mirror.tuna.tsinghua.edu.cn/nodejs-release/v14.3.0/node-v14.3.0-linux-x64.tar.xz --no-check-certificate
RUN tar -xvf node-v14.3.0-linux-x64.tar.xz
RUN mv node-v14.3.0-linux-x64 nodejs
RUN ln -s /opt/nodejs/bin/node /usr/local/bin/node
RUN ln -s /opt/nodejs/bin/npm /usr/local/bin/npm
RUN npm config set registry https://registry.npm.taobao.org
## 编译前端
WORKDIR /opt/loonflow/frontend
RUN npm install --unsafe-perm
RUN npm run build


# 安装nginx
RUN yum install -y nginx
# uwsgi配置文件
ADD docker_compose_deploy/loonflow-web/uwsgi.ini /opt/loonflow/uwsgi.ini
# nginx配置文件
ADD docker_compose_deploy/loonflow-web/nginx.conf /etc/nginx/nginx.conf


