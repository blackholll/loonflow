# loonflow
a workflow engine base on django
基于django的工作流引擎系统,通过http接口调用。 可以作为企业内部统一的工作流引擎，提供诸如权限申请、资源申请、发布申请、请假、报销、it服务等所有工作流场景的服务。如果有一定的开发能力建议只使用后端引擎功能，前端根据场景定制开发可分散于各个内部后台管理系统(如人事、运维、监控、cmdb等等)。

欢迎访问我的博客了解我的设计思路 http://loonapp.com/blog/27/

最新代码见develop分支，正式版本见release中,推荐使用最新的版本.可以直接通过此链接下载[release版本](https://github.com/blackholll/loonflow/releases), 或者使用以下命令
```
git clone git@github.com:blackholll/loonflow.git
git checkout vx.x.x  #(具体的版本号，如v0.1.4）拉取代码
```


## 前言
本人2011年开始接触工作流，2013年开始开发工作流第一版本，至今经历了多个版本。目前着手开发一个开源版本，致力于提供企业统一工作流引擎方案

欢迎加入qq群一起交流工作流相关技术: 558788490

如发现有问题或建议，请通过issue方式提交，我会每天定时回答。你可以提交issue后将issue的链接发到群里,群里会有热性的朋友帮忙解答

## 基本架构
LOONFLOW 分为两部分:
- 管理后台(工作流的配置) 
- 提供http api供各个系统(如果oa、cmdb、运维系统、客服系统)的后端调用以完成各自系统定制化的工单需求

## 效果图/动画
loonflow只提供后端调用api和工作流的配置后台，感谢youshutong2080(使用vue.js)
[shutongFlow](https://github.com/youshutong2080/shutongFlow) 和jimmy201602(使用bootstrap,  [workflowdemo](https://github.com/jimmy201602/workflowdemo)
分别帮忙写的一个调用方demo,**==当前调用方demo功能还比较简单,仅供参考,不建议直接用于生产==** ,欢迎大家在使用过程中提pr优化demo的功能.下面是效果图和动画

#### vue版本demo
![create_ticket](/docs/images/create-ticket.png)
![todo_list](/docs/images/todo-list.png)
![detail_ticket](/docs/images/detail-ticket.png)

### bootstrap版本demo
![bootstrap_demo](/docs/images/jimmy201602_demo.gif)
另外boostrap版本还提供了docker镜像，供新人快速部署(仅供查看效果图，不要直接用与生产环境):https://hub.docker.com/r/webterminal/workflowdemo/

### 管理后台
![workflow_list](/docs/images/workflowlist.png)
![customfield](/docs/images/customfield.png)
![flowchart](/docs/images/flowchart.png)

## 使用文档
[使用文档](https://github.com/blackholll/loonflow/wiki)



## 主要功能
- 【API】新建工单
- 【API】获取工单列表:待办、关联、创建的工单
- 【API】获取工单详情(区分是否有处理权限，如果处理权限显示处理表单，有查看权限显示展现表单)
- 【API】用户对工单可以做的操作
- 【API】处理工单(提交、保存、同意、拒绝、完成等等配置的操作)
- 【API】获取工单流转记录(工单的历史操作记录)
- 【API】工单step(简化的处理记录顺序图)
- 【API】修改工单状态
- 【API】批量获取工单状态(逗号隔开，简单的状态信息:只包括状态id,状态名称)
- 【API】获取工单状态详情
- 【API】接单(当工单当前的处理人实际为多个人时，支持先接单，然后再处理)
- 【API】转交工单
- 【API】加签工单
- 【API】提供修改工单字段的值的api
- 【API】工单列表中接口中state对象增加label信息
- 【API】提供接口获取工作流拥有的状态(state)列表
- 【API】工单脚本允许重试执行(执行失败的情况),重试工单脚本的api
- 【API】工单列表接口支持根据state_ids，是否已经结束,工单ids来查询
- 【内部逻辑】支持在工单流转过程中自动化执行python脚本(可以通过写脚本实现各种定制化的操作)
- 【内部逻辑】必填字段的校验支持不同transiton区分配置是否开启
- 【内部逻辑】自定义字段新增标签字段,用于调用方自行处理逻辑
- 【内部逻辑】工单流水号前缀自定义
- 【内部逻辑】工单的分配支持随机处理、全部处理(工单状态的处理人为多人、部门、角色等实际对应为多个处理人时候,如果该状态设置的分配方式为随机处理，则将会工单处理人设置为其中的某一个人。 如果该状态设置的分配方式为全部处理，那么需要涉及的每个人都处理完才会进入到下一个状态)
- 【内部逻辑】支持条件流转(如请假申请工单，当请假天数>3需要总监审批，当请假天数>5需要CEO审批）
- 【内部逻辑】支持设置transion为同意、拒绝、还是其他属性，并更新工单状态
- 【内部逻辑】待办通知功能(通过自定义的发送消息脚本来发送， 支持通知内容模板自定义)
- 【内部逻辑】新建工单的权限支持(通过权限限制表达式来实现支持限制周期、限制人员、限制级别等等)
- 【内部逻辑】退回操作支持自定义是否退回到目标状态最后一个处理人(如权限申请类型的工单，其中有个状态是运维人员处理中，运维A接单处理完成后，达到申请人验证中，如果申请人发现验证不通过需要退回，可以定义退回到所有运维人员还是只退回到之前处理的运维A)
- 【内部逻辑】API调用授权范围管理:支持根据调用方确定列表范围(不同来源应用只允许查询该应用相关的数据:工单列表、工单详情、等等)
- 【内部逻辑】定时器流转(如果需要工单在某个工单状态下超过多长时间自动流转到下个状态，可以通过此来实现)--使用celery的countdown实现
- 【内部逻辑】工单历史记录中保存当前工单所有信息便于回查(工单每次操作 都会当前工单的所有字段的信息保存起来)
- 工作流配置管理后台

# 相关术语(如转交、接单、加签等等)
见[使用文档](https://github.com/blackholll/loonflow/wiki)

# 欢迎捐助
您的支持是我最大的动力,欢迎支付宝扫码捐助

![donation_code](/docs/images/donation_code.png)
