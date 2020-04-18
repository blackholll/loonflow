# -*- coding: utf-8 -*-
import os
import sys

from utils import cmd, get_config_info


def change_mysql_psw(new_psw):
    """
    :param new_psw: 新密码
    """
    key_str = 'password is generated for root@localhost: '
    with open('/var/log/mysqld.log') as f:
        for each_line in f.readlines():
            if key_str in each_line:
                init_psw = each_line.split(key_str)[-1][:-1]
                cmd("mysqladmin -uroot -p'{}' password '{}'".format(init_psw, new_psw))
                print("修改 mysql5.7 root密码完成")
                return
    print("ERROR: 修改 mysql5.7 root密码失败！未找到初始密码。")


def setup_mysql57():
    """
    在宿主机安装 mysql5.7

    为什么不以docker安装database？
    测试时发现了很多问题。最终放弃了以docker方式安装 mysql5.7
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)

    print("在宿主机 mysql5.7 安装开始")
    cmd("yum install -y wget")
    cmd("wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm")
    cmd("yum -y install mysql57-community-release-el7-10.noarch.rpm")
    cmd("yum -y install mysql-community-server")
    print("在宿主机 mysql5.7 安装完成")

    cmd("systemctl start mysqld.service")
    config_info = get_config_info()
    root_password = config_info['mysql']['root_password']
    change_mysql_psw(root_password)
    print("在宿主机 mysql5.7 配置完成")

    cmd("mysqladmin -uroot -p'{}' create loonflow".format(root_password))
    init_sql = '/opt/loonflow/docker_compose_deploy/loonflow_shutongflow/loonflow-web/loonflow_demo_init.sql'
    cmd_str = "mysql -p'{}' -uroot loonflow < {}".format(
        root_password, init_sql)
    cmd(cmd_str)
    print("loonflow demo data write db ok")

    cmd("mysqladmin -uroot -p'{}' create shutongflow".format(root_password))
    init_sql = '/opt/loonflow/docker_compose_deploy/loonflow_shutongflow/shutongflow/shutongflow_demo_init.sql'
    cmd_str = "mysql -p'{}' -uroot shutongflow < {}".format(
        root_password, init_sql)
    cmd(cmd_str)
    print("shutongflow demo data write db ok")


def main():
    if os.geteuid() != 0:
        raise Exception("请以root权限运行")

    config_info = get_config_info()
    is_need_setup_mysql = config_info['is_need_setup_mysql']
    if is_need_setup_mysql:
        print('宿主机安装mysql5.7')
        print('这一步不是必须的，您也可使用自己已有的数据库')
        print('执行到这里说明您已将is_need_setup_mysql配置为true（默认值true）')
        try:
            setup_mysql57()
        except Exception:
            print("Warning: 在宿主机 mysql5.7 安装失败，但可能是因为你已经安装过了")

    cmd("python docker_compose_deploy/loonflow_shutongflow/setup_docker.py")
    cmd("service docker restart")
    cmd("python docker_compose_deploy/loonflow_shutongflow/setup_compose.py")
    cmd("cd docker_compose_deploy/loonflow_shutongflow && docker-compose up")


if __name__ == '__main__':
    main()
