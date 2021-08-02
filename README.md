# 部署
## 开发环境部署
- 修改settings/config.py下的Mysql和Redis配置(据库配置、redis地址配置、日志路径配置等等)
- 配置python虚拟环境: python3.6.x (python3.6最新稳定版)
- 安装依赖包: pip install -r requirements/dev.txt
- 启动redis(用于生成唯一的工单流水号+celery异步任务[执行脚本、状态hook、通知hook])
- 初始化数据库

```
python manage.py makemigrations
python manage.py migrate
```

- 导入数据库: 导入项目目录下的default.sql数据库
  
- 启动开发环境: python manage.py runserver 6060

- 启动celery任务: celery -A tasks worker -l info -Q loonflow (用于执行任务脚本、触发任务hook、通知hook。本地开发二次开发如果不需要这些功能时可以不启动)

- 访问http://127.0.0.1:6060/student/ 即可


## 基本架构
本项目开发思路:
- 前端界面(vue + element): 对接上后端的接口，解决跨域问题，做好表单提交
- 后端完成接口的开发，如新建工单，流程步骤，撤回工单，同意或拒绝工单，定义好路由让前端请求过来


## 开发思路
1. 接口调用鉴权 ：
    - 定义header参考[官方文档](https://loonflow.readthedocs.io/zh_CN/r2.0.5/api_docs/authentication/)
      ```
        import time 
        timestamp = str(time.time())[:10]   # 取得当前时间戳，进行切片
        ori_str = timestamp + token         # 拼接URL
        signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()   # 转换为MD5
        ```
    - API调用
        ```
      import requests

       # appname和username需要在后台设置，打开后台找到用户及权限->调用权限
       headers = dict(signature=signature, timestamp=timestamp, appname='xxx', username='xxx')
    
        # get
        get_data = dict(per_page=20, category='all')
        r = requests.get('http://127.0.0.1:6060/api/v1.0/tickets', headers=headers, params=get_data)
        result = r.json()
      
        # post
        data = dict(target_username='lisi', suggestion='请协助提供更多信息')
        r = requests.post('http://127.0.0.1:6060/api/v1.0/tickets/{ticket_id}/add_node', headers=headers, json=data)
        result = r.json()
      
        # patch
        data = dict(target_username='lisi', suggestion='请协助提供更多信息')
        r = requests.patch('http://127.0.0.1:6060/api/v1.0/tickets/{ticket_id}/add_node', headers=headers, json=data)
        result = r.json()
        ```
2. 前后端接口开发：
    - 大部分接口可以在这里找到 https://loonflow.readthedocs.io/zh_CN/r2.0.5/api_docs/ticket/
    - 新建工单接口 
      
      请求地址：api/v1.0/tickets
      
      请求方式 ：post
    
      请求参数：如下

    |参数名 |类型|必填|说明|  
    |------|---|---|---|
    |workflow_id|int|是|工作流id(工单关联的工作流的id)|
    |transition_id|int|是|新建工单时候的流转id（通过workflows/{id}/init_state接口可以获取新建工单时允许的transition）|
    |parent_ticket_id|int|否|父工单的id(用于子工单的逻辑，如果新建的工单是某个工单的子工单需要填写父工单的id)|
    |parent_ticket_state_id|int|否|父工单的状态（子工单是和父工单的某个状态关联的），如果提供parent_ticket_id，则此参数也必须）|
    |suggestion|varchar|否|处理意见（与处理工单类型，用户在处理工单的时候点击了按钮操作 可以填写附加的一些意见如:麻烦尽快处理）|
    |其他必填字段|N/A|否|其他必填字段或可选字段（在配置工作流过程中,会配置工作流初始状态必填和可选的字段。在新建工单时候必须提供必填字段。如请假申请工单，配置了自定义字段请假天数days，工单初始状态也设置了days为必填，那么新建此类工单时候就必选提供days)|

    ## Django 新建工单 Demo
    
    ### 后端部分
    
    #### 定义路由    urls.py
     ```
    from django.urls import path
    from . import views  
   
   app_name = 'student'

    urlpatterns = [
        # 渲染页面
        url(r'^new_ask/$', views.new_ask, name='new_ask'),
        
        # 数据接口
        url(r'^postform/$', views.postform, name='postform'),

    ]
    ```

    #### 编写视图函数    views.py

    ```
       # 仅用于渲染页面
        @login_required()
        def new_ask(request):
            return render(request, 'student/new_ask.html')
       
       # 提交数据接口
       @login_required()
        def postform(request):
            timestamp = str(time.time())[:10]
            ori_str = timestamp + 'f504e46a-f123-11eb-960b-f894c2bd30ac'
            signature = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
            headers = dict(signature=signature, timestamp=timestamp, appname='admin', username=request.user.username)
   
            if request.method == 'POST':
                # 取得前端提交的表单数据 
                title = request.POST['title']       # 标题
                region = request.POST['region']     # 事假或病假
                date1 = request.POST['date1']       # 开始时间
                date2 = request.POST['date2']       # 结束时间  
                days = request.POST['days']         # 请假天速
                desc = request.POST['desc']         # 请假原因
                filename = request.POST['filename'] # 附件路径
           
                # 定义需要提交数据，workflow_id代表工作流ID, transition_id是工作流中的流转的ID
                data = dict(transition_id=27, workflow_id=1, days=days, leave_end=date2,
                            leave_start=date1, leave_type=region,
                            text_desp=desc, title=title, filename=filename)
                r = requests.post('http://localhost:6060/api/v1.0/tickets', headers=headers, json=data)
                resp = r.json()
                # 如果提交成功返回数据到前端
                if resp['code'] == 0:
                    return HttpResponse(json.dumps({'code': resp['code'], 'data': resp['data'], 'msg': resp['msg']}))
                else:
                    return HttpResponse(json.dumps({'code': resp['code'], 'data': None, 'msg': resp['msg']}))
            else:
                return HttpResponse("仅支持POST请求！")     
    ```
   
    ### 前端部分
    
    #### 创建模板
    
    #### 找到根目录下的\templates\student\文件夹，在里面创建new_ask.html文件

    ### 配置前端模板 new_ask.html
   
    ```
        // 分别导入一下js和css，注意JQ需要先导入，分别是JQ，Vue，Element CSS,，Element JS, Axios, Csrf
        <script src="{% static 'bower_components/mystatic/learning_logs/jquery/jquery.min.js' %}"></script>
        <script src="{% static 'bower_components/mystatic/vue/vue.js' %}"></script>
        <link rel="stylesheet" href="{% static 'bower_components/mystatic/vue/index.css' %}">
        <script src="{% static 'bower_components/mystatic/vue/index.js' %}"></script>
        <script src="{% static 'bower_components/mystatic/vue/axios.min.js' %}"></script>
        // 解决csrf 403
        <script src="{% static 'bower_components/mystatic/csrf.js' %}"></script>

        // 定义提交的表单
        <el-form :model="ruleForm" label-width="80px" ref="ruleForm" enctype="multipart/form-data"
             :hide-required-asterisk="false">
        <el-form-item label="标题" :required="true" prop="title">
            <el-input v-model="ruleForm.title"></el-input>
        </el-form-item>
        <el-form-item label="类型" :required="true" prop="region">
            <el-select v-model="ruleForm.region">
                <el-option label="事假" value="1"></el-option>
                <el-option label="病假" value="2"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="开始时间" :required="true">
            <el-col :span="11">
                <el-date-picker prop="date1" value-format="yyyy-MM-dd HH:mm" format="yyyy-MM-dd HH:mm"
                                type="datetime"
                                placeholder="选择日期" v-model="ruleForm.date1"
                                style="width: 100%;"></el-date-picker>
            </el-col>
        </el-form-item>
    
        <el-form-item label="结束时间" :required="true">
            <el-col :span="11">
                <el-date-picker prop="date2" value-format="yyyy-MM-dd HH:mm" format="yyyy-MM-dd HH:mm"
                                type="datetime"
                                placeholder="选择日期" v-model="ruleForm.date2"
                                style="width: 100%;"></el-date-picker>
            </el-col>
        </el-form-item>
        <el-form-item label="天数" :required="true" prop="days">
            <el-input type="number" v-model="ruleForm.days"></el-input>
        </el-form-item>
    
        <el-form-item label="请假原因" :required="true" prop="desc">
            <el-input type="textarea" v-model="ruleForm.desc"></el-input>
        </el-form-item>
    
        <el-upload style="padding-left: 80px;"
                   class="upload-demo"
                   action="http://127.0.0.1:6060/student/ueditor_imgup"
                   :on-success="handleSuccess"
                   :before-remove="beforeRemove"
                   multiple
                   name="imgup"
                   id="imgup"
                   :limit="1"
                   accept=".jpg,.png,.docx"
                   :on-exceed="handleExceed"
                   :file-list="fileList">
            <el-button size="small" type="primary">点击上传附件</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png/docx文件，且不超过500kb</div>
        </el-upload>
    
        <el-form-item>
            <br>
            <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
            <el-button>取消</el-button>
        </el-form-item>
    </el-form>
    ```
    
    #### JS部分

    ```
        <script>
        var Main = {
            data() {
                return {
                    // 表格验证规则
                    rules: {
                        title: [
                            {required: true, message: '请输入标题', trigger: 'blur'},
                            {min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur'}
                        ],
                        region: [
                            {required: true, message: '请选择类型', trigger: 'change'}
                        ],
                        date1: [
                            {type: 'date', required: true, message: '请选择开始日期', trigger: 'change'}
                        ],
                        date2: [
                            {type: 'date', required: true, message: '请选择结束日期', trigger: 'change'}
                        ],
                        days: [
                            {required: true, message: '请输入天数', trigger: 'blur'},
                            {min: 1, max: 7, message: '时间在1 - 7 天', trigger: 'blur'}
                        ],
                        desc: [
                            {required: true, message: '请输入简介', trigger: 'blur'},
                            {min: 5, max: 50, message: '大约50字以内', trigger: 'blur'}
                        ],


                    },
                    ruleForm: {
                        filename: '',
                        title: '',
                        region: '',
                        date1: '',
                        date2: '',
                        days: '',
                        desc: ''
                    },
                    fileList: []
                }
            },
            methods: {
                # 此处的三个函数用于处理上传文件的事件
                handleSuccess(file, fileList){
                    this.ruleForm.filename = file['url']
                },
                handleExceed(files, fileList) {
                    this.$message.warning(`当前限制选择 1个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
                },
                beforeRemove(file, fileList) {
                    return this.$confirm(`确定移除 ${file.name}？`);
                },
                
                // 提交表单时触法
                submitForm(form) {
                    this.$refs[form].validate((valid) => {
                        if (valid) {
                            // 传入表单数据
                            $.post('/student/postform/', this.ruleForm,
                                function (result) {
                                    const obj = JSON.parse(result);
                                    if (obj['code'] === 0) {
                                        // 提交成功重定向到列表页
                                        window.location.href = '{% url 'student:index'  %}'
                                    } else {
                                        // 调试信息
                                        console.log(obj['msg'])
                                    }
                                })
                        } else {
                            return false;
                        }
                    });
                },

            }
        }
        // 关键！！！ 解决跨域错误，将csrf_token一起传入到表单当中即可解决
        $.ajaxSetup({data: {csrfmiddlewaretoken: '{{ csrf_token }}'}})

        var Ctor = Vue.extend(Main)
        new Ctor().$mount('#app')
   </script>
   ```
    #### 提交表单的效果图 
   [![WzwlAU.png](https://z3.ax1x.com/2021/08/01/WzwlAU.png)](https://imgtu.com/i/WzwlAU)

    ## Django 查看工单步骤 Demo
    ### 后端部分
    
    #### 定义路由    urls.py

     ```
    from django.urls import path
    from . import views  
   
   app_name = 'student'

    urlpatterns = [
        # 渲染页面
         path('setup/<path:id>/', views.setup, name='setup'),
        
        # 数据接口
         path('flowsteps/<path:id>/', views.flowsteps, name='flowsteps'),

    ]
    ```

    #### 编写视图函数    views.py

    ```
     # 仅用于渲染页面
     @login_required()
     def setup(request, id):
        return render(request, 'student/setup.html')
   
   
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
    
    ```
   
    ### 前端部分

    #### 在模板目录中创建setup.html文件
    
    #### 配置前端模板 setup.html 

    ```
        <br>
        <el-steps :active="active" finish-status="success">
            <el-step v-for="(item,index) in titleList" :title="item.title" :description="item.description" :key="index"
                     @click.native="stepChange(index+1)"></el-step>
        </el-steps>
        <br>

        <el-form ref="form" :model="form" label-width="80px">

            <el-form-item label="标题">
                <el-input v-model="form.title" :disabled="true"></el-input>
            </el-form-item>

            <el-form-item label="类型">
                <el-select v-model="form.region" placeholder="请选择类型" :disabled="true">
                    <el-option label="事假" value="0"></el-option>
                    <el-option label="病假" value="1"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="开始时间">
                <el-col :span="11">
                    <el-date-picker :disabled="true" value-format="yyyy-MM-dd HH:mm" format="yyyy-MM-dd HH:mm"
                                    type="datetime" placeholder="选择日期" v-model="form.date1"
                                    style="width: 100%;"></el-date-picker>
                </el-col>
            </el-form-item>

            <el-form-item label="结束时间">
                <el-col :span="11">
                    <el-date-picker :disabled="true" value-format="yyyy-MM-dd HH:mm" format="yyyy-MM-dd HH:mm"
                                    type="datetime" placeholder="选择日期" v-model="form.date2"
                                    style="width: 100%;"></el-date-picker>
                </el-col>
            </el-form-item>

            <el-form-item label="请假天数">
                <el-input v-model="form.days" :disabled="true"></el-input>
            </el-form-item>

            <el-form-item label="请假原因">
                <el-input type="textarea" v-model="form.desc" :disabled="true"></el-input>
            </el-form-item>

            <el-form-item label="附件下载">
                <el-input type="text" v-model="form.filename"></el-input>
            </el-form-item>

        </el-form>

        <el-row>
            {% if request.user.type_id == 1 or request.user.type_id == 2 %}
                {#管理员显示操作按钮#}
                <el-button type="success" @click="Details()">同意申请</el-button>
                <el-button type="danger" @click="Cancel()">退回工单</el-button>
            {% else %}
                {#非管理员仅能查看，无法同意或退回#}
            {% endif %}
        </el-row>
    ```
    
    #### JS部分

    ```
        <script>
        // 取得URL ID
        let url_id = window.location.pathname.split('/')[3]
        var Main_setup = {
            created() {
                // 取得步骤
                axios.get('/student/flowsteps/' + url_id + '/').then(response => {
                        if (response.statusText === 'OK') {
                            for (let i = 0; i < response.data.data.value.length; i++) {
                                for (let j = 0; j < response.data.data.value[i]['state_flow_log_list'].length; j++) {
                                    // 拼接字符串 张三同学 + 提交 + @2021-08-01 15:09:22
                                    let participant_info = response.data.data.value[i]['state_flow_log_list'][j]['participant_info']['participant_alias']
                                    let transition_name = response.data.data.value[i]['state_flow_log_list'][j]['transition']['transition_name']
                                    let gmt_created = response.data.data.value[i]['state_flow_log_list'][j]['gmt_created']
   
                                    for (let k = 0; k < this.titleList.length; k++) {
                                        // 效果：张三同学提交@2021-08-01 15:09:22
                                        this.titleList[i]['description'] = participant_info + transition_name + '@' + gmt_created
                                    }
                                }
                                // 判断状态ID current_state_id来识别当前流转到哪了，然后修改this.active的值即可
                                if (response.data.data['current_state_id'] === 1) {
                                    this.active = 1
                                } else if (response.data.data['current_state_id'] === 3) {
                                    this.active = 2
                                } else if (response.data.data['current_state_id'] === 5) {
                                    this.active = 3
                                }
                            }
                        } else {
                            // 提示消息
                            this.$message({
                                showClose: true,
                                message: '数据加载失败！',
                                type: 'error'
                            });
                        }
                    },
                    response => {
                        console.log("error");
                    }
                );

                // 取得当前工单状态，并显示到表单上
                axios.get('/student/states/' + url_id + '/').then(response_states => {
                        if (response_states.statusText === 'OK') {
                            for (let i = 0; i < response_states.data.data.value['field_list'].length; i++) {
                                let field_key = response_states.data.data.value['field_list'][i]['field_key']
                                // 此处的field_key为后台中的，工作流配置->自定义字段
                                if (field_key === 'days') {
                                    this.form.days = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'text_desp') {
                                    this.form.desc = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'title') {
                                    this.form.title = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'leave_start') {
                                    this.form.date1 = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'leave_end') {
                                    this.form.date2 = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'leave_type') {
                                    this.form.region = response_states.data.data.value['field_list'][i]['field_value']
                                } else if (field_key === 'filename') {
                                    if (response_states.data.data.value['field_list'][i]['field_value'] === ''){
                                        this.form.filename = '当前无附件'
                                    }else{
                                        // 附件的下载地址
                                        this.form.filename = 'http://127.0.0.1:6060' + response_states.data.data.value['field_list'][i]['field_value']
                                    }

                                }

                            }
                        } else {
                            this.$message({
                                showClose: true,
                                message: '数据加载失败！',
                                type: 'error'
                            });
                        }
                    },
                    response_states => {
                        console.log("error");
                    }
                );
            },

            data() {
                return {
                    active: 1,  // 当前步骤
                    titleList: [
                        {
                            title: '发起人-新建中',
                            description: '新建中...'
                        },
                        {
                            title: '教师审批',
                            description: '等待审批...'
                        },
                        {
                            title: '结束',
                            description: '已结束...'
                        },
                    ],
                    form: {
                        title: '',
                        region: '',
                        date1: '',
                        date2: '',
                        days: '',
                        desc: ''
                    }
                };
            },

            methods: {
                // 同意工单
                Details() {
                    if (this.active >= 3) {
                        this.$message('工单已完结');
                    } else {
                        // 同意工单
                        axios.get('/student/accept_tickets_submit/' + url_id + '/').then(response_accept_tickets_submit => {
                            console.log(response_accept_tickets_submit);
                            if (response_accept_tickets_submit['code'] === 0) {
                                console.log('同意工单！')
                            }
                        }, response => {
                            console.log("error");
                        });
                        window.location.reload()
                    }
                },
                // 退回工单
                Cancel() {

                    if (this.active >= 3) {
                        this.$message('工单已完结');
                    } else {
                        axios.get('/student/close_tickets/' + url_id + '/').then(response_close_tickets=> {
                            if (response_close_tickets['code'] === 0) {
                                console.log('工单撤回成功！')
                                window.location.reload()
                            }
                        }, response => {
                            console.log("error");
                        });
                    }
                }


            }
        }
        var Ctor = Vue.extend(Main_setup)
        new Ctor().$mount('#app')
    </script>
    ```
   
    #### 步骤图页面效果图
    [![Wzr4Ln.png](https://z3.ax1x.com/2021/08/01/Wzr4Ln.png)](https://imgtu.com/i/Wzr4Ln)

    ## Django 同意或拒绝工单 Demo

    #### 定义路由   定义视图函数
    
    #### urls.py

    ```
    from django.urls import path
    from . import views  
   
   app_name = 'student'

    urlpatterns = [
        # 同意
        path('accept_tickets_submit/<path:id>/', views.accept_tickets_submit, name='accept_tickets_submit'),
        # 拒绝               
        path('close_tickets/<path:id>/', views.close_tickets, name='close_tickets'),

    ]
    ```
   #### views.py
        
    ```
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
    ```

    #### 前端接口调用

    setup.html 模板中添加这两个函数
    ```
                // 同意工单
                Details() {
                    if (this.active >= 3) {
                        this.$message('工单已完结');
                    } else {
                        // 同意工单
                        axios.get('/student/accept_tickets_submit/' + url_id + '/').then(response_accept_tickets_submit => {
                            console.log(response_accept_tickets_submit);
                            if (response_accept_tickets_submit['code'] === 0) {
                                console.log('同意工单！')
                            }
                        }, response => {
                            console.log("error");
                        });
                        window.location.reload()
                    }
                },
                // 退回工单
                Cancel() {

                    if (this.active >= 3) {
                        this.$message('工单已完结');
                    } else {
                        axios.get('/student/close_tickets/' + url_id + '/').then(response_close_tickets=> {
                            if (response_close_tickets['code'] === 0) {
                                console.log('工单撤回成功！')
                                window.location.reload()
                            }
                        }, response => {
                            console.log("error");
                        });
                    }
                }
    ```
    
## 效果图
### 提交请假
![效果图1](https://i.loli.net/2021/08/01/brcEpqVsDC4adFT.gif)
### 老师同意请假
<<<<<<< HEAD
![效果图2](https://i.loli.net/2021/08/01/wMVzJfqL4C78QbN.gif)
=======
![效果图2](https://i.loli.net/2021/08/01/wMVzJfqL4C78QbN.gif)
>>>>>>> 1ed3a9f898a3310eac00bceb5eefeef4757ecaf7
