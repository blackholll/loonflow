# -*- coding: utf-8 -*-
import json
import subprocess


def replace_in_file(f, old_str, new_str):
    with open(f, 'r') as f_r:
        lines = f_r.readlines()
    with open(f, 'w+') as f_w:
        for each in lines:
            t = each.replace(old_str, new_str)
            f_w.write(t)


def get_config_info():
    cfg_f = '/opt/loonflow/docker_compose_deploy/loonflow_shutongflow/config.json'
    with open(cfg_f, 'r') as f:
        json_str = f.read()
        return json.loads(json_str)


def cmd(cmd_str):
    if subprocess.call(cmd_str, shell=True):
        raise Exception("{} 执行失败".format(cmd_str))


def use_aliyun_yum():
    """
    使用阿里云yum源
    """
    print('安装wget')
    cmd("yum install -y wget")

    print('备份/etc/yum.repos.d/CentOS-cmd.repo文件')
    cmd('mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.back')

    print('下载阿里云的Centos-6.repo文件')
    cmd('wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo')

    print('重新加载yum')
    cmd('yum clean all')
    cmd('yum makecache')

