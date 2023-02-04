FROM centos:7
LABEL maintainer=blackholll@163.com
# 安装基础包
RUN yum install -y wget mysql-devel gcc gcc-devel python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git automake libtool make

RUN mkdir -p /var/log/loonflow

# 复制文件到镜像
COPY . /opt/loonflow/

# 安装python3.10
RUN wget https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tgz
RUN tar zxvf Python-3.10.9.tgz
RUN cd Python-3.10.9 && ./configure --enable-optimizations && make altinstall
RUN python3.10 -m venv /opt/venv/loonflow


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

WORKDIR /opt/loonflow