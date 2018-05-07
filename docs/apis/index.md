# Loonflow v0.1 api
Loonflow作为工作流引擎，正确是的使用姿势是各个系统通过http api调用按照各自的需求来完成工单展示、工单新建、工单处理逻辑
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

header = dict(signature=signature, timestamp=timestamp, appname=app_name) # header不允许设置参数名包含'-'
header.update({'Content-Type': 'application/json; charset=UTF-8'})

r = requests.get('http://127.0.0.1:8000/api/v1.0/tickets')
result = r.json()

```
## API
[工单相关接口](./ticket.md)
[工作流相关接口](./workflow.md)


## 常量定义
见文档首页的"常量定义"