==============
工作流相关接口
==============

--------------
获取工作流列表
--------------
- url

api/v1.0/workflows

- method

get

- 使用场景

获取到工作流列表后，用户选择对应的工作流来新建对应的工单。如果需要多级类型，可以在调用方系统保存对应关系。
如调用方的“权限申请-VPN权限申请“对应loonflow中id为1的workflow,调用方的“权限申请-服务器权限申请“对应loonflow中id为2的workflow

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - page
     - int
     - 否
     - 页码，默认1
   * - per_page
     - int
     - 否
     - 每页个数，默认10
   * - name
     - varchar
     - 否
     - 支持根据workflow name模糊查询

- 返回数据

::

  {
    "code": 0,
    "data": {
      "total": 2,
      "page": 1,
      "per_page": 10,
      "value": [{
        "name": "请假申请",
        "creator": "admin",
        "description": "请假申请",
        "gmt_created": "2018-04-23 20:49:32"
      }, {
        "name": "vpn申请",
        "creator": "admin",
        "description": "vpn权限申请",
        "gmt_created": "2018-05-06 12:32:36"
      }]
    },
    "msg": ""
  }

-----------------
获取工作流初始状态
-----------------

- url

api/v1.0/workflows/{workflow_id}/init_state

- method

get

- 请求参数

无

- 使用场景

用于获取创建工单时对应工作流的初始状态信息，返回内容包括创建工单时需要填写的表单内容，可以执行的提交操作

- 返回数据

::

  {
    "msg": "",
    "code": 0,
    "data": {
      "order_id": 0,
      "workflow_id": 1,
      "name": "新建中",
      "participant_type_id": 1,
      "distribute_type_id": 1,
      "participant": "wangfei",
      "is_hidden": false,
      "type_id": 1,
      "gmt_created": "2018-04-23 20:53:33",
      "id": 1,
      "transition": [{
        "transition_id": 1,
        "transition_name": "提交"
      }, {
        "transition_id": 2,
        "transition_name": "保存"
      }],
      "sub_workflow_id": 0,
      "creator": "admin",
      "label": {},
      "field_list": [{
        "order_id": 20,
        "field_key": "title",
        "field_attribute": 2,
        "value": null,
        "name": "标题",
        "field_type_id": 5
      }, {
        "order_id": 35,
        "field_key": "leave_proxy",
        "field_attribute": 2,
        "field_type_id": 60,
        "field_value": null,
        "field_name": "代理人",
        "field_choice": {}
      }, {
        "order_id": 25,
        "field_key": "leave_end",
        "field_attribute": 2,
        "field_type_id": 30,
        "field_value": null,
        "field_name": "结束时间",
        "field_choice": {}
      }, {
        "order_id": 20,
        "field_key": "leave_start",
        "field_attribute": 2,
        "field_type_id": 30,
        "field_value": null,
        "field_name": "开始时间",
        "field_choice": {}
      }, {
        "order_id": 40,
        "field_key": "leave_type",
        "field_attribute": 2,
        "field_type_id": 40,
        "field_value": null,
        "field_name": "请假类型",
        "field_choice": {
          "1": "年假",
          "2": "调休",
          "3": "病假",
          "4": "婚假"
        }
      }, {
        "order_id": 45,
        "field_key": "leave_reason",
        "field_attribute": 2,
        "field_type_id": 55,
        "field_value": null,
        "field_name": "请假原因及相关附件",
        "field_choice": {}
      }, {
        "order_id": 30,
        "field_key": "leave_days",
        "field_attribute": 2,
        "field_type_id": 5,
        "field_value": null,
        "field_name": "请假天数(0.5的倍数)",
        "field_choice": {}
      }]
    }
  }

----------------
获取工作流状态详情
----------------

- url

api/v1.0/workflows/states/{state_id}

- method

get

- 请求参数

无

- 使用场景

略

- 返回数据

::

  {
    "code": 0,
    "data": {
      "id": 1,
      "name": "\u65b0\u5efa\u4e2d",
      "workflow_id": 1,
      "sub_workflow_id": 0,
      "distribute_type_id": 1,
      "is_hidden": false,
      "order_id": 0,
      "type_id": 1,
      "participant_type_id": 1,
      "participant": "wangfei",
      "state_field": {
        "title": 2,
        "leave_start": 2,
        "leave_end": 2,
        "leave_days": 2,
        "leave_proxy": 2,
        "leave_type": 2,
        "leave_reason": 2
      },
      "label": {},
      "creator": "admin",
      "gmt_created": "2018-04-23 20:53:33"
    },
    "msg": ""
  }

---------------
获取工作流状态列表
---------------

- url

api/v1.0/workflows/{workflow_id}/states

- method

get

- 使用场景
可用于用户查询工单列表时选择工作流类型后，显示该工作流类型拥有的状态，然后可以再根据工单当前状态来查询。 另外可用于管理员干预工单强制修改状态时 允许选择的目标状态

- 返回数据

::

  {
    "code": 0,
    "data": {
      "value": [{
        "id": 1,
        "creator": "admin",
        "gmt_created": "2018-04-23 20:53:33",
        "gmt_modified": "2018-05-13 11:42:11",
        "is_deleted": false,
        "name": "\u65b0\u5efa\u4e2d",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "is_hidden": false,
        "order_id": 0,
        "type_id": 1,
        "remember_last_man_enable": false,
        "participant_type_id": 1,
        "participant": "wangfei",
        "distribute_type_id": 1,
        "state_field_str": {
          "title": 2,
          "leave_start": 2,
          "leave_end": 2,
          "leave_days": 2,
          "leave_proxy": 2,
          "leave_type": 2,
          "leave_reason": 2
        },
        "label": {},
        "participant_info": {
          "participant": "wangfei",
          "participant_name": "wangfei",
          "participant_type_id": 1,
          "participant_type_name": "\u4e2a\u4eba",
          "participant_alias": "wangfei"
        }
      }, {
        "id": 2,
        "creator": "admin",
        "gmt_created": "2018-04-30 15:45:48",
        "gmt_modified": "2018-05-14 06:44:10",
        "is_deleted": false,
        "name": "\u53d1\u8d77\u4eba-\u7f16\u8f91\u4e2d1",
        "workflow_id": 1,
        "sub_workflow_id": 2,
        "is_hidden": true,
        "order_id": 2,
        "type_id": 0,
        "remember_last_man_enable": false,
        "participant_type_id": 5,
        "participant": "creator",
        "distribute_type_id": 1,
        "state_field_str": {
          "leave_end": 3,
          "leave_days": 3,
          "sn": 1,
          "state.state_name": 1,
          "leave_proxy": 3,
          "title": 3,
          "gmt_created": 1,
          "creator": 1,
          "leave_start": 3,
          "leave_reason": 3,
          "leave_type": 3
        },
        "label": {},
        "participant_info": {
          "participant": "creator",
          "participant_name": "creator",
          "participant_type_id": 5,
          "participant_type_name": "\u53d8\u91cf",
          "participant_alias": "\u5de5\u5355\u521b\u5efa\u4eba"
        }
      }, {
        "id": 3,
        "creator": "admin",
        "gmt_created": "2018-04-30 15:46:42",
        "gmt_modified": "2018-11-27 07:20:33",
        "is_deleted": false,
        "name": "TL\u5ba1\u6279\u4e2d",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "is_hidden": false,
        "order_id": 3,
        "type_id": 0,
        "remember_last_man_enable": true,
        "participant_type_id": 5,
        "participant": "creator_tl",
        "distribute_type_id": 3,
        "state_field_str": {
          "leave_reason": 1,
          "leave_start": 1,
          "leave_type": 1,
          "creator": 1,
          "gmt_created": 1,
          "title": 1,
          "leave_proxy": 1,
          "sn": 1,
          "leave_end": 1,
          "leave_days": 1
        },
        "label": {
          "tech_er_in": "qa"
        },
        "participant_info": {
          "participant": "creator_tl",
          "participant_name": "creator_tl",
          "participant_type_id": 5,
          "participant_type_name": "\u53d8\u91cf",
          "participant_alias": "\u5de5\u5355\u521b\u5efa\u4eba\u7684tl"
        }
      }, {
        "id": 4,
        "creator": "admin",
        "gmt_created": "2018-04-30 15:47:58",
        "gmt_modified": "2018-05-13 11:42:59",
        "is_deleted": false,
        "name": "\u4eba\u4e8b\u90e8\u95e8-\u5904\u7406\u4e2d",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "is_hidden": false,
        "order_id": 4,
        "type_id": 0,
        "remember_last_man_enable": false,
        "participant_type_id": 1,
        "participant": "admin",
        "distribute_type_id": 1,
        "state_field_str": {
          "sn": 1,
          "title": 1,
          "leave_start": 1,
          "leave_end": 1,
          "leave_days": 1,
          "leave_proxy": 1,
          "leave_type": 1,
          "creator": 1,
          "gmt_created": 1,
          "leave_reason": 1
        },
        "label": {},
        "participant_info": {
          "participant": "admin",
          "participant_name": "admin",
          "participant_type_id": 1,
          "participant_type_name": "\u4e2a\u4eba",
          "participant_alias": "\u8d85\u7ea7\u7ba1\u7406\u5458"
        }
      }, {
        "id": 5,
        "creator": "admin",
        "gmt_created": "2018-04-30 15:51:41",
        "gmt_modified": "2018-05-11 06:52:39",
        "is_deleted": false,
        "name": "\u7ed3\u675f",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "is_hidden": false,
        "order_id": 6,
        "type_id": 2,
        "remember_last_man_enable": false,
        "participant_type_id": 0,
        "participant": "",
        "distribute_type_id": 1,
        "state_field_str": {},
        "label": {},
        "participant_info": {
          "participant": "",
          "participant_name": "",
          "participant_type_id": 0,
          "participant_type_name": "",
          "participant_alias": ""
        }
      }],
      "per_page": 10,
      "page": 1,
      "total": 5
    },
    "msg": ""
  }