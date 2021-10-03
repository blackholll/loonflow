========
版本升级
========

------------
r0.1.x-r0.2.x
------------
从r0.1.x-r.2.x升级。需要一些DDL操作

- workflow.models.Transition新增字段timer,新增字段attribute_type_id,condition_expression
- ticket.modles.TicketRecord新增script_run_last_result字段,新增is_end字段,新增is_rejected字段,新增multi_all_person字段
- 删除ticket.modles.TicketStateLastMan
- workfow.models.State新增remember_last_man_enable字段
- account.models.AppToken新增字段workflow_ids字段,用于给每个app授权可以访问的工作流资源(对应工作及对应的工单，升级后需要修改此配置).新增ticket_sn_prefix字段，用于支持配置工单流水号前缀
- workflow.models.Workflow新增字段limit_expression，用于新建工单权限的限制
- workflow.models.workflow新增字段notices，用于关联通知方式
- workflow.models新增表CustomNotice 用于支持自定义通知方式
- workflow.models.CustomField新增label字段用于调用方自行扩展

------------
r0.2.x-r0.3.x
------------
- 因为v0.3版本中username参数改成从header中获取，所以接口调用时需要将username通过header方式传递
- 为了脚本安全考虑,当状态的参与人类型为脚本时，参与人需要设置为脚本记录的id。 迁移时需要将这些状态的参与人从脚本名称改成脚本记录的id


--------------
r0.3.x-r1.0.x
--------------
0. 如果你对升级过程不熟悉，强烈建议你将生产环境数据(数据库)导入到测试环境，按照下面的操作演练过且没问题后再在生产环境操作

1. 准备好通知的hook服务端(如果你当前有用到通知脚本，你需要改成hook方式,如果没用到通知功能，可忽略此步)

准备好通知的hook的服务端(可以在服务端提供短信、钉钉、企业微信、邮件等通知服务)，服务端给loonflow分配一个token用于生签名，服务器端以此token使用相同的算法生成签名用于校验loonflow。校验通过后根据hook请求的数据来发送通知消息。

2. 下载loonflow v1.0.x版本到新的服务器或者新的目录
3. 将0.3.x版本的media目录下目录及文件全部复制到v1.0.x版本的media目录下

4. 创建新的python3.6虚拟环境，并安装好requirement/pro.txt中的依赖

5. 停止调用方服务
6. 停止loonflow 0.3版本服务(包括web服务及task任务，task任务可优雅停止，命令:xxxx)

::

  celery multi stopwait -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid

7. 备份好0.3.x版本数据库(为了在发现问题时快速回退)
8. 执行升级sql

::

  https://github.com/blackholll/loonflow-helper/tree/master/update/0.3.xto1.0.x/ddl.sql
  https://github.com/blackholll/loonflow-helper/tree/master/update/0.3.xto1.0.x/dml.py   ## 将文件中的数据库配置修改为你的0.3.x版本使用的数据库


9. 将代码中settings/pro.py中复制并重命名为settings/config.py,将config.py中数据库就redis配置修改为当前使用的地址，临时修改config.py中的DEBUG参数=True，进入新的虚拟环境尝试使用python manage.py runserver 0.0.0.0:9999 启动loonflow 1.0.x，观察是否有报错，排查错误

10. 访问http://$serverip:9999, 在“工作流管理”-“通知管理”中新增好需要用到的通知

11. 访问http://$serverip:9999，在“工作流管理”--“工作流配置”中逐个编辑需要发送通知的工作流，选择对应的通知，并设置标题模板和通知模板

12. 修改config.py中的DEBUG参数=False,使用uwsgi+nginx启动loonflow r1.0.x, 

13. 启动task服务

14. 启动调用方服务


--------------
r1.0.x-r2.0.x
--------------
待提供
