# loonflow
a workflow engine base on django
基于django的工作流引擎系统,通过http接口调用。 可以作为企业内部统一的工作流引擎，提供诸如权限申请、资源申请、发布申请、请假、报销、it服务等所有工作流场景的服务。如果有一定的开发能力建议只使用后端引擎功能，前端根据场景定制开发可分散于各个内部后台管理系统(如人事、运维、监控、cmdb等等)。

欢迎访问我的博客了解我的设计思路 http://loonapp.com/blog/27/

最新代码见develop分支，正式版本见release中,推荐使用最新的版本.可以直接通过此链接下载[release版本](https://github.com/blackholll/loonflow/releases), qq群文件(每次发布后都会将压缩包上传到群文件，qq群:558788490),或者使用以下命令
```
git clone git@github.com:blackholll/loonflow.git
git checkout vx.x.x  #(具体的版本号，如v0.1.4）拉取代码
```


## 前言
本人2011年开始接触工作流，2013年开始开发工作流第一版本，至今经历了多个版本。当前开源版本致力于提供企业统一工作流引擎方案

欢迎加入qq群一起交流工作流相关技术: 558788490

如发现有问题或建议，请通过issue方式提交，我会每天定时回答。issue的动态也会通过qq机器人自动发送到群里,群里会有热心的朋友帮忙解答

## 基本架构
LOONFLOW 分为两部分:
- 管理后台(工作流的配置) 
- 提供http api供各个系统(如果oa、cmdb、运维系统、客服系统)的后端调用以完成各自系统定制化的工单需求

## 效果图/动画
loonflow只提供后端调用api和工作流的配置后台，感谢以下调用方demo项目:
技术栈 | 项目地址 | 作者联系方式 | 说明
---|---|---|---
vue.js + django | https://github.com/youshutong2080/shutongFlow | qq群中,qq号: 343306138 |支持PC端浏览器中使用, 功能比较简单,实际使用需要根据自己的需求做适当改造,欢迎提交pr
bootstrap + django | https://github.com/jimmy201602/workflowdemo | qq群中,qq号: 313484953|支持PC端浏览器中使用, 功能比较简单,实际使用需要根据自己的需求做适当改造,欢迎提交pr
vue.js + django |https://gitee.com/shihow/howflow-open | qq群中,qq号:39188043 | 支持在钉钉中使用，迭代中，欢迎提交pr


下面是一些效果图和动画

#### vue版本(shutongflow)demo
![create_ticket](/docs/images/create-ticket.png)
![todo_list](/docs/images/todo-list.png)
![detail_ticket](/docs/images/detail-ticket.png)

### bootstrap版本(workflowdemo)demo
![bootstrap_demo](/docs/images/jimmy201602_demo.gif)
另外boostrap版本还提供了docker镜像，供新人快速部署(仅供查看效果图，不要直接用于生产环境):https://hub.docker.com/r/webterminal/workflowdemo/

### 管理后台
![user_manage](/docs/images/user_manage.png)
![workflow_list](/docs/images/workflow_list.png)
![workflow_edit](/docs/images/workflow_edit.png)
![customfield](/docs/images/workflow_config_detail.png)
![flowchart](/docs/images/flowchart.png)

![ticket_manage](/docs/images/ticket_manage.png)
![ticket_manage](/docs/images/ticket_manage_detail.png)

## 使用文档
[使用文档](https://loonflow.readthedocs.io)

## 鸣谢

特别感谢 [JetBrains](https://www.jetbrains.com/?from=mirai) 为本开源项目提供免费的 [IntelliJ IDEA](https://www.jetbrains.com/idea/?from=loonflow)  授权  

[<img src="/docs/images/jetbrains-variant-3.png" width="200"/>](https://www.jetbrains.com/?from=loonflow)

# 欢迎捐助
您的支持是我最大的动力,欢迎支付宝扫码捐助

![donation_code](/docs/images/donation_code.png)
