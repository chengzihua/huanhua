#!/usr/bin/env python
#._*_coding:utf-8 _*_

import os

DEBUG = True

SECRET_KEY = os.urandom(24)


DIALECT = 'mysql'
DRIVER = 'mysqlconnector'     #驱动
USERNAME='root'     #用户名
PASSWORD = 'hua1012'   #密码
HOST = '127.0.0.1'     #域名/IP
PORT ='3306'           #端口号
DATABASE = 'huanhua'  #创建的数据库名

#指定给固定的变量sqlalchemy会在config文件中读取该变量。
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
