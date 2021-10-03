========
代码结构
========

::

  .
  ├── apps
  │   ├── account # 用户应用
  │   ├── manage  # 管理后台应用
  │   ├── ticket  # 工单应用
  │   └── workflow # 工作流应用
  ├── docker_compose_deploy # docker compose方式部署相关文件
  │   ├── loonflow-task  # 异步任务服务相关配置，dcokerfile等
  │   ├── loonflow-web  # web服务，dcokerfile,nginx配置,uwsgi配置等
  │   ├── docker-compose.yaml  # docker compose配置
  │   ├── README.md  # 一些说明
  │   └── run.py  # docker compose方式部署主程序
  ├── frontend  # ant design实现的前端部分（包括管理后台及新建、处理工单等页面）
  │   ├── config # 前端相关配置
  │   │   ├── config.ts  # 前端路由菜单配置
  │   │   └── proxy.ts  # 代理配置，本地开发时，将后端请求代理到后端服务的地址
  │   ├── src  # 前端主要代码
  │   │   ├── pages # 相关前端页面
  │   │   └──  services # 服务层，请求后端的接口的逻辑
  ├── loonflow
  │   └── __init__.py
  |   └── url.py # url路由主入口
  |   └── wsgi.py  # wsgi配置
  ├── media # 静态文件目录
  │   ├── flowchart  # 工作流流程图，用户上次的流程图，后续将弃用
  │   ├── notice_script  # 通知脚本目录
  │   └── workflow_script  # 工作流执行脚本目录
  ├── requirements # 依赖文件目录
  │   ├── common.txt  # 通用依赖
  │   ├── dev.txt  # 开发环境依赖
  │   ├── pro.txt  # 生产环境依赖
  │   ├── test.txt  # 测试环境依赖
  ├── service # 服务层
  │   ├── account  # 用户相关服务
  │   ├── common  # 通用服务
  │   ├── manage  # 管理后台相关服务
  │   ├── permission   # 权限相关服务
  │   ├── ticket  # 工单相关服务
  │   └── workflow  # 工作流相关服务
  ├── settings # 配置文件目录
  │   └──  __init__.py
  │   └──  common.py  #通用配置
  │   └──  dev.py  # 开发环境配置
  │   └──  prod.py  # 生产环境配置
  │   └──  test.py  # 测试环境配置
  ├── static # 静态文件，管理后台页面使用
  │   ├── bower_components
  │   ├── dist
  │   └── plugins
  ├── templates  # 模板文件，管理后台页面使用，因为管理后台未前后端分离，所以有模板文件
  │   ├── admin
  │   ├── doc
  │   ├── user_and_permission
  │   └── workflow
  └── tests  # 单元测试目录
      ├── test_models # model层测试
      ├── test_services # service层测试
      └── test_views  # view层测试