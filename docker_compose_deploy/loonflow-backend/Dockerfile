FROM python:3.12-slim as builder
WORKDIR /app


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

