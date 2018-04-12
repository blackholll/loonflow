# loonflow
a workflow engine base django
基于django的工作流引擎系统,通过http接口调用。 可以作为企业内部统一的工作流引擎，提供诸如权限申请、资源申请、发布申请、请假、报销、it服务等所有工作流场景的服务。如果有一定的开发能力建议只使用后端引擎功能，前端根据场景定制开发可分散于各个内部后台管理系统(如人事、运维、监控、cmdb等等)。

欢迎访问我的博客了解我的设计思路 http://loonapp.com/blog/27/

非开源版本demo见: http://loonflow.loonapp.com/    账号密码: guest/loon1234

最新代码见develop分支，正式版本见tags中(如果已经有正式版本发布的话)

### 前言
本人2011年开始接触工作流，2013年开始开发工作流第一版本，至今经历了多个版本。目前着手开发一个开源版本，致力于提供企业统一工作流引擎方案

欢迎加入qq群一起交流工作流相关技术: 558788490


#loonflow 后端
### 运行开发环境
- 创建数据库: 根据backend/settings/dev.py中的配置创建数据库
- 创建python虚拟环境: python3.5
- 安装依赖包: pip install -r backend/requirements/dev.txt
- 初始化数据库: 

        python manage.py makemigrations
        python manage.py migrate
- 初始化数据: python manage.py loaddata notice_type.json
- 创建初始账户: python manage.py createsuperuser
