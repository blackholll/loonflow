FROM centos:7
LABEL maintainer blackholll@163.com
# 安装基础包
RUN yum install -y mysql-devel gcc gcc-devel python3 python3-pip python3-dev python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git
RUN mkdir -p /var/log/loonflow
WORKDIR /opt
# RUN git clone https://github.com/blackholll/loonflow.git
RUN git clone https://gitee.com/shihowcom/loonflow_ro
WORKDIR /opt/loonflow_ro
RUN git checkout r1.0.12
WORKDIR /opt
RUN mv loonflow_ro loonflow
WORKDIR /opt/loonflow/requirements
RUN pip3 install -r pro.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com
# 复制config.py文件
WORKDIR /opt/loonflow/settings
RUN cp pro.py.simple config.py
# 修改redis配置
RUN sed -i "s/REDIS_HOST = '127.0.0.1'/REDIS_HOST = 'loonflow-redis'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/REDIS_PASSWORD = ''/REDIS_PASSWORD = 'loonflow123'/g" /opt/loonflow/settings/config.py

# 修改数据库配置
RUN sed -i "s/'NAME': 'loonflownew'/'NAME': 'loonflow'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'USER': 'loonflownew'/'USER': 'loonflow'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'PASSWORD': '123456'/'PASSWORD': 'loonflow123,.Ly'/g" /opt/loonflow/settings/config.py
RUN sed -i "s/'HOST': '127.0.0.1'/'HOST': 'loonflow-db'/g" /opt/loonflow/settings/config.py

# 修改日志路径
RUN sed -i "/HOMEPATH = os.environ/c\    HOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py

WORKDIR /opt/loonflow