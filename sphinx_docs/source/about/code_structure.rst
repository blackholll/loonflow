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
  ├── docs # 文档目录，后续会将文档全部迁移到wiki中
  │   ├── apis # 接口文档
  │   ├── images  # 相关图片
  │   └── specs  # 代码规范
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