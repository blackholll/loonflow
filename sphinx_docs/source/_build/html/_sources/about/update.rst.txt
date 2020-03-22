========
版本升级
========

------------
r0.1.x-r.2.x
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
r0.2.x-r.3.x
------------
- 因为v0.3版本中username参数改成从header中获取，所以接口调用时需要将username通过header方式传递
- 为了脚本安全考虑,当状态的参与人类型为脚本时，参与人需要设置为脚本记录的id。 迁移时需要将这些状态的参与人从脚本名称改成脚本记录的id


--------------
r0.3.x-r1.0.x
--------------
待完善（r1.0.0正式版发布时会提供）
