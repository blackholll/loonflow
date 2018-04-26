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
      state_id: 1,
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
      state_id: 1,
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

