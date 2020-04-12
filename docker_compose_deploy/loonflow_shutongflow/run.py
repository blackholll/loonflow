# -*- coding: utf-8 -*-
import os
import sys
import subprocess

if sys.version_info.major < 3:
    raise Exception('请使用python3版本运行本脚本')


def run_cmd(cmd):
    """
    执行命令
    :param cmd:
    :return:
    """
    try:
        if subprocess.call(cmd, shell=True):
            return False, "{} 执行失败".format(cmd)
        else:
            return True, ''
    except Exception as e:
        return False, e.__str__()


def stop_compose():
    """
    停止compose服务
    :return:
    """
    home_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/loonflow_shutongflow'
    cmd_str = 'cd {}&&docker-compose stop'.format(home_path)
    flag, result = run_cmd(cmd_str)
    if flag:
        print('-' * 30)
        print('停止服务成功')
    else:
        print('-' * 30)
        print('停止失败:{}'.format(result))


def init_db():
    """
    导入loonflow及shutongflow的初始数据库
    :return:
    """
    print('-'*30)
    print('开始导入初始化sql，需要下载镜像arey/mysql-client, 请耐心等候')
    init_loonflow_sql = os.path.abspath(os.path.join(os.getcwd(), "..")) + 'loonflow-web/loonflow_demo_init.sql'
    init_shutongflow_sql = os.path.abspath(os.path.join(os.getcwd(), "..")) + 'shutongflow/shutongflow_demo_init.sql'

    cmd_str = 'docker run -i arey/mysql-client -h{} -p{} -u{} {} < {}'.format(db_host, ddl_db_password, ddl_db_user,db_name, init_sql)
    print(cmd_str)
    run_cmd(cmd_str)
    print('-' * 30)
    print('完成初始化sql导入')


def install():
    # 启动容器后需要导入初始化数据
    home_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/loonflow_shutongflow'
    cmd_str = 'cd {}&&docker-compose up -d'.format(home_path)
    flag, result = run_cmd(cmd_str)
    if flag:
        init_db()
        print('-' * 30)
        print('启动成功，你可以直接通过http://hostip来访问loonflow的管理后台,其中hostip为你宿主机的ip')
    else:
        print('x' * 30)
        print('启动失败,请确认已经安装了docker compose后检查报错信息')


def start():
    """
    开始启动
    :return:
    """
    home_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/loonflow_shutongflow'
    cmd_str = 'cd {}&&docker-compose up -d'.format(home_path)
    flag, result = run_cmd(cmd_str)
    if flag:
        print('-' * 30)
        print('启动成功，你可以直接通过http://hostip来访问loonflow的管理后台,其中hostip为你宿主机的ip')
    else:
        print('x'*30)
        print('启动失败,请确认已经安装了docker compose后检查报错信息')


if __name__ == '__main__':

    params = sys.argv
    if len(params) != 2:
        raise Exception('usage: python3 run.py install/start/stop')
    if params[1] == 'install':
        install()
    elif params[1] == 'start':
        start()
    elif params[1] == 'stop':
        stop_compose()
    else:
        raise Exception('usage: python3 run.py install/start/stop')
