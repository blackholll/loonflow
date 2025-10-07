FROM centos:7
LABEL maintainer=blackholll@163.com

RUN mkdir -p /var/log/loonflow & \
    yum install -y wget make mysql-devel gcc gcc-devel python3-devel mysql-devel zlib-devel openssl-devel git automake libtool libffi-devel

WORKDIR /tmp

RUN wget http://www.openssl.org/source/openssl-1.1.1q.tar.gz --no-check-certificate
RUN tar -zxvf openssl-1.1.1q.tar.gz
RUN cd openssl-1.1.1q && ./config shared --openssldir=/usr/local/openssl --prefix=/usr/local/openssl \
	&& make && make install \
	&& echo "/usr/local/lib64/" >> /etc/ld.so.conf \
	&& echo "/usr/local/openssl/lib" >> /etc/ld.so.conf \
	&& ldconfig \
	&& ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl \
	&& ln -s /usr/local/openssl/include/openssl /usr/include/openssl


RUN wget https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tgz
RUN tar zxvf Python-3.10.9.tgz
RUN cd Python-3.10.9 && ./configure --with-openssl=/usr/local/openssl --enable-optimizations && make altinstall


RUN wget http://nginx.org/download/nginx-1.22.1.tar.gz --no-check-certificate
RUN tar zxvf nginx-1.22.1.tar.gz
RUN sed -i "s/\/.openssl//g" /tmp/nginx-1.22.1/auto/lib/openssl/conf
RUN cd nginx-1.22.1 && ./configure --with-openssl=/usr/local/openssl --with-http_stub_status_module --with-http_ssl_module && make && make install

WORKDIR /opt
RUN wget -c https://nodejs.org/download/release/v14.3.0/node-v14.3.0-linux-x64.tar.xz --no-check-certificate
RUN tar -xvf node-v14.3.0-linux-x64.tar.xz
RUN mv node-v14.3.0-linux-x64 nodejs
RUN ln -s /opt/nodejs/bin/node /usr/local/bin/node
RUN ln -s /opt/nodejs/bin/npm /usr/local/bin/npm
