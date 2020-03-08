============
接口调用鉴权
============

Loonflow作为工作流引擎，正确是的使用姿势是各个系统的后端通过http api调用按照各自的需求来完成工单展示、工单新建、工单处理逻辑
在loonflow的管理后台中"账户-调用token"中新新增记录.填写调用方app_name新增后会生成一个签名token.调用方将签名信息写到
http header中来调用具体的api 签名算法如下:
::

  import time
  timestamp = str(time.time())[:10]
  ori_str = timestamp + token
  signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()

api调用:
::

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

注意: 开发阶段如果需要在postman中测试接口，避免每次都需要重新生成签名，可以将service.permission.api_permission.ApiPermissionCheck中签名有效期改长些