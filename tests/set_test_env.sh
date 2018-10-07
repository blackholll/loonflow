#!/bin/bash

# 从开发环境导出数据，并导入到测试环境


echo "                                     "
echo "                                     "
echo "########### 开始从开发环境导出数据 ###########"
/usr/local/mysql/bin/mysqldump  -uloonflownew loonflownew >  testloonflow.sql
echo "                                     "
echo "                                     "
echo "########### 导出数据完成 ###########"

echo "                                     "
echo "                                     "
echo "########### 开始导入数据到测试环境,输入测试环境数据库密码 ###########"
/usr/local/mysql/bin/mysql -uloonflownew -h127.0.0.1 -p test_loonflownew < "testloonflow.sql"
echo "                                     "
echo "                                     "

echo "########### 完成数据初始化 ###########"

echo "                                     "
echo "                                     "

echo "你现在可以在上级目录执行python manage.py test tests/ --keepdb开始单元测试了"
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
