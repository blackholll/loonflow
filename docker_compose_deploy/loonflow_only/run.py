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
    home_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/loonflow_only'
    cmd_str = 'cd {}&&docker-compose stop'.format(home_path)
    flag, result = run_cmd(cmd_str)
    if flag:
        print('-' * 30)
        print('停止服务成功')
    else:
        print('-' * 30)
        print('停止失败:{}'.format(result))


def update_db_config(db_host, db_port, db_name, db_user, db_password):
    """
    更新数据库配置
    :return:
    """
    print('-' * 30)
    print('开始更新数据库配置')
    home_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

    for file_dir in ('loonflow-task', 'loonflow-web'):
        dockerfile_path = home_path + '/loonflow_only/{}/Dockerfile'.format(file_dir)
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(dockerfile_path, "w", encoding="utf-8") as f_w:
            for line in lines:
                if """RUN sed -i "s/'NAME': """ in line:
                    line = """RUN sed -i "s/'NAME': 'loonflownew'/'NAME': '{}'/g" /opt/loonflow/settings/config.py\n""".format(
                        db_name)
                if """RUN sed -i "s/'USER': """ in line:
                    line = """RUN sed -i "s/'USER': 'loonflownew'/'USER': '{}'/g" /opt/loonflow/settings/config.py\n""".format(
                        db_user)
                if """RUN sed -i "s/'PASSWORD': """ in line:
                    line = """RUN sed -i "s/'PASSWORD': '123456'/'PASSWORD': '{}'/g" /opt/loonflow/settings/config.py\n""".format(
                        db_password)
                if """RUN sed -i "s/'HOST': """ in line:
                    line = """RUN sed -i "s/'HOST': '127.0.0.1'/'HOST': '{}'/g" /opt/loonflow/settings/config.py\n""".format(
                        db_host)
                    line = line + """RUN sed -i "s/'PORT': '3306'/'PORT': '{}'/g" /opt/loonflow/settings/config.py\n""".format(
                        db_port)
                f_w.write(line)

    print('-' * 30)
    print('完成数据库配置')


def init_db(db_host, db_name, ddl_db_user, ddl_db_password):
    """
    初始数据库
    :param db_host:
    :param ddl_db_user:
    :param ddl_db_password:
    :return:
    """
    print('-'*30)
    print('开始导入初始化sql，需要下载镜像arey/mysql-client, 请耐心等候')
    init_sql = os.path.abspath(os.path.join(os.getcwd(), "../..")) + '/loonflow_init.sql'
    cmd_str = 'docker run -i arey/mysql-client -h{} -p{} -u{} {} < {}'.format(db_host, ddl_db_password, ddl_db_user,db_name, init_sql)
    print(cmd_str)
    run_cmd(cmd_str)
    print('-' * 30)
    print('完成初始化sql导入')


def start():
    """
    开始启动
    :return:
    """
    home_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/loonflow_only'
    cmd_str = 'cd {}&&docker-compose up -d'.format(home_path)
    flag, result = run_cmd(cmd_str)
    if flag:
        print('-' * 30)
        print('启动成功，你可以直接通过http://hostip来访问loonflow的管理后台,其中hostip为你宿主机的ip')
    else:
        print('x'*30)
        print('启动失败,请确认已经安装了docker compose后检查报错信息')


if __name__ == '__main__':
    db_host = ''  # loonflow使用的数据库的ip
    db_port = ''  # loonflow使用的数据库的端口
    db_name = ''  # loonflow使用的数据库的名称
    db_user = ''  # loonflow使用的数据库的用户
    db_password = ''  # loonflow使用的数据库的用户密码

    ddl_db_user = ''  # 可以执行ddl(拥有修改表结构权限)的用户
    ddl_db_password = ''  # 可以执行ddl(拥有修改表结构权限)的用户的密码

    if not (db_host and db_name and db_password and db_user):
        raise Exception('请配置的你的数据库地址、端口、数据库名称、用户、密码')

    params = sys.argv
    if len(params) != 2:
        raise Exception('usage: python3 run.py install/start/stop')

    if params[1] == 'install':
        if not (db_host and db_name and db_password and db_user):
            raise Exception('安装loonflow需要初始化你的数据库表结构及初始admin账号，请提供拥有ddl权限的数据库用户及密码')
        init_db(db_host, db_name, ddl_db_user, ddl_db_password)
        update_db_config(db_host, db_port, db_name, db_user, db_password)
        start()
    elif params[1] == 'start':
        update_db_config(db_host, db_port, db_name, db_user, db_password)
        start()
    elif params[1] == 'stop':
        stop_compose()
    else:
        raise Exception('usage: python3 run.py install/start/stop')
