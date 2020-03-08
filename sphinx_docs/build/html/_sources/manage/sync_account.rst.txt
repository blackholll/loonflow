===========
同步用户信息
===========

同步账户中用户、角色、用户角色(用户具有的角色)、部门信息。 loonflow中工单的流转过程中需要根据用户的相关信息来确定新的处理人，
因为不同公司用户组织架构信息保存方式各不一样(如ldap、AD或者直接保存在企业微信、钉钉等等)，需要你自己编写用户组织信息的脚本，
定时将你司的最新用户组织信息同步到loonflow中。可参考从AD中同步。 非常欢迎大家将自己的脚本pr到https://github.com/blackholll/loonflow-helper。

注意:

- loonflow中的用户只是用于流转的时候确定新的处理人，无需要用户登录loonflow的管理后台，所以同步脚本中往loonflow插入用户记录时，密码随便插入。当然超级管理员除外(超级管理员可以通过python manage.py createsuperuser命令来创建)

- 用户表中 dept_id为loonflow的部门表中主键id， 非你司用户信息中的部门id。 同步部门时可以将你司部门id保存在loonflow部门表中的label字段中来关联.label字段建议使用字段的json格式，方便以后扩展。如{"source_dept_id":11}
