#!/usr/bin/env python
#._*_coding:utf-8 _*

from exts import db
from flask_sqlalchemy import SQLAlchemy
import time

# 创建用户模型
class User(db.Model):
    __tablename__ ='user'
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)



class Diary(db.Model):
    __tablename__ = 'diary'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # now()获取服务器第一次运行的时间
    # now就是每次创建一个模型的时候，都获取当前的时间。
    # create_time = db.Column(db.DateTime,default=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User',backref=db.backref('diarys'))

    # 查询某篇文章的作者：Question
    # question = Question.query.filter(question.title == 'aaa').first()
    # question.user.username

    # 查询某作者的所有文章：
    # user = User.query.filter(User.username=='17839270952').first()
    # user.questions

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)

    comment_id = db.Column(db.Integer, db.ForeignKey('diary.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    diary = db.relationship('Diary', backref=db.backref('comments'))
    # question = db.relationship('Question', backref=db.backref('answers',order_by=id.desc()))
    user = db.relationship('User', backref=db.backref('comments'))