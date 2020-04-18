# -*- coding: utf-8 -*-
import os
import subprocess


def cmd(cmd_str):
    if subprocess.call(cmd_str, shell=True):
        raise Exception("{} 执行失败".format(cmd_str))


def create_dir():
    if (not os.path.exists("/var/cmdb/db")):
        cmd("sudo mkdir -p /var/cmdb/db")


def main():
    if os.geteuid() != 0:
        raise Exception("请以root权限运行")

    print("安装 python3 开始")
    cmd("yum -y install python3")
    print("安装 python3 完成")


if __name__ == '__main__':
    main()
