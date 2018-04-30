# 获取工单列表
### URL
/api/v1.0/tickets
### method
GET
### 请求参数

参数名 | 类型 | 必填 | 说明
---|---|---|---
page| int | 否 | 页码，默认1
per_page| int | 否 | 每页个数，默认10
username | varchar | 是 | 用户名
category | varchar | 是 | 类型('all':所有工单, 'owner':我创建的工单, 'duty':我的待处理工单, 'relation':我的关联工单[包括我新建的、我处理过的、曾经需要我处理过的工单。注意这里只考虑历史状态，工单将来状态的处理人不考虑])

### 返回数据

```
{
  code: 0,
  msg: "",
  data: {
    per_page: 10,
    total: 2,
    page: 1,
    value: [{
      title: "title",
      participant_type_id: 1,
      state:{
        state_id: 1,
        state_name: 发起人-编辑中
      }
      parent_ticket_id: 0,
      gmt_modified: "2018-04-10 16:48:43",
      workflow_id: 1,
      sn: "loonflow201804010001",
      parent_ticket_state_id: 0,
      gmt_created: "2018-04-10 16:48:43",
      creator: "admin",
      participant: "admin"
    },
    {
      title: "dfdsfsfsdf",
      participant_type_id: 0,
      state:{
        state_id: 1,
        state_name: 发起人-编辑中
      }
      parent_ticket_id: 0,
      gmt_modified: "2018-04-10 16:43:20",
      workflow_id: 1,
      sn: "loonflow201804010002",
      parent_ticket_state_id: 0,
      gmt_created: "2018-04-10 16:43:20",
      creator: "wangfei",
      participant: "wangfei"
    }
    ]}
}
```

# 新建工单
### URL
/api/v1.0/tickets
### method
POST
### 请求参数

参数名 | 类型 | 必填 | 说明
---|---|---|---
workflow_id | int | 是 | 工作流id(工单关联的工作流的id)
username | varchar | 是 | 新建工单的用户名
parent_ticket_id| int | 否 | 父工单的id(用于子工单的逻辑，如果新建的工单是某个工单的子工单需要填写父工单的id)
parent_ticket_state_id | varchar | 否 | 父工单的状态（子工单是和父工单的某个状态关联的）
suggestion | varchar | 否 | 处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）
其他必填字段 | NULL | 否 | 其他必填字段或可选字段（在配置工作流过程中,会配置工作流初始状态必填和可选的字段。在新建工单时候必须提供必填字段。如请假申请工单，配置了自定义字段请假天数days，工单初始状态也设置了days为必填，那么新建此类工单时候就必选提供days)
### 返回数据
```
{
  code: 0,
  msg: "",
  data: {
      ticket_id : 1  # 新建的工单的工单id
    }
}
```

# 获取工单详情
### URL
/api/v1.0/tickets/{ticket_id}

### method
GET

### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名

### 返回数据
```
{
  msg: "",
  code: 0,
  data: {
    value: {
      state_id: 1,
      id: 1,
      gmt_created: "2018-04-10 16:43:20",
      gmt_modified: "2018-04-10 16:43:20",
      sn: "loonflow201804010001",  # 工单流水号
      field_list: [{   # 需要显示的字段
        field_choice: [ ], #字段的选项，用于radio\checkbox\select等需要选择的字段，是一个字典的list,如[{1:'中国', 2:'美国', 3:'英国'}]
        field_attribute: 1, #字段的编辑属性，只读、必填、可选，具体定义见文档首页的"常量定义"
        field_name: "型号",
        field_value: null,
        order_id: 0,
        field_type_id: 1,
        field_key: "model"
      }],
      participant_type_id: 0,
      title: "dfdsfsfsdf",
      participant: "wangfei",
      workflow_id: 1,
      creator: "wangfei",
      parent_ticket_id: 0
    }
  }
}
```

# 获取工单可以做的操作
### URL
/api/v1.0/ticket/{ticket_id}/transitions
### method
GET
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名

### 返回数据
```
{
  msg: "",
  data: {
    value: [
      {
        transition_name: "提交",
        transition_id: 1
      },
      {
        transition_name: "保存",
        transition_id: 2
      }
    ]
    },
  code: 0
}
```

# 处理工单
### URL
api/v1.0/tickets/{ticket_id}
### method
patch
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名
transition_id | int | 是 | 流转id
suggestion | varchar | 否 | 处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）
其他必填字段 | NULL | 否 | 其他必填字段或可选字段（在配置工作流过程中,会配置工作流每个状态的必填和可选的字段。在处理工单时候必须提供必填字段。如请假申请工单，配置了自定义字段请假天数days，工单初始状态也设置了days为必填，那么处理此类工单时候就必选提供days)

### 返回数据
```
{
  msg: "",
  data: "",
  code: 0
}
```

# 获取工单流转记录
### URL
api/v1.0/tickets/{ticket_id}/flowlogs
### method
get
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制
### 返回数据
```
{
  msg: "",
  data: {
    total: 4,
    value: [
      {
        state: {
          state_name: "发起人-确认中",
          state_id: 5
        },
        transition: {
          transition_name: "确认完成",
          transition_id: 5
        },
        ticket_id: 1,
        gmt_modified: "2018-04-30 15:57:26",
        gmt_created: "2018-04-30 15:56:02",
        suggestion: "已经生效，感谢"
      },
      {
      state: {
        state_name: "技术人员-处理中",
        state_id: 4
        },
      transition: {
        transition_name: "处理完成",
        transition_id: 4
      },
      ticket_id: 1,
      gmt_modified: "2018-04-30 15:57:14",
      gmt_created: "2018-04-30 15:55:32",
      suggestion: "处理完成"
      },
      {
      state: {
        state_name: "TL审批中",
        state_id: 3
      },
      transition: {
        transition_name: "同意",
        transition_id: 3
      },
      ticket_id: 1,
      gmt_modified: "2018-04-30 15:57:00",
      gmt_created: "2018-04-30 15:53:19",
      suggestion: "同意处理"
      },
      {
      state: {
        state_name: "新建中",
        state_id: 1
      },
      transition: {
        transition_name: "提交",
        transition_id: 1
      },
      ticket_id: 1,
      gmt_modified: "2018-04-30 15:52:35",
      gmt_created: "2018-04-10 17:39:33",
      suggestion: "请尽快处理，谢谢"
      }],
    page: 1,
    per_page: 10
    },
  code: 0
}
```

# 工单处理步骤记录
### URL
api/v1.0/tickets/{ticket_id}/flowsteps
### method
get
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制

### 返回数据
```
{
  data: {
  value: [
    {
      state_name: "新建中",
      state_flow_log_list: [
        {
          state_id: 1,
          suggestion: "请尽快处理，谢谢",
          gmt_created: "2018-04-10 17:39:33",
          id: 1
        }],
      state_id: 1
    },
    {
      state_name: "TL审批中",
      state_flow_log_list: [
        {
          state_id: 3,
          suggestion: "同意处理",
          gmt_created: "2018-04-30 15:53:19",
          id: 2
        }],
      state_id: 3
      },
    {
      state_name: "技术人员-处理中",
      state_flow_log_list: [
        {
          state_id: 4,
          suggestion: "处理完成",
          gmt_created: "2018-04-30 15:55:32",
          id: 3
        }],
      state_id: 4
      },
    {
      state_name: "发起人-确认中",
      state_flow_log_list: [
      {
        state_id: 5,
        suggestion: "已经生效，感谢",
        gmt_created: "2018-04-30 15:56:02",
        id: 4
      }],
      state_id: 5
    },
    {
      state_name: "结束",
      state_flow_log_list: [ ],
      state_id: 6
    }]
  },
  msg: "",
  code: 0
}
```

# 修改工单状态
### URL
api/v1.0/tickets/{ticket_id}/state
### method
put
### 使用场景
用于干预工单的当前状态,可以直接将工单状态修改为指定状态，系统会根据state_id获取对应的处理人信息
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制
state_id | int | 是 | 目标状态id
### 返回格式
```
{
  msg: "",
  data: "",
  code: 0
}
```

# 批量获取工单状态
### URL
api/v1.0/tickets/states
### method
get
### 请求参数
参数名 | 类型 | 必填 | 说明
---|---|---|---
username | varchar | 是 | 请求用户的用户名,用于做必要的权限控制
ticket_ids | str | 是 | 工单ids,逗号隔开的字符串
### 返回数据
```
{
  code: 0,
  data: {
    1: {
        state_id: 1,
        state_name: "发起人-编辑中"
      },
    2: {
        state_id: 2,
        state_name: "新建中"
      }
  },
  msg: ""
}
```

# 获取工单状态详情
### URL
api/v1.0/workflow/states/{state_id}
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
    participant: "wangfei",
    sub_workflow_id: 0,
    is_hidden: false,
    distribute_type_id: 1,
    state_field: {
    model: 1
    },
    order_id: 0,
    creator: "admin",
    type_id: 0,
    label: { },  # 自定义标签，json格式保存，接口调用方可针对状态的标签字段灵活显示前端页面。如可以设置为{'appdetail':1,'projectdetail':2}表示这个状态下前端需要显示应用详情、项目详情，含义和前端约定好就行。loonflow只负责将配置的信息返回给前端
    gmt_created: "2018-04-23 20:53:33",
    participant_type_id: 1,
    workflow_id: 1,
    name: "新建中",
    id: 1
  },
  msg: ""
  }
```




