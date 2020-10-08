FROM centos:7
LABEL maintainer children1987

RUN mkdir -p /var/log/loonflow & \
    yum install -y git python3

WORKDIR /opt
RUN git clone --branch r1.0.12 https://gitee.com/shihowcom/loonflow_ro loonflow
WORKDIR loonflow
RUN python3 /opt/loonflow/docker_compose_deploy/loonflow_shutongflow/setup_loonflow.py
