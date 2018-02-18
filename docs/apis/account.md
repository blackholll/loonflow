# 获取用户列表
### URL
/accounts/users
### method
GET
### 请求参数

参数名 | 类型 | 必填 | 说明
---|---|---|---
page| int | 否 | 页码，默认1
per_page| int | 否 | 每页个数，默认10
username | varchar | 否 | 用户名，模糊查询
alias | varchar | 否 | 姓名， 模糊查询
### 返回数据

```
{
    "code": 200,
    "data": {
        "total": 2,
        "per_page": 10,
        "page": 1,
        "value": [
            {
                "id": 1,
                "username": "admin",
                "alias": "",
                "email": "blackholll@163.com",
                "phone": "",
                "dept": {
                    "dept_id": 1
                    "dept_name": "总部"
                    }
                "is_active": true,
                "gmt_modified": "2018-02-13 15:38:29",
                "is_deleted": false,
            },
            {
                "id": 4,
                "username": "sdfsf",
                "alias": "fdsfdsf",
                "email": "fsdf@163.com",
                "phone": "11111",
                "dept": {
                    "dept_id": 1
                    "dept_name": "总部"
                    },
                "is_active": true,
                "gmt_modified": "2018-02-13 15:46:05",
                "is_deleted": false,
            }
        ]
    },
    "msg": ""
}
```
