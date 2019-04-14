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
无

### 返回数据
```
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
```


# 获取工作流状态详情
### URL
api/v1.0/workflows/states/{state_id}
### method
get
### 使用场景

### 请求参数
无

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

# 获取工作流的状态列表
### URL
api/v1.0/workflows/{workflow_id}/states
### method
get
### 使用场景
可用于用户查询工单列表时选择工作流类型后，显示该工作流类型拥有的状态，然后可以再根据工单当前状态来查询
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
page | int | 否 | 第几页，默认第一页
per_page | int | 否 | 每页多少行数据
### 返回数据
{
	code: 0,
	data: {
		"total": 2,
		"page": 1,
		"per_page": 10,
		"value": [{
			"id": 1,
			"name": "发起人编辑中",
			"workflow_id": 1,
			"sub_workflow_id": 0,
			"is_hidden": 0,
			"order_id": 0,
			"participant_type_id": 5,
			"participant": "creator",
			"distribute_type_id": 1,
			"state_field_str": {
				"title": 2,
				"description": 2,
				},
			"label": {},
			"creator": "loonflow",
			"gmt_created": "2018-02-27 06:00:00"
			}]
	},
	msg: ""