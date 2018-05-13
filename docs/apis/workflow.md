**工作流相关接口**

# 获取工作流列表
### URL
api/v1.0/workflows
### method
get
### 使用场景
获取到工作流列表后，用户选择对应的工作流来新建对应的工单。如果需要多级类型，可以在调用方系统保存对应关系。如调用方的“权限申请-VPN权限申请“对应loonflow中id为1的workflow,调用方的“权限申请-服务器权限申请“对应loonflow中id为2的workflow
### 请求参数

参数名 | 类型 | 必填 | 说明
---|---|---|---
page| int | 否 | 页码，默认1
per_page| int | 否 | 每页个数，默认10
username | varchar | 是 | 用户名，用于做必要的权限控制
name | varchar | 否 | 支持根据workflow name模糊查询

### 返回数据

```
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
```

# 获取工作流初始状态
### URL
api/v1.0/workflows/{workflow_id}/init_state
### method
get
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制
### 返回数据
```
{
	"data": {
		"transition": [{ # 初始状态可以做的操作，也就是新建工单时的提交路径
			"transition_name": "提交",
			"transition_id": 1
		}, {
			"transition_name": "保存",
			"transition_id": 2
		}],
		"state_field": {  # 提交工单时候需要的字段 及每个字段的读写属性
			"model": 1
		},
		"order_id": 0,
		"participant_type_id": 1,
		"sub_workflow_id": 0,
		"is_hidden": false,
		"participant": "wangfei",
		"workflow_id": 1,
		"id": 1,
		"creator": "admin",
		"type_id": 1,
		"label": {},
		"distribute_type_id": 1,
		"name": "新建中",
		"gmt_created": "2018-04-23 20:53:33"
	},
	"msg": "",
	"code": 0
}
```


# 获取工作流状态详情
### URL
api/v1.0/workflows/states/{state_id}
### method
get
### 使用场景

### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制
### 返回数据
```
{
	code: 0,
	data: {
		participant: "zhangsan",
		sub_workflow_id: 0,
		is_hidden: false,
		distribute_type_id: 1,
		state_field: {
			model: 1
		},
		order_id: 0,
		creator: "admin",
		type_id: 0,
		label: {},
		#自定义标签， json格式保存， 接口调用方可针对状态的标签字段灵活显示前端页面。 如可以设置为 {
			'appdetail': 1,
			'projectdetail': 2
		}
		表示这个状态下前端需要显示应用详情、 项目详情，含义和前端约定好就行。 loonflow只负责将配置的信息返回给前端
		gmt_created: "2018-04-23 20:53:33",
		participant_type_id: 1,
		workflow_id: 1,
		name: "新建中",
		id: 1
	},
	msg: ""
}
```