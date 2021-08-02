import hashlib
import json
import os
import time

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@login_required()
def index(request):
    return render(request, 'student/index.html')


@login_required()
def new_ask(request):
    return render(request, 'student/new_ask.html')


@login_required()
def setup(request, id):
    return render(request, 'student/setup.html')


@login_required()
def postform(request):
    """ 提交数据接口 """
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    if request.method == 'POST':
        # 未提交数据：创建一个表单
        # POST提交的数据，对数据进行处理
        print(request.POST)
        title = request.POST['title']
        region = request.POST['region']
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        days = request.POST['days']
        desc = request.POST['desc']
        filename = request.POST['filename']
        data = dict(transition_id=27, workflow_id=1, days=days, leave_end=date2,
                    leave_start=date1, leave_type=region,
                    text_desp=desc, title=title, filename=filename)

        r = requests.post('http://localhost:6060/api/v1.0/tickets', headers=headers, json=data)
        resp = r.json()
        if resp['code'] == 0:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': resp['data'], 'msg': resp['msg']}))
        else:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': None, 'msg': resp['msg']}))
    else:
        return HttpResponse("仅支持POST请求！")


@login_required()
def lists(request):
    """ 列表接口 """
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    if request.user.type_id == 1 or request.user.type_id == 2:
        get_data = dict(per_page=300, category='all')
        r = requests.get('http://localhost:6060/api/v1.0/tickets', headers=headers, params=get_data)
        resp = r.json()

        if resp['code'] == 0:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': resp['data'], 'msg': resp['msg']}))
        else:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': None, 'msg': resp['msg']}))
    else:
        get_data = dict(per_page=300, category='owner')
        r = requests.get('http://localhost:6060/api/v1.0/tickets', headers=headers, params=get_data)
        resp = r.json()

        if resp['code'] == 0:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': resp['data'], 'msg': resp['msg']}))
        else:
            return HttpResponse(json.dumps({'code': resp['code'], 'data': None, 'msg': resp['msg']}))


@login_required()
def info(request, id):
    """ 查询单个工单接口 """
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    get_data = dict(per_page=300, category='all')
    r = requests.get('http://localhost:6060/api/v1.0/tickets/' + id, headers=headers, params=get_data)
    result = r.json()

    if result['code'] == 0:
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


@login_required()
def flowsteps(request, id):
    """ 查看流程步骤 """
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    r = requests.get('http://127.0.0.1:6060/api/v1.0/tickets/' + id + '/flowsteps', headers=headers)
    result = r.json()
    if result['code'] == 0:
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


@login_required()
def states(request, id):
    """ 获取工单详情"""
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    r = requests.get('http://127.0.0.1:6060/api/v1.0/tickets/' + id, headers=headers)
    result = r.json()
    if result['code'] == 0:
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


@login_required()
def accept_tickets_submit(request, id):
    # 同意工单
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)

    r = requests.post('http://127.0.0.1:6060/api/v1.0/tickets/' + id + '/accept', headers=headers)
    result = r.json()
    if result['code'] == 0:
        data = dict(transition_id=28)
        r = requests.patch('http://127.0.0.1:6060/api/v1.0/tickets/' + id, headers=headers, json=data)
        result = r.json()
        if result['code'] == 0:
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(result))
    else:
        return HttpResponse('接单失败！')


@login_required()
def close_tickets(request, id):
    # 拒绝工单
    timestamp = str(time.time())[:10]
    ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
    signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
    headers = dict(signature=signature, timestamp=timestamp, appname='admin', username='admin')
    get_data = dict(suggestion='意见')
    r = requests.post('http://127.0.0.1:6060/api/v1.0/tickets/' + id + '/close', headers=headers, json=get_data)

    result = r.json()
    if result['code'] == 0:
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


def format_file_name(name):
    """
    去掉名称中的url关键字
    """
    URL_KEY_WORDS = ['#', '?', '/', '&', '.', '%']
    for key in URL_KEY_WORDS:
        name_list = name.split(key)
        name = ''.join(name_list)
    return name


def upload_file(file_obj, file_type='pic'):
    if file_obj:
        filename = file_obj.name
        # filename = file_obj.name.decode('utf-8', 'ignore')
        filename_list = filename.split('.')
        file_postfix = filename_list[-1]  # 后缀
        # if file_postfix in ['txt', 'sql']:
        filename_list_clean = filename_list[:-1]
        file_name = ''.join(filename_list_clean) + str(int(time.time() * 1000))
        file_name = format_file_name(file_name)
        # else:
        #     file_name = str(uuid.uuid1())
        sub_folder = time.strftime("%Y%m")
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload', sub_folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        absolute_path = os.path.join(upload_folder, file_name) + '.%s' % file_postfix
        if file_postfix.lower() in (
            "sql", "jpg", "jpeg", "bmp", "gif", "png", "xls", "xlsx", "rar", "doc", "docx", "zip", "pdf", "txt", "swf",
                "wmv"):
            destination = open(absolute_path, 'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()

            # if file_type == 'pic':  #暂不剪切图片
            #     if file_postfix.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
            #         im = Image.open(absolute_path)
            #         im.thumbnail((720, 720))
            #         im.save(absolute_path)

            real_url = os.path.join('/media/', 'upload', sub_folder, file_name) + '.%s' % file_postfix
            response_dict = {'original': filename, 'url': real_url, 'title': 'source_file_tile', 'state': 'SUCCESS',
                             'msg': ''}
        else:
            response_dict = {'original': filename, 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                             'msg': 'invalid file format'}
    else:
        response_dict = {'original': '', 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                         'msg': 'invalid file obj'}
    return json.dumps(response_dict)


@csrf_exempt
def ueditor_uploadimage(request):
    """
    上传图片
    :param request:
    :return:
    """
    fileObj = request.FILES.get('imgup', None)
    print(request.FILES.get('imgup'))
    response = upload_file(fileObj, 'pic')
    return HttpResponse(response)


@csrf_exempt
def ueditor_uploadfile(request):
    """ 上传文件 """
    fileObj = request.FILES.get('upfile', None)
    response = upload_file(fileObj, 'file')
    return HttpResponse(response)