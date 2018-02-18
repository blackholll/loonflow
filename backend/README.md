#loonflow 后端
### 运行开发环境
- 创建数据库: 根据backend/settings/dev.py中的配置创建数据库
- 创建python虚拟环境: python3.5
- 安装依赖包: pip install -r backend/requirements/dev.txt
- 初始化数据库: 

        python manage.py makemigrations
        python manage.py migrate
- 初始化数据: python manage.py loaddata notice_type.json
- 创建初始账户: python manage.py createsuperuser
