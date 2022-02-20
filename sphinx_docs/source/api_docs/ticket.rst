============
工单相关接口
============

------------
获取工单列表
------------
- url

api/v1.0/tickets

- method

get

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - sn
     - varchar
     - 否
     - 流水号，支持根据sn的前几位模糊查询
   * - title
     - varchar
     - 否
     - 工单标题，模糊查询
   * - create_start
     - varchar
     - 否
     - 创建时间起,如果创建时间起 和创建时间止 都不提供，则只返回最近一年的数据
   * - create_end
     - varchar
     - 否
     - 创建时间止,如果创建时间起 和创建时间止 都不提供，则只返回最近一年的数据
   * - workflow_ids
     - varchar
     - 否
     - 工作流ids，逗号隔开多个工作流id, 如"1,2,3"
   * - state_ids
     - varchar
     - 否
     - 状态ids,逗号隔开多个状态id,如"1,2,3"
   * - ticket_ids
     - varchar
     - 否
     - 工单ids, 逗号隔开多个id，如"1,2,3"
   * - reverse
     - varchar
     - 否
     - 是否按照创建时间倒序，"0"或者"1"，默认倒序
   * - page
     - int
     - 否
     - 页码，默认1
   * - per_page
     - varchar
     - 否
     - 每页个数，默认10
   * - act_state_id
     - int
     - 否
     - 工单的进行状态, 0草稿中(也就是初始状态)、1进行中 2被退回 3被撤回 4已完成 5已关闭
   * - parent_ticket_id
     - int
     - 否
     - 父工单id
   * - parent_ticket_state_id
     - int
     - 否
     - 父工单状态id
   * - category
     - varchar
     - 是
     - 类型('all':所有工单, 'owner':我创建的工单, 'duty':我的待处理工单, 'relation':我的关联工单[包括我新建的、我处理过的、曾经需要我处理过的工单。注意这里只考虑历史状态，工单将来状态的处理人不考虑], 'worked':我处理过的工单)

- 返回数据

::

  {
    "msg": "",
    "code": 0,
    "data": {
      "value": [{
        "participant_info": {
          "participant_type_id": 1,
          "participant": "1",
          "participant_name": "zhangsan",
          "participant_type_name": "个人",
          "participant_alias": "张三"
        },
        "gmt_created": "2018-05-15 07:16:38",
        "parent_ticket_state_id": 0,
        "state": {
          "state_name": "发起人-确认中",
          "state_id": 10
        },
        "creator": "lilei",
        "parent_ticket_id": 0,
        "title": "vpn申请",
        "gmt_modified": "2018-05-22 07:26:54",
        "workflow": {
          "workflow_name": "vpn申请",
          "workflow_id": 2
        },
        "sn": "loonflow_201805150001",
        "id": 17
      }],
      "total": 1,
      "page": 1,
      "per_page": 10
    }
  }

--------
新建工单
--------

- url

api/v1.0/tickets

- method

post

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - workflow_id
     - int
     - 是
     - 工作流id(工单关联的工作流的id)
   * - transition_id
     - int
     - 是
     - 新建工单时候的流转id（通过workflows/{id}/init_state接口可以获取新建工单时允许的transition）
   * - parent_ticket_id
     - int
     - 否
     - 父工单的id(用于子工单的逻辑，如果新建的工单是某个工单的子工单需要填写父工单的id)
   * - parent_ticket_state_id
     - int
     - 否
     - 父工单的状态（子工单是和父工单的某个状态关联的），如果提供parent_ticket_id，则此参数也必须
   * - suggestion
     - varchar
     - 否
     - 处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）
   * - 其他必填字段
     - N/A
     - 否
     - 其他必填字段或可选字段（在配置工作流过程中,会配置工作流初始状态必填和可选的字段。在新建工单时候必须提供必填字段。如请假申请工单，配置了自定义字段请假天数days，工单初始状态也设置了days为必填，那么新建此类工单时候就必选提供days)

- 返回数据

::

  {
    "msg": "",
    "code": 0,
    "data": {
      "ticket_id": 1
    }
  }

------------
获取工单详情
------------

- url

api/v1.0/tickets/{ticket_id}

- method

get

- 请求参数

无

- 返回数据

::

  {
    "code": 0,
    "msg": "",
    "data": {
      "value": {
        "workflow_id": 2,
        "in_add_node": true,
        "gmt_created": "2018-05-15 07:16:38",
        "id": 17,
        "relation": "guiji,wangwu,lilei",
        "title": "vpn\u7533\u8bf72",
        "sn": "loonflow_201805150001",
        "parent_ticket_id": 0,
        "creator": "lilei",
        "script_run_last_result": true,
        "gmt_modified": "2018-05-22 07:26:54",
        "act_state_id": 1,
        "multi_all_person": "{}",
        "creator_info": {
          "email": "lilei@163.com",
          "alias": "\u674e\u78ca",
          "dept_info": {
            "creator_info": {
              "creator_id": 1,
              "creator_alias": "\u8d85\u7ea7\u7ba1\u7406\u5458"
            },
            "leader": "lilei",
            "parent_dept_info": {
              "parent_dept_name": "\u603b\u90e8",
              "parent_dept_id": 1
            },
            "approver_info": [],
            "parent_dept_id": 1,
            "name": "\u6280\u672f\u90e8",
            "is_deleted": false,
            "creator": "admin",
            "gmt_modified": "2018-05-09 06:45:27",
            "label": "",
            "id": 2,
            "approver": "",
            "gmt_created": "2018-04-14 23:37:06",
            "leader_info": {
              "leader_alias": "\u674e\u78ca",
              "leader_username": "lilei"
            }
          },
          "username": "lilei",
          "phone": "13888888888",
          "is_active": true
        },
        "participant_type_id": 3,
        "state_id": 10,
        "is_end": false,
        "is_deleted": false,
        "field_list": [{
          "field_value": "loonflow_201805150001",
          "label": {},
          "boolean_field_display": {},
          "field_type_id": 5,
          "field_template": "",
          "field_choice": {},
          "field_key": "sn",
          "field_attribute": 1,
          "description": "\u5de5\u5355\u7684\u6d41\u6c34\u53f7",
          "default_value": null,
          "order_id": 10,
          "field_name": "\u6d41\u6c34\u53f7"
        }, {
          "field_value": "\u53d1\u8d77\u4eba-\u786e\u8ba4\u4e2d",
          "label": {},
          "boolean_field_display": {},
          "field_type_id": 5,
          "field_template": "",
          "field_choice": {},
          "field_key": "state.state_name",
          "field_attribute": 1,
          "description": "\u5de5\u5355\u5f53\u524d\u72b6\u6001\u7684\u540d\u79f0",
          "default_value": null,
          "order_id": 41,
          "field_name": "\u72b6\u6001\u540d"
        }, {
          "field_value": "\u603b\u90e8",
          "label": {},
          "boolean_field_display": {},
          "field_type_id": 5,
          "field_template": "",
          "field_choice": {},
          "field_key": "participant_info.participant_name",
          "field_attribute": 1,
          "description": "\u5de5\u5355\u7684\u5f53\u524d\u5904\u7406\u4eba",
          "default_value": null,
          "order_id": 50,
          "field_name": "\u5f53\u524d\u5904\u7406\u4eba"
        }, {
          "field_value": "vpn\u7533\u8bf7",
          "label": {},
          "boolean_field_display": {},
          "field_type_id": 5,
          "field_template": "",
          "field_choice": {},
          "field_key": "workflow.workflow_name",
          "field_attribute": 1,
          "description": "\u5de5\u5355\u6240\u5c5e\u5de5\u4f5c\u6d41\u7684\u540d\u79f0",
          "default_value": null,
          "order_id": 60,
          "field_name": "\u5de5\u4f5c\u6d41\u540d\u79f0"
        }],
        "parent_ticket_state_id": 0,
        "add_node_man": "zhangsan",
        "participant": "1",
        "state_info": {
          "id": 10,
          "creator": "admin",
          "gmt_created": "2018-04-30 15:47:58",
          "gmt_modified": "2018-05-13 11:42:59",
          "is_deleted": false,
          "name": "\u4eba\u4e8b\u90e8\u95e8-\u5904\u7406\u4e2d",
          "workflow_id": 1,
          "is_hidden": false,
          "order_id": 4,
          "type_id": 0,
          "enable_retreat": false,
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
          "label": {}
        }
      }
    }
  }

--------------------
获取工单可以做的操作
--------------------

- url

api/v1.0/tickets/{ticket_id}/transitions

- method

get

- 请求参数

无

- 返回数据

::

  {
    "msg": "",
    "data": {
      "value": [
        {
          "transition_name": "提交",
          "field_require_check": true,  # 默认为ture,如果此为否时， 不校验表单必填内容
          "transition_id": 1,
          "is_accept": false, # 不是接单,
          "in_add_node": false, # 不处于加签状态下
          "enable_alert": false,  # 是否弹窗告警，可用于当用户点击此操作的时确定是否弹窗信息
          "alert_text": "" # 弹窗中的消息内容
        },
        {
          "transition_name": "保存",
          "field_require_check": true,  # 默认为ture,如果此为否时， 不校验表单必填内容
          "transition_id": 2,
          "is_accept": false, # 不是接单,
          "in_add_node": false, # 不处于加签状态下
          "enable_alert": false,  # 是否弹窗告警，可用于当用户点击此操作的时确定是否弹窗信息
          "alert_text": "" # 弹窗中的消息内容
        }
      ]
      },
    "code": 0
  }

如果当前处理人超过一个人(处理人类型为多人，部门、角色都有可能实际为多个人)，且当前状态的分配方式为主动接单，则会要求先接单,返回数据如下。
处理时需要处理人先接单(点击接单按钮时 调用接单接口).

::

  {
    "msg": "",
    "code": 0,
    "data": {
      "value": [
        {
          "transition_id": 0,
          "transition_name": "接单",
          "is_accept": true,  # 接单,
          "in_add_node": false,
          "field_require_check": false
        }
      ]
    }
  }

当工单当前处于加签状态下，返回格式如下。 则用户点击“完成”按钮时，需要调用完成加签操作接口

::

  {
    "msg": "",
    "code": 0,
    "data": {
      "value": [
        {
          "transition_id": 0,
          "transition_name": "完成",
          "is_accept": false,
          "in_add_node": true, # 处于加签状态
          "field_require_check": false
        }
      ]
    }
  }

--------
接单
--------

- url

api/v1.0/tickets/{ticket_id}/accept

- method

post

- 请求参数

无

- 使用场景

使用接口获取工单当前可以做的的操作后，如果data.value.is_accept==true,则需要用户先接单才能处理，即页面显示接单按钮，
用户点击后调用接单接口，将工单的当前处理人设置该用户

- 返回数据

::

  {
    "data": {},
    "code": 0,
    "msg": ""
  }


--------
转交
--------

- url

api/v1.0/tickets/{ticket_id}/deliver

- method

post

- 请求参数


.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - target_username
     - varchar
     - 是
     - 转交对象的用户名
   * - suggestion
     - varchar
     - 否
     - 转交意见
   * - from_admin
     - boolß
     - 否
     - 是否管理员强制转交，此参数用于对应工作流管理员或者超级管理员强制转交工单，传了from_admin,loonflow会校验用户是否是超级管理员或者该工作流的管理员


- 使用场景

在工单处理界面可以显示一个按钮“转交”，当用户认为当前工单自己处理不了时，可以将工单转交给合适的人处理。 另外作为管理员可以强制(即非工单当前处理人的情况下)将工单转交给别人ß

- 返回数据

::

  {
    "data": true,
    "code": 0,
    "msg": ""
  }


--------
加签
--------

- url

api/v1.0/tickets/{ticket_id}/add_node

- method

post

- 请求参数


.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - target_username
     - varchar
     - 是
     - 加签对象的用户名
   * - suggestion
     - varchar
     - 否
     - 加签意见

- 使用场景

当用户A提交了一个权限申请工单，达到运维人员处理人中状态，作为运维人员的B在处理过程中发现需要C先处理或者提供一些必要的信息，B才能处理。
那么B在处理工单界面可以点击”加签“按钮，弹窗中选择C。 系统调用loonflow的加签接口将工单加签给C。C处理完后点击”完成“按钮，
系统调用loonflow的加签完成接口， 工单处理人将回到B. 那么B就可以按照之前既定流程正常流转下去

- 返回数据

::

  {
    "data": {},
    "code": 0,
    "msg": ""
  }


-----------
加签处理完成
-----------

- url

api/v1.0/tickets/{ticket_id}/add_node_end

- method

post

- 请求参数


.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - suggestion
     - varchar
     - 否
     - 加签完成意见

- 使用场景

使用场景 当A将工单加签给B.B在处理工单时候，界面将只显示“完成“按钮，点击后后端调用此接口，将工单基础表中的is_add_node设置为false

- 返回数据

::

  {
    "data": {},
    "code": 0,
    "msg": ""
  }


-----------
处理工单
-----------

- url

api/v1.0/tickets/{ticket_id}

- method

patch

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - transition_id
     - int
     - 是
     - 流转id
   * - suggestion
     - varchar
     - 否
     - 处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）
   * - 其他必填字段
     - N/A
     - 否
     - 其他必填字段或可选字段（在配置工作流过程中,会配置工作流每个状态的必填和可选的字段。在处理工单时候必须提供必填字段。如请假申请工单，配置了自定义字段请假天数days，工单初始状态也设置了days为必填，那么处理此类工单时候就必选提供days)。工单详情接口中有当前处理是时必选的字段

- 返回数据

::

  {
    "msg": "",
    "data": {},
    "code": 0
  }

----------------
获取工单流转记录
----------------

- url

api/v1.0/tickets/{ticket_id}/flowlogs

- method

get

- 请求参数


.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - ticket_data
     - string
     - 否
     - 是否返回每个操作时工单的所有字段信息，取值"1"/"0"，默认"0"(否)
   * - desc
     - string
     - 否
     - 是否按照时间降序返回记录，取值"1"/"0"，默认"1"(是)

- 返回数据（ticket_data未传或ticket_data传0）

::

  {
    "msg": "",
    "data": {
      "total": 4,
      "value": [
        {
          "state": {
            "state_name": "发起人-确认中",
            "state_id": 5
          },
          "transition": {
            "transition_name": "确认完成",
            "transition_id": 5,
            "attribute_type_id": 3
          },
          "ticket_id": 1,
          "participant_info": {
            "participant_email": "lilei@163.com",
            "participant_alias": "李磊",
            "participant_phone": "13888888888",
            "participant": "lilei",
            "participant_type_id": 1
          },
          "gmt_modified": "2018-04-30 15:57:26",
          "gmt_created": "2018-04-30 15:56:02",
          "suggestion": "已经生效，感谢"
        },
        {
        "state": {
          "state_name": "技术人员-处理中",
          "state_id": 4
          },
        "transition": {
          "transition_name": "处理完成",
          "transition_id": 4
        },
        "ticket_id": 1,
        "participant_info": {
            "participant_email": "lilei@163.com",
            "participant_alias": "李磊",
            "participant_phone": "13888888888",
            "participant": "lilei",
            "participant_type_id": 1
          },
        "gmt_modified": "2018-04-30 15:57:14",
        "gmt_created": "2018-04-30 15:55:32",
        "suggestion": "处理完成"
        },
        {
        "state": {
          "state_name": "TL审批中",
          "state_id": 3
        },
        "transition": {
          "transition_name": "同意",
          "transition_id": 3
        },
        "ticket_id": 1,
        "participant_info": {
            "participant_email": "lilei@163.com",
            "participant_alias": "李磊",
            "participant_phone": "13888888888",
            "participant": "lilei",
            "participant_type_id": 1
          },
        "gmt_modified": "2018-04-30 15:57:00",
        "gmt_created": "2018-04-30 15:53:19",
        "suggestion": "同意处理"
        },
        {
        "state": {
          "state_name": "新建中",
          "state_id": 1
        },
        "transition": {
          "transition_name": "提交",
          "transition_id": 1
        },
        "ticket_id": 1,
        "gmt_modified": "2018-04-30 15:52:35",
        "gmt_created": "2018-04-10 17:39:33",
        "suggestion": "请尽快处理，谢谢"
        }],
      "page": 1,
      "per_page": 10
      },
    "code": 0
  }

- 返回数据（ticket_data传1）

::

  {
	"msg": "",
	"data": {
		"total": 4,
		"value": [{
				"state": {
					"state_name": "发起人-确认中",
					"state_id": 5
				},
				"transition": {
					"transition_name": "确认完成",
					"transition_id": 5,
					"attribute_type_id": 3
				},
				"ticket_id": 1,
				"participant_info": {
					"participant_email": "lilei@163.com",
					"participant_alias": "李磊",
					"participant_phone": "13888888888",
					"participant": "lilei",
					"participant_type_id": 1
				},
				"gmt_modified": "2018-04-30 15:57:26",
				"gmt_created": "2018-04-30 15:56:02",
				"suggestion": "已经生效，感谢",
				"ticket_data": {
					"title": "xxx",
					"sn": "xxxxx",
					"state_id": 1,
					"ticket_id": 1,
					"gmt_modified": "2018-04-30 15:57:26",
					"gmt_created": "2018-04-30 15:56:02",
					"xxxx": "....."
				}
			},
			{
				"state": {
					"state_name": "技术人员-处理中",
					"state_id": 4
				},
				"transition": {
					"transition_name": "处理完成",
					"transition_id": 4
				},
				"ticket_id": 1,
				"participant_info": {
					"participant_email": "lilei@163.com",
					"participant_alias": "李磊",
					"participant_phone": "13888888888",
					"participant": "lilei",
					"participant_type_id": 1
				},
				"gmt_modified": "2018-04-30 15:57:14",
				"gmt_created": "2018-04-30 15:55:32",
				"suggestion": "处理完成",
				"ticket_data": {
					"title": "xxx",
					"sn": "xxxxx",
					"state_id": 1,
					"ticket_id": 1,
					"gmt_modified": "2018-04-30 15:57:26",
					"gmt_created": "2018-04-30 15:56:02",
					"xxxx": "....."
				}
			},
			{
				"state": {
					"state_name": "TL审批中",
					"state_id": 3
				},
				"transition": {
					"transition_name": "同意",
					"transition_id": 3
				},
				"ticket_id": 1,
				"participant_info": {
					"participant_email": "lilei@163.com",
					"participant_alias": "李磊",
					"participant_phone": "13888888888",
					"participant": "lilei",
					"participant_type_id": 1
				},
				"gmt_modified": "2018-04-30 15:57:00",
				"gmt_created": "2018-04-30 15:53:19",
				"suggestion": "同意处理",
				"ticket_data": {
					"title": "xxx",
					"sn": "xxxxx",
					"state_id": 1,
					"ticket_id": 1,
					"gmt_modified": "2018-04-30 15:57:26",
					"gmt_created": "2018-04-30 15:56:02",
					"xxxx": "....."
				}
			},
			{
				"state": {
					"state_name": "新建中",
					"state_id": 1
				},
				"transition": {
					"transition_name": "提交",
					"transition_id": 1
				},
				"ticket_id": 1,
				"gmt_modified": "2018-04-30 15:52:35",
				"gmt_created": "2018-04-10 17:39:33",
				"suggestion": "请尽快处理，谢谢",
				"ticket_data": {
					"title": "xxx",
					"sn": "xxxxx",
					"state_id": 1,
					"ticket_id": 1,
					"gmt_modified": "2018-04-30 15:57:26",
					"gmt_created": "2018-04-30 15:56:02",
					"xxxx": "....."
				}
			}
		],
		"page": 1,
		"per_page": 10
	},
	"code": 0
}

----------------
工单处理步骤记录
----------------

- url

api/v1.0/tickets/{ticket_id}/flowsteps

- method

get

- 请求参数

无

- 返回数据

::

  {
    "data": {
      "current_state_id": 2  //工单当前状态id
      "value": [{
        "state_id": 17,
        "state_flow_log_list": [],
        "order_id": 0,
        "state_name": "test11111"
      }, {
        "state_id": 18,
        "state_flow_log_list": [],
        "order_id": 0,
        "state_name": "2233222"
      }, {
        "state_id": 6,
        "state_flow_log_list": [{
          "gmt_created": "2018-05-15 07:16:38",
          "participant_info": {
            "participant_alias": "李磊",
            "participant_type_id": 1,
            "participant": "lilei",
            "participant_phone": "13888888888",
            "participant_email": "lilei@163.com"
          },
          "suggestion": "",
          "participant": "lilei",
          "state_id": 6,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "提交",
            "transition_id": 7
          },
          "id": 32,
          "intervene_type_id": 0
        }],
        "order_id": 1,
        "state_name": "发起人-新建中"
      }, {
        "state_id": 7,
        "state_flow_log_list": [{
          "gmt_created": "2018-05-15 07:20:40",
          "participant_info": {
            "participant_alias": "李磊",
            "participant_type_id": 1,
            "participant": "lilei",
            "participant_phone": "13888888888",
            "participant_email": "lilei@163.com"
          },
          "suggestion": "同意申请",
          "participant": "lilei",
          "state_id": 7,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 8
          },
          "id": 33,
          "intervene_type_id": 0
        }],
        "order_id": 2,
        "state_name": "发起人tl-审批中"
      }, {
        "state_id": 8,
        "state_flow_log_list": [{
          "gmt_created": "2018-05-16 06:42:00",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "接单处理",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "未知操作",
            "transition_id": 0
          },
          "id": 36,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 06:49:55",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 37,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 06:57:31",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "接单处理",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "未知操作",
            "transition_id": 0
          },
          "id": 38,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 06:57:36",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 39,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 06:58:41",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 40,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:01:53",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 41,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:03:34",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 43,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:04:45",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 45,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:31:29",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 47,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:21:00",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 49,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:24:03",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 51,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:24:44",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 53,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:33:26",
          "participant_info": {
            "participant_alias": "轨迹",
            "participant_type_id": 1,
            "participant": "guiji",
            "participant_phone": "13888888888",
            "participant_email": "guiji@163.com"
          },
          "suggestion": "同意",
          "participant": "guiji",
          "state_id": 8,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "同意",
            "transition_id": 9
          },
          "id": 55,
          "intervene_type_id": 0
        }],
        "order_id": 3,
        "state_name": "运维人员-审批中"
      }, {
        "state_id": 9,
        "state_flow_log_list": [{
          "gmt_created": "2018-05-16 07:01:54",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "False\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 42,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:03:34",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "False\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 44,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:04:45",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "False\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 46,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 07:31:29",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "lilei\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 48,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:21:00",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "lilei\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 50,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:24:03",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "lilei\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 52,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:24:44",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "lilei\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 54,
          "intervene_type_id": 0
        }, {
          "gmt_created": "2018-05-16 23:33:26",
          "participant_info": {
            "participant_phone": "",
            "participant_alias": "demo_script.py",
            "participant_email": "",
            "participant_type_id": 6,
            "participant": "demo_script.py"
          },
          "suggestion": "lilei\n",
          "participant": "demo_script.py",
          "state_id": 9,
          "participant_type_id": 6,
          "transition": {
            "transition_name": "脚本执行完成",
            "transition_id": 10
          },
          "id": 56,
          "intervene_type_id": 0
        }],
        "order_id": 4,
        "state_name": "授权脚本-自动执行中"
      }, {
        "state_id": 10,
        "state_flow_log_list": [{
          "gmt_created": "2018-05-17 06:45:58",
          "participant_info": {
            "participant_alias": "李磊",
            "participant_type_id": 1,
            "participant": "lilei",
            "participant_phone": "13888888888",
            "participant_email": "lilei@163.com"
          },
          "suggestion": "请处理",
          "participant": "lilei",
          "state_id": 10,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "转交操作",
            "transition_id": 0
          },
          "id": 57,
          "intervene_type_id": 1
        }, {
          "gmt_created": "2018-05-17 06:47:46",
          "participant_info": {
            "participant_alias": "张三",
            "participant_type_id": 1,
            "participant": "zhangsan",
            "participant_phone": "13888888888",
            "participant_email": "zhangsan@163.com"
          },
          "suggestion": "请协助处理",
          "participant": "zhangsan",
          "state_id": 10,
          "participant_type_id": 1,
          "transition": {
            "transition_name": "加签操作",
            "transition_id": 0
          },
          "id": 58,
          "intervene_type_id": 2
        }],
        "order_id": 6,
        "state_name": "发起人-确认中"
      }, {
        "state_id": 11,
        "state_flow_log_list": [],
        "order_id": 7,
        "state_name": "结束"
      }]
    },
    "msg": "",
    "code": 0
  }

----------------
修改工单状态
----------------

- url

api/v1.0/tickets/{ticket_id}/state

- method

put

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - state_id
     - int
     - 是
     - 目标状态id
   * - suggestion
     - varchar
     - 否
     - 处理意见

- 使用场景

用于干预工单的当前状态,可以直接将工单状态修改为指定状态，系统会根据state_id获取对应的处理人信息

- 返回格式

::

  {
    "msg": "",
    "data": {},
    "code": 0
  }


----------------
批量获取工单状态
----------------

- url

api/v1.0/tickets/states

- method

get

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - ticket_ids
     - varchar
     - 是
     - 工单ids,逗号隔开的字符串
  
- 使用场景

调用方自己保存工单基础信息 并根据loonflow中工单id关联，在显示工单列表时直接从自己后端获取工单列表。 但是工单状态需要实时从loonflow中获取，那么可以
通过此接口获取一页工单列表每个工单的状态

- 返回数据

::

  {
    "code": 0,
    "data": {
      "1": {
          "state_id": 1,
          "state_name": "发起人-编辑中"
        },
      2: {
          "state_id": 2,
          "state_name": "新建中"
        }
    },
    "msg": ""
  }


----------------
修改工单字段的值
----------------

- url

api/v1.0/tickets/{ticket_id}/fields

- method

patch

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - 需要修改值的字段的key1
     - varchar
     - 是
     - 如需要修改标题，则就是title
   * - 需要修改值的字段的key2
     - varchar
     - 是
     - 如需要修改标题，则就是title
   * - 其他需要修改的字段的字段标识
     - varchar
     - 是
     - 如需要修改标题，则就是title

- 返回数据

::

  {
    "msg": "",
    "data": {},
    "code": 0
  }

--------------------
重试工单脚本/hook任务
--------------------

- url

api/v1.0/tickets/{ticket_id}/retry_script

- method

post

- 请求参数

无

- 使用场景

当工单的脚本(或者hook[v0.3.17版本支持])执行失败后，工单详情接口中获取的数据中script_run_last_result为false.
这时可以在工单详情界面 step图中此状态下显示有个”重试按钮“，用户点击此按钮后，可以调用此接口重新执行或重新触发hook

- 返回数据

::

  {
    "msg": "Ticket script or hook retry start successful",
    "data": {},
    "code": 0
  }

--------------------
新增工单评论/注释
--------------------

- url

api/v1.0/tickets/{ticket_id}/comments

- method

post

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - suggestion
     - varchar
     - 是
     - 处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）

- 返回数据

::

  {
    "code": 0,
    "msg": "",
    "data": {}
  }


--------------------
工单hook回调
--------------------

- url

api/v1.0/tickets/{ticket_id}/hook_call_back

- method

post

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - result
     - boolean
     - 是
     - hook任务执行是否成功， false, true
   * - msg
     - varchar
     - 是
     - hook执行输出信息,可留空''
   * - field_value
     - dict object
     - 否
     - 需要修改值的字段. 这些字段需要在状态表单设置中为可选或者必填

- 使用场景

当工作流状态设置处理人类型为hook，工单到达此状态时，会触发hook请求，被请求方可以执行一些操作，执行完成后回调用loonflow,
告知loonflow任务执行结果，以触发loonflow中工单状态的流转(当hook配置中wait为false时，无需回调，hook发出后会立即触发流转，wait为true会等待
回调)。回调参数如果result为false,那么loonflow会标记该工单的script_run_last_result为False(获取工单详情接口也会返回此标识，前端可以根据这
个标识来显示一个重试的按钮，用户点击这个重试按钮后调用"重试工单脚本/hook任务"接口)，同时也会将msg(你可以传失败的原因)中的内容记录到工单流转记录中。

- 返回数据

::

  {
    "code": 0,
    "msg": "",
    "data": {}
  }

--------------------
工单当前的参与人详情
--------------------

- url

api/v1.0/tickets/{ticket_id}/participant_info

- method

get

- 使用场景

此接口将返回该工单当前的参与人详细信息，如果是部门或角色会返回对应部门角色下所有用户。调用方可基于此提供工单催办的功能。
用户在前端点击催办按钮，前端弹窗要求用户选择通知的类型：短信、邮件、微信、钉钉等等 以及需要的备注信息，
然后调用方后端发送相应的通知消息给工单的当前处理人

- 返回数据

::

  {
    "msg": "",
    "data": {
      "participant_info_list": [{
        "alias": "\u8d85\u7ea7\u7ba1\u7406\u5458",
        "username": "admin",
        "phone": "13888888888",
        "email": "blackholll@163.com"
      }, {
        "alias": "\u8f68\u8ff9",
        "username": "guiji",
        "phone": "13888888888",
        "email": "guiji@163.com"
      }, {
        "alias": "\u674e\u78ca",
        "username": "lilei",
        "phone": "13888888888",
        "email": "lilei@163.com"
      }, {
        "alias": "\u5f20\u4e09",
        "username": "zhangsan",
        "phone": "13888888888",
        "email": "zhangsan@163.com"
      }, {
        "alias": "\u674e\u56db",
        "username": "lisi",
        "phone": "13888888888",
        "email": "lisi@163.com"
      }, {
        "alias": "\u738b\u4e94",
        "username": "wangwu",
        "phone": "13888888888",
        "email": "wangwu@163.com"
      }, {
        "alias": "\u6770\u514b",
        "username": "jack",
        "phone": "13888888888",
        "email": "jack@163.com"
      }],
      "participant_username_list": ["admin", "guiji", "lilei", "zhangsan", "lisi", "wangwu", "jack"]
    },
    "code": 0
  }


--------------------
强制关闭工单
--------------------

- url

api/v1.0/tickets/{ticket_id}/close

- method

post

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - suggestion
     - varchar
     - 否
     - 关闭原因

- 使用场景

超级管理员在查看工单详情时，可以在界面上显示一个强制关闭工单的按钮，点击后调用关闭工单按钮，实现强制关闭工单。
另外工单创建人在工单处于初始状态下(创建人撤回、退回到初始状态等情况工单状态会处于初始状态)也可以强制关闭工单。

- 返回数据

::

  {
    "code": 0,
    "msg": "",
    "data": {}
  }



--------------------
撤回工单
--------------------

- url

api/v1.0/tickets/{ticket_id}/retreat

- method

post

- 请求参数

.. list-table::
   :header-rows: 1

   * - 参数名
     - 类型
     - 必填
     - 说明
   * - suggestion	
     - varchar
     - 否
     - 撤回原因

- 使用场景

在配置工作流状态时，可以指定某些状态下允许创建人撤回工单，那么当工单处于这些状态时，创建人可以撤回该工单(调用方前端在这个情况下显示一个撤回按钮)

- 返回数据

::

  {
    "code": 0,
    "msg": "",
    "data": {}
  }
