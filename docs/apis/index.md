# Loonflow v0.3 api
Loonflow作为工作流引擎，正确是的使用姿势是各个系统的后端通过http api调用按照各自的需求来完成工单展示、工单新建、工单处理逻辑
## 调用授权
在loonflow的管理后台中"账户-调用token"中新新增记录.填写调用方app_name新增后会生成一个签名token.调用方将签名信息写到http header中来调用具体的api
签名算法如下:
```
import time
timestamp = str(time.time())[:10]
ori_str = timestamp + token
signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
```
api调用:
```
import requests

headers = dict(signature=signature, timestamp=timestamp, appname=app_name, username=username)

# get
get_data = dict(per_page=20, category='all')
r = requests.get('http://127.0.0.1:8000/api/v1.0/tickets', headers=headers, params=get_data)
result = r.json()

# post
data = dict(target_username='lisi', suggestion='请协助提供更多信息')
r = requests.post('http://127.0.0.1:8000/api/v1.0/tickets/{ticket_id}/add_node', headers=headers, json=data)
result = r.json()

# patch
requsts.patch,传参同post

# put
requests.put, 传参同post


```

## 注意
settings/dev中将签名校验部分(service.permission.api_permission.ApiPermissionCheck)注释掉了。settings/pro中开启的


## API
[工单相关接口](./ticket.md)
[工作流相关接口](./workflow.md)

## API调用逻辑
#### 新建工单
![admin_homapage](/docs/images/new_ticket.jpg)

#### 处理工单
![admin_homapage](/docs/images/handle_ticket.jpg)



## 常量定义
见文档首页的"常量定义"