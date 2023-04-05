FROM blackholll/loonflow-base:latest
LABEL maintainer=blackholll@163.com


RUN python3.10 -m venv /opt/venv/loonflow


# 复制文件到镜像
COPY . /opt/loonflow/

WORKDIR /opt/loonflow/requirements
RUN /opt/venv/loonflow/bin/pip install -r pro.txt

WORKDIR /opt/loonflow/settings
RUN cp pro.py.sample config.py

RUN sed -i "/HOMEPATH = os.environ/c\    HOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py


## 编译前端
WORKDIR /opt/loonflow/frontend
RUN npm install --unsafe-perm
RUN npm run build


# uwsgi配置文件
ADD docker_compose_deploy/loonflow-web/uwsgi.ini /opt/loonflow/uwsgi.ini
# nginx配置文件
RUN mv /usr/local/nginx/conf/nginx.conf /usr/local/nginx/conf/nginx.confbak
ADD docker_compose_deploy/loonflow-web/nginx.conf /usr/local/nginx/conf/nginx.conf

RUN mkdir /var/log/nginx


