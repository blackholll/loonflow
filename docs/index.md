# LOONFLOW V0.3 使用文档
a workflow engine base django
基于django的工作流引擎系统,通过http接口调用。 可以作为企业内部统一的工作流引擎，提供诸如权限申请、资源申请、发布申请、请假、报销、it服务等所有工作流场景的服务。如果有一定的开发能力建议只使用后端引擎功能，前端根据场景定制开发可分散于各个内部后台管理系统(如人事、运维、监控、cmdb等等)。

## 前言
本人2011年开始接触工作流，2013年开始开发工作流第一版本，至今经历了多个版本。目前着手开发一个开源版本，致力于提供企业统一工作流引擎方案

欢迎加入qq群一起交流工作流相关技术: 558788490

## 操作系统支持
- 建议使用Centos,Redhat,Ubuntu这类linux操作系统
- 因为celery4以后不支持windows,所以状态脚本和通知脚本执行会无法使用。 可以参考此文档兼容下:  [参考文档](https://blog.csdn.net/weixin_42833042/article/details/83655245)

## 运行开发环境
- 创建数据库并修改settings/dev.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 修改tasks.py中DJANGO_SETTINGS_MODULE对应的配置文件为实际使用的配置文件
- 创建python虚拟环境: python3.5
- 安装依赖包: pip install -r requirements/dev.txt
- 启动redis
- 初始化数据库: 
```
python manage.py makemigrations
python manage.py migrate
```
- 创建初始账户: python manage.py createsuperuser
- 启动开发环境: python manage.py runserver 如果需要启动在其他端口:python manage.py runserver 8888
- 启动celery任务: celery -A tasks worker -l info -Q loonflow

## 生产环境部署
- 创建数据库并修改settings/pro.py中相应配置(数据库配置、redis地址配置、日志路径配置等等)
- 修改tasks.py中DJANGO_SETTINGS_MODULE对应的配置文件为实际使用的配置文件
- 创建python虚拟环境:python3.5
- 按照依赖包: pip install -r requirements/pro.txt
- 启动redis
- 初始化数据库:
```
python manage.py makemigrations
python manage.py migrate
```
- 创建初始账户: python manage.py createsuperuser
- python manage.py collectstatic
- 建议使用nginx+uwsgi部署
- 启动celery任务: celery multi start -A tasks worker -l info -c 8 -Q loonflow --logfile=xxx.log --pidfile=xxx.pid   # -c参数为启动的celery进程数， logfile为日志文件路径, pidfile为pid文件路径，可自行视情况调整

## 版本升级
#### v0.1.x-v.2.x
从v0.1.x-v.2.x升级。需要一些DDL操作
- workflow.models.Transition新增字段timer,新增字段attribute_type_id,condition_expression
- ticket.modles.TicketRecord新增script_run_last_result字段,新增is_end字段,新增is_rejected字段,新增multi_all_person字段
- 删除ticket.modles.TicketStateLastMan
- workfow.models.State新增remember_last_man_enable字段
- account.models.AppToken新增字段workflow_ids字段,用于给每个app授权可以访问的工作流资源(对应工作及对应的工单，升级后需要修改此配置).新增ticket_sn_prefix字段，用于支持配置工单流水号前缀
- workflow.models.Workflow新增字段limit_expression，用于新建工单权限的限制
- workflow.models.workflow新增字段notices，用于关联通知方式
- workflow.models新增表CustomNotice 用于支持自定义通知方式
- workflow.models.CustomField新增label字段用于调用方自行扩展

#### v0.2.x-v.3.x
- 因为v0.3版本中username参数改成从header中获取，所以接口调用时需要将username通过header方式传递
- 为了脚本安全考虑,当状态的参与人类型为脚本时，参与人需要设置为脚本记录的id。 迁移时需要将这些状态的参与人从脚本名称改成脚本记录的id



## 术语定义 
工单：具体的待处理事项，用户新建的是工单，工单按照工作流的设计来实现不同状态不同处理人之间的流转

工作流：即工作流的设计，定义了工单的审批链、各状态的处理人、各状态可以执行的操作（提交、保存，处理完成，退回，关闭等等）、每个状态下显示哪些字段、哪些字段可以在哪些编辑

子工单:主要用于工单流转存在子集的情况，如在项目开发周期中存在项目周期和应用周期两个层级， 当项目处于开发中时，项目的多个涉及应用在项目开发中可能正处于不同的阶段(代码编写、静态扫描、单元测试、完成开发等状态)。当应用状态都完成开发时将触发项目的状态到提测中。在这个场景中应用的工单即为项目工单的子工单。 应用工单的父状态即为项目的“开发中”

子工作流:工作流的父子层级不体现在工作流记录中，而体现在状态记录中。在配置工作流时，可以给某个工作流的某个状态设置一个子工作流。可以在工作流的不同状态设置不同的子工作流。

流程图:为了方便用户了解工作流的流转规则，可以通过流程图的方式展示给用户，如下
![admin_homapage](/docs/images/workflow_chart.png)


转交:正常情况下工单的流转都是按照其对应工作流设定的规则来流转(状态、处理人类型、处理人等).在实际操作中，比如A提交了个工单，到达运维处理中状态，B接单处理，B在处理过程中发现自己其实处理不了，需要C才能处理。于是将工单转交给C。

加签:加签与转交不同。正常情况下工单的流转都是按照其对应工作流设定的规则来流转(状态、处理人类型、处理人等).在实际操作中,比如A提交了个工单，到达运维处理中状态，B接单处理，B在处理过程中发现需要C做些操作或者提供些信息，才能处理，于是将工单加签给C.C处理完成后工单处理人会回到B.于是B可以继续处理

工单自定义字段与工作流自定义字段的区别: workflow里面自定义字段规定工作流有哪些自定义的字段。比如配置一个请假的工作流。 需要有请假天数这个字段。工单里面的自定义字段 存的是自定义字段具体的值。 比如现在用于新建了一个请假工单，填写了请假天数。那么工单的自定义字段表中会保存这个值

工作流处理过程可以理解为工单状态的变化，如一个工作流处理过程中可以有：发起人新建中、发起人编辑中、部门经理审核中、技术人员处理中、发起人验证中、结束等状态，每个状态对应相应的处理人（如部门经理审核中这个状态下只有部门经理才可以处理该工单）。如用户在新建工单的时候处于“发起人新建中”，（用户）提交后工单处于“部门经理审核中”， 部门经理（即“部门经理审核中”状态的处理人）审批通过后，工单的状态变更为“技术人员处理中”。 注意："转交"和"加签"使用场景不同，使用时前端需要做必要的说明，避免用户使用错误

## 基本架构
LOONFLOW 分为两部分:
- 工作流配置的管理后台
- 提供http api供各个系统(如果oa、cmdb、运维系统、客服系统)调用以完成各自系统定制化的工单需求

## 工作流配置
1. 登录后台
- 使用部署过程中创建的(python manage.py creatsuperuser)用户名密码 登录http://host_ip:port 

2. 工作流配置
- 同步账户中用户、角色、用户角色(用户具有的角色)、部门信息

    请根据相关表结构自行编写定时任务脚来同步你所在企业的账户信息
- 上传必要的脚本(包括执行脚本和通知脚本.如自动赋权、自动开通账号等脚本，可用于实现工单审批通过后自动赋权、自动开通账号)
![run_script](/docs/images/run_script.png)
![notice_manage](/docs/images/notice_manage.png)
- 新建工作流
![new_workflow](/docs/images/new_workflow.png)

- 进入工作流的具体配置页面
![workflow_config_entry](/docs/images/workflow_config_entry.png)

- 新建工作流的自定义字段
![workflow_custom_field_config](/docs/images/workflow_custom_field_config.png)

- 设置工作流的状态
![workflow_state_config](/docs/images/workflow_state_config.png)

- 设置工作流流转: 工作流流转控制工单状态的变化，流转的名称即工单处理中的按钮的名称，用户点击工单后，系统通过此表中的配置获取到下个状态信息，以更新工单的状态以及做相应的其他操作(执行脚本、通知相关人员等等)
![workflow_transiton_config](/docs/images/workflow_transiton_config.png)

- 校验配置是否正确
![flow_chart_entry1](/docs/images/flow_chart_entry1.png)
![flow_chart_entry2](/docs/images/flow_chart_entry2.png)
![flow_chart](/docs/images/flowchart.png)


#### 注意
- 当某个状态的参与人配置为脚本时，其直连下个状态只能有一个。因为脚本执行完成后会只获取一个下个状态来自动流转
- 当状态下配置了子工作流,其处理人类型需要为个人，处理人为'loonrobot',.且其直连下个状态只能一个，因为所有子工单都结束后会自动流转到下个状态(只取一个)
- 一些内置字段不得作为工作流自定义字段,在设置自定义字段时，字段名字尽量特殊点,如yw_username, oa_title等。这些字段包括但不限于以下:
```
title,workflow_id, sn, state_id, parent_ticket_id, parent_ticket_state_id, participant_type_id, participant, relation, in_add_node, add_node_man, transition_id, suggestion, usernane, creator, gmt_created, gmt_modified, is_deleted
```

- 设置为部门处理时， 该部门的下级部门的相关人员也会自动包含在内

## 常量定义

```
  状态类型
    1: 开始状态.工单的最初始状态，如发起人新建中
    2: 结束状态.工单的最终状态，如完成、结束、关闭等等
  分配方式
    1: 主动接单。工单到达时如果当前处理人是多人，需要用户先接单再处理(避免多人同时处理。场景: 开发人员提交了一个定制化的机器的申请， 在运维人员处理中这个状态，此状态下配置的处理人是整个运维部门,那么所有运维都会看到这个工单，其中一个运维人员点击接单后代表其将为其服务。这时候其他人将在工单详情中看到处理人已经是这运维人员)
    2: 直接处理。工单到达时如果当前处理人是多人，不需要先接单，谁都可以处理
    3: 随机分配。工单到达时候，如果处理人为多人，那么系统将随机分配给某个人。如上面这个例子，系统将直接给工单的当前处理人设置为随机的一名运维人员(v0.2版本支持)
    4: 全部处理。当设置成某个状态为全部处理时，工单在此状态下需要所有相关人员都处理完成后，才会进入到下个状态(v0.2版本支持)
  处理人类型
    1: 个人
    2: 多人
    3: 部门
    4: 角色
    5: 变量 如工单创建人、工单创建人leader
    6: 脚本/机器人  执行脚本的情况 
    7. 工单字段 工单的某个字段(需要是用户名或者是逗号隔开的用户名),如工单的某个自定义字段是测试人员'devs',工单流转过程中其中一个状态是测试人员测试中，那么那个状态的处理人类型可以为7, 处理人为'devs')
    8. 父工单字段 父工单的某个字段(需要是用户名或者是逗号隔开的用户名),如上述项目和应用周期的工单，应用工单在某个状态下需要项目的负责人'po'审批，那么该状态的处理人类型可以为8，处理人为'po'
  流转类型
    1: 常规流转
    2: 定时器流转(将在v0.2版本中支持)
  自定义字段类型
    5: 字符串
    10: 整形
    15: 浮点型
    20: 布尔类型
    25: 日期类型
    30: 日期时间类型
    35: 单选框radio
    40: 多选框checkbox
    45: 下拉列表
    50: 多选的下拉列表
    55: 文本域
    60: 用户名(需要调用方系统自行处理用户列表，loonflow只保存用户名)
    70: 多选用户名(需要调用方系统自行处理用户列表，loonflow只保存用户名，多人的情况使用逗号隔开)
    80: 附件，多个附件使用逗号隔开。调用方自己实现上传功能，loonflow只保存文件路径
  字段属性:
    1: 只读 调用新建或处理工单的接口时如果传了设置为只读的字段的值，loonflow将忽略，不会更新工单此字段的值
    2: 必填 调用新建或处理工单的接口时必须传递此字段的值，如果未提供则新建或处理工单接口将调用失败
    3: 可选 调用新建或处理工单的接口时可传可不传此字段的值，如果传了此类型的字段，则loonflow将更新工单此字段的值
  工单权限类别:
    1: 用户当前拥有此工单的处理权限(因为随着工单的状态变化，权限也会相应变化)
    2: 用户当前拥有此工单的查看权限(因为随着工单的状态变化，权限也会相应变化)
```

## API调用
[接口文档](./apis/index.md)


## Q&A
-  为什么没使用django rest framework

    因为不使用外键(为什么不使用？可以百度搜下)且使用框架不够用灵活

- 为什么使用http api方式提供服务

    loonflow的理念是:工单应该是嵌入到各个系统中(如oa,cmdb,运维平台、客服系统等等), 这些系统通过后端api调用loonflow。所以loonflow只有管理界面(v0.1版本直接使用django admin,后面会重写管理界面)。后续会提供几个调用方demo供大家参考。感谢@youshutong帮忙写的调用方demo(vue+django):
    https://github.com/youshutong2080/shutongFlow 另外帮忙jimmy201602写的demo(bootstrap+django): https://github.com/jimmy201602/workflowdemo

- 为何不建议调用方前端直接调用loonflow

    调用方和loonflow之前需要做权限验证，签名算法考虑到安全只能写在调用方后端;作为引擎,loonflow不提供用户登录验证功能,只校验调用方的合法性，所以登录验证需要做在调用方自己的后端;每个调用方除了纯粹的工单的功能，还会需要一些额外的功能，比如根据自定义字段筛选工单列表，loonflow提供了工单列表的接，但是因为loonflow的自定义字段是纵表形式存储的，无法提供根据这些字段来筛选工单列表。如果需要自定义字段的筛选，需要调用方自己保存一份工单数据，用于筛选;比如需要做一个项目全生命周期管理的系统，需要用到工作流。 但是还有比如发布,获取人员信息、和其他系统交互、日志查看、项目数据统计等等功能。这些需要做在自己的后端

- 调用方是否需要保存工单的基础数据

    根据情况而定，如果调用方在显示工单数据的时候需要显示更多相关信息，可以本地保存一份附属信息与loonflow中对应关系。针对本地保存的情况，如果涉及工单流转的字段(如参与人等)，在本地修改时需要同时调用loonflow修改loonflow中保存的字段的值(v0.2版本会提供修改工单字段值的接口)

- 如何限制用户查看工单权限
  
    默认会限制工单的查看权限(通过api获取工单详情时,只有username参数是工单相关人员时才能获取到数据)。如果需要放开限制，可以修改工作流配置中的“查看权限校验”为否。权限配置只针对工作流的，多个类型的工作流需要单独配置

- 为何需要同步用户及部门信息到loonflow

    因为工单流转涉及到较多的用户信息获取，所以需要将用户信息(包括部门)同步到loonflow的账户系统中。同步部门信息的时候，如果发现部门被删除，建议修改部门名字，如前面加个 “已废弃:”,否则如果该部门存在某个工单的当前处理人的时候会有问题。用户离职的情况设置is_active=0.另外用户密码请随便填写(为了不允许普通用户登录)。管理员账户请通过python manage.py creatsuperuser来创建。只需要管理员实现一个同步脚本定时执行即可,其他调用方不用考虑此问题

- 如何支持根据工单的自定义字段查询

    loonflow只提供工单基础字段的查询，如果需要针对自定义字段的查询，请在自己系统中保存一份工单数据(注意工单处理过程中，如果有字段修改，也需要更新自己系统中的数据)
    
- 工单列表支持排序

    只支持根据创建时间排序。其他字段排序可以在调用方系统中保存一份数据来自己实现排序，然后只有在获取工单详情的时候调用loonflow接口

- 工单类型需要支持多级
    比如需要支持“运维-权限申请-vpn权限申请”。 因为loonflow的工作流只有一级，如果需要支持多级类型,需要在调用方保存一份工单类型与loonflow工作流关联的数据。表字段可以如下：type_id, type_name, up_type_id, loonflow_workflow_id
