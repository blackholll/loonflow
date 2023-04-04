FROM blackholll/loonflow-base:latest
LABEL maintainer=blackholll@163.com


COPY . /opt/loonflow/
RUN python3.10 -m venv /opt/venv/loonflow

WORKDIR /opt/loonflow/requirements
RUN /opt/venv/loonflow/bin/pip install -r pro.txt

WORKDIR /opt/loonflow/settings
RUN cp pro.py.sample config.py


RUN sed -i "/HOMEPATH = os.environ/c\    HOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py

WORKDIR /opt/loonflow