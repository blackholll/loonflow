# -*- coding: utf-8 -*-
import os
import sys
import time

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


def sql_to_docker_mysql(root_pwd, db_name, sql_file):
    """
    把sql文件写入docker中的mysql
    root_pwd: the pwd of mysql root
    db_name: the name of database
    sql_file: the file full name of sql file.
    """
    print('创建 {} 数据库'.format(db_name))
    cmd("docker exec -itd mysql mysqladmin -uroot -p'{}' create {}".format(
        root_pwd, db_name))

    print('copy {} 文件进入容器'.format(sql_file))
    cmd('docker cp {} mysql:/{}.sql'.format(sql_file, db_name))

    print('创建 {}.sh'.format(db_name))
    cmd(
        '''echo "mysql -p'{0}' -uroot {1} < /{1}.sql" > ./{1}.sh'''.format(
            root_pwd, db_name
        )
    )
    print('copy {}.sh 文件进入容器'.format(db_name))
    cmd_str = 'docker cp ./{}.sh mysql:/'.format(db_name)
    cmd('echo "{}"'.format(cmd_str))
    cmd(cmd_str)

    print("导入 {}.sql".format(db_name))
    cmd_str = "docker exec -itd mysql /bin/bash /{}.sh".format(db_name)
    cmd('echo "{}"'.format(cmd_str))
    cmd(cmd_str)
    print("{} demo data write db ok".format(db_name))


def setup_mysql57():
    """
    在宿主机安装 mysql5.7

    为什么不以docker安装database？
    测试时发现了很多问题。最终放弃了以docker方式安装 mysql5.7
    """

    config_info = get_config_info()
    root_pwd = config_info['mysql']['root_password']

    print("docker安装 mysql5.7 开始")
    cmd(
        ("docker run --name mysql -d --net=host -e MYSQL_ROOT_PASSWORD={} "
         "-v /var/loonflow/db:/var/lib/mysql mysql:5.7.21").format(root_pwd)
    )
    print("docker安装 mysql5.7 完成")

    print("睡眠10秒，确保mysql启动完成")
    time.sleep(10)

    db_name = 'loonflow'
    sql_file = '/opt/loonflow/docker_compose_deploy/loonflow_shutongflow/loonflow-web/loonflow_demo_init.sql'
    sql_to_docker_mysql(root_pwd, db_name, sql_file)

    print("睡眠10秒，确保sql导入完成")
    time.sleep(10)

    db_name = 'shutongflow'
    sql_file = '/opt/loonflow/docker_compose_deploy/loonflow_shutongflow/shutongflow/shutongflow_demo_init.sql'
    sql_to_docker_mysql(root_pwd, db_name, sql_file)


def main():
    if os.geteuid() != 0:
        raise Exception("请以root权限运行")

    print('安装 docker')
    cmd_str = 'mkdir tmp_for_setup_docker && yum install -y git && git clone https://gitee.com/shihowcom/setup_docker.git tmp_for_setup_docker/setup_docker && python ./tmp_for_setup_docker/setup_docker/setup_docker.py'
    cmd(cmd_str)

    print('安装 docker版 mysql5.7')
    setup_mysql57()

    cmd("python docker_compose_deploy/loonflow_shutongflow/setup_compose.py")
    cmd("cd docker_compose_deploy/loonflow_shutongflow && docker-compose up")


if __name__ == '__main__':
    main()
