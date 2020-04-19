# -*- coding: utf-8 -*-
import os

from utils import cmd, use_aliyun_yum


def main():
    if os.geteuid() != 0:
        raise Exception("请以root权限运行")

    # print("使用阿里云yum源 开始")
    # use_aliyun_yum()
    # print("使用阿里云yum源 完成")

    print("安装 python3 开始")
    cmd("yum -y install python3")
    print("安装 python3 完成")

    print("安装 docker-compose 开始")
    cmd("pip3 install docker-compose -i https://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com")
    print("安装 docker-compose 完成")


if __name__ == '__main__':
    main()
