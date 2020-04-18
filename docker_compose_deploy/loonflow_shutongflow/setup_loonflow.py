# -*- coding: utf-8 -*-
"""
@author: children1987
"""

from utils import get_config_info, cmd, replace_in_file


def main():
    cmd('yum install -y mysql-devel gcc python3-devel')
    cmd('pip3 install -r requirements/dev.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com')
    cmd('cp settings/pro.py.simple settings/config.py')
    cfg_file = '/opt/loonflow/settings/config.py'

    replace_in_file(cfg_file, "'NAME': 'loonflownew'", "'NAME': 'loonflow'")
    replace_in_file(cfg_file, "'USER': 'loonflownew'", "'USER': 'root'")
    replace_in_file(cfg_file, "DEBUG = False", "DEBUG = True")
    config_info = get_config_info()
    password = config_info['mysql']['root_password']
    replace_in_file(
        cfg_file, "'PASSWORD': '123456'", "'PASSWORD': '{}'".format(password)
    )
    replace_in_file(
        '/opt/loonflow/settings/common.py',
        "HOMEPATH = os.environ['HOME']",
        "HOMEPATH = '/var/log/loonflow'"
    )
    cmd('python3 manage.py collectstatic --noinput')


if __name__ == '__main__':
    main()
