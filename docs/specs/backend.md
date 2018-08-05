# 编码规范
原则上要求按照PEP8规范来执行
### 目录结构

```
apps: 存放app
    account: 具体的app目录， view目录里面代码只处理request请求，具体逻辑调用service里面的类方法来完成
loonflow: 项目路由入口
    __init 
    urls.py
    wsgi.py
requirements:库依赖
    common.txt:通用依赖
    dev.txt: 开发环境依赖
    pro.txt: 生产环节依赖
    test.txt: 测试环境依赖
service:服务层目录，主要是一些具体的逻辑，如数据库操作，缓存操作等等
settings:配置文件目录
    __init__.py
    common.py: 通用配置
    dev.py: 开发环境配置
    pro.py: 生产环境配置
    test.py: 测试环境配置
static: 静态文件目录
media: 存放用户上传的目录，生产环境部署时建议存放到其他路径， 方便迁移
manage.py
uwsgi.py
README.md:说明性文字
```
### 注释规范

```
class AccountService(BaseService):
    """
 用户相关服务
 """
 def __init__(self):
        pass
 
 @auto_log
 def get_user_auth_type(self, username):
    """
    获取用户登录类型
    :param username:
    :return:
    """
    user_info = MyUser.objects.filter(username=username)
    if user_info:
        auth_type = user_info[0].auth_type
    else:
        auth_type = '2'
        return auth_type, ''
```
### 函数返回值规范

```
函数返回一个元祖， 第一个参数是布尔类型（True, False）或者对象, 第二是message信息(可以是对错误信息的描述)
推荐使用auto_log装饰器来做异常处理。 内如如下
def auto_log(func):
    """
    自动记录日志的装饰器：
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logging.error(traceback.format_exc())
            return False, e.__str__()
    return _deco

```
### 代码提交

migrations目录下除了__init__.py以外文件不要提交，否则多人提交，导致本地数据库同步会有问题

### 更加Pythonic的模型写法
通用字段使用CommonModel抽象模型，如：（不过因为此方法定义的model，migrate生成的数据库，字段顺序不好灵活控制，暂时未实际遵循）
```python
from django.db import models
from django.utils.translation import ugettext_lazy as _

class CommonModel(models.Model):
    creator = models.CharField(verbose_name=_('创建人'), max_length=100)
    created = models.DateTimeField(verbose_name=_('创建时间'), auto_now=True)
    modified = models.DateTimeField(verbose_name=_('修改时间'), auto_now=True)
    deleted = models.BooleanField(verbose_name=_('己删除'), default=False)

    class Meta:
        abstract = True
```
真实的模型继承该抽象模型即可，如：
```python
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.common_model import CommonModel


class TicketRecord(CommonModel):
    title = models.CharField(verbose_name=_('标题'), max_length=200, blank=True)
    workflow = models.IntegerField(verbose_name=_('关联工作流程'))
    sn = models.BigIntegerField(verbose_name=_('流水号'))
    current_state = models.IntegerField(verbose_name=_('当前状态'))
    items = models.TextField(verbose_name=_('工单内容'), help_text='工单内容，以json数据表示')
    description = models.TextField(verbose_name=_('工单描述'))

    class Meta:
        db_table = 'ticket_record'

```