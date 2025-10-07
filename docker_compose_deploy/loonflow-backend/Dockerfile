FROM python:3.12-slim as builder
WORKDIR /app

# todo: remove 设置阿里云镜像源
RUN sed -i 's|http://deb.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|http://security.debian.org|https://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources

# 设置Python环境
ENV PYTHONUNBUFFERED=1 \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com
# todo:

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements/common.txt .
COPY ./backend/requirements/pro.txt .

RUN pip install --user --no-warn-script-location -r pro.txt


FROM python:3.12-slim
LABEL maintainer=blackholll@163.com

WORKDIR /app/loonflow

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH


COPY --from=builder /root/.local /root/.local

COPY ./backend /app/loonflow

RUN cp settings/pro.py.sample settings/config.py && \
    sed -i "/HOMEPATH = os.environ/c\    HOMEPATH = '/var/log/loonflow'" /app/loonflow/settings/common.py

RUN mkdir -p /var/log/loonflow

# execution permisson
# RUN chmod +x /app/loonflow/manage.py

EXPOSE 8000

