# loonflow
a workflow engine base on django

English | [简体中文](./README.md)
Thanks for [Arefyekkalam](https://github.com/Arefyekkalam) 's translation

Django-based workflow engine system(Called through the http interface，Can be used as a unified workflow engine within the enterprise，provide permission applications such as、resource request、Post application、Ask for leave、to reimburse、Services for all workflow scenarios such as it service),If you have a certain development ability, it is recommended to only use the back-end engine function，The front end can be customized and developed according to the scene and can be dispersed in various internal background management systems(such as personnel、Operation and maintenance、monitor、cmdb and so on). Since version 1.1.x, loonflow comes with a front-end interface for creating and processing work orders, which can be used directly.

see official version[release](https://github.com/blackholll/loonflow/releases)middle,It is recommended to use the latest version In order to facilitate everyone to download, the compressed package will be uploaded to the qq group file after each release of a new version(QQ group:558788490), You can also use the git command to download the corresponding code directly

```
git clone git@github.com:blackholll/loonflow.git
git checkout rx.x.x  #(specific version number，such as r1.1.0）拉取代码

```


## foreword
I started working with workflow in 2011，In 2013 began to develop the first version of the workflow，There have been several versions so far.The current open source version is dedicated to providing a unified workflow engine solution for enterprises

Welcome to join the QQ group to exchange workflow related technologies: 558788490
The purpose of the QQ group:
- For everyone to communicate
- Some loonflow development dynamics and synchronization of development plans

Before use, please[Documentation](http://loonflow.readthedocs.io/)Read it twice.Problems encountered during use or any suggestions，Please check first[github issue](https://github.com/blackholll/loonflow/issues)See if there is an answer. If you can't find it, you can submit a new issue. You can also ask questions and communicate in the QQ group (there will be enthusiastic classmates in the group to answer, do not @group owner, the group owner generally only responds to issues due to energy)


A paid service has been launched, and if you donate over 300 yuan (see the Alipay payment code at the end of this document), you can enjoy the VIP service. The benefits include
- Add WeChat friends, if you have any questions, you can directly consult WeChat
- Support WeChat voice Q&A
- Reasonable and general new requirements put forward will be supported in the new version first.


## Basic Architecture
LOONFLOW divided into two parts:
- front-end interface(react + ant design pro): Including work order creation, processing, management, workflow management configuration, statistics, etc.
- Provide http api for back-end calls of various systems (if oa, cmdb, operation and maintenance system, customer service system) to complete the customized work order requirements of their respective systems

## Related items
In the period of loonflow 0.x.x and 1.0.x versions, the user-side interface for creating and processing work orders is not provided. Thanks to the providers of the following call-side demo projects. If you use vue or bootstrap to write your front-end to integrate various internal systems that need to use work orders, the following items are for reference
 
Technology Stack | Project Address | Author Contact | Description

---|---|---|---
vue.js + django | https://github.com/youshutong2080/shutongFlow | In the QQ group, QQ number: 343306138 | Supports the use in PC browsers, the function is relatively simple, the actual use needs to be modified according to your own needs, welcome to submit pr
bootstrap + django | https://github.com/jimmy201602/workflowdemo |In the QQ group, QQ number: 313484953|Supports the use in PC browsers, the function is relatively simple, the actual use needs to be modified according to your own needs, welcome to submit pr
vue.js + django |https://gitee.com/shihow/howflow-open | In the QQ group, QQ number: 39188043 | Support for use in DingTalk, during iteration, welcome to submit pr


## Renderings
Yes, you can no longer use workflowdemo, shutongflow and howflow-open. Of course, you can also refer to these three projects to write your own caller system

![user_manage](/static/images/2.0.x/login.png)
![user_manage](/static/images/2.0.x/workbench.png)
![user_manage](/static/images/2.0.x/new_ticket.png)
![user_manage](/static/images/2.0.x/handle_ticket.png)
![user_manage](/static/images/2.0.x/user.png)
![user_manage](/static/images/2.0.x/workflow_basic_conf.png)
![user_manage](/static/images/2.0.x/custom_field.png)
![user_manage](/static/images/2.0.x/status.png)
![user_manage](/static/images/2.0.x/transition.png)
![user_manage](/static/images/2.0.x/system_config.png)
![user_manage](/static/images/2.0.x/flow_chart.png)
![user_manage](/static/images/2.0.x/statistics.png)


## Working with documentation
[Working with documentation](https://loonflow.readthedocs.io)

## thanks

Special thanks to [JetBrains](https://www.jetbrains.com/?from=mirai) Free for this open source project [IntelliJ IDEA](https://www.jetbrains.com/idea/?from=loonflow)    Authorize

[<img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" width="200"/>](https://www.jetbrains.com/?from=loonflow)

# Donations welcome
Your support is my biggest motivation, welcome to donate by Alipay scan code

![donation_code](/static/images/donation_code.png)