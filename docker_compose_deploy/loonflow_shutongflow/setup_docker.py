# -*- coding: utf-8 -*-
import os

from utils import cmd, use_aliyun_yum


def install_docker():
    cmd("sudo yum install -y yum-utils device-mapper-persistent-data lvm2")
    cmd("sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo")
    cmd("sudo yum makecache fast")
    cmd("sudo yum -y install docker-ce")
    if(not os.path.exists("/etc/docker")):
        cmd("mkdir -p /etc/docker")
    with open("/etc/docker/daemon.json", "w") as f:
        f.write('{\n    "registry-mirrors": ["http://hub-mirror.c.163.com"] \n}')
    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl start docker")


def main():
    if os.geteuid() != 0:
        raise Exception("请以root权限运行")

    # print("使用阿里云yum源 开始")
    # use_aliyun_yum()
    # print("使用阿里云yum源 完成")

    print("安装 docker 开始")
    install_docker()
    print("安装 docker 完成")


if __name__ == '__main__':
    main()
