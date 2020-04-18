# -*- coding: utf-8 -*-
"""
@author: children1987
"""

from utils import get_config_info, replace_in_file


def main():
    cfg_file = '/opt/shutongFlow/apps/apps/settings.py'
    # 修改数据库配置
    replace_in_file(cfg_file, "'USER': 'shutongflow'", "'USER': 'root'")
    config_info = get_config_info()
    password = config_info['mysql']['root_password']
    replace_in_file(
        cfg_file, "'PASSWORD': '123456'", "'PASSWORD': '{}'".format(password)
    )
    # 使前端项目在dev模式下可被外部访问
    f = '/opt/shutongFlow/fronted/config/index.js'
    replace_in_file(f, "host: 'localhost'", "host: '0.0.0.0'")

    f = '/opt/shutongFlow/fronted/src/main.js'
    ip = config_info['ip']
    replace_in_file(
        f,
        "axios.defaults.baseURL = 'http://127.0.0.1:6062/'",
        "axios.defaults.baseURL = 'http://{}:6062/'".format(ip)
    )

if __name__ == '__main__':
    main()
