#!/usr/bin/env python
#._*_coding:utf-8 _*_

from flask import Flask,render_template,request,redirect,url_for,session
from exts import db
import config
from models import User,Diary,Comment
from sqlalchemy import or_
import time
from datetime import datetime


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # print(datetime.now())
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    #得到具体的年月日，时分秒
    return render_template('homepage.html')


@app.route('/homestay/')
def homestay():
    return render_template('homestay.html')

@app.route('/snack/')
def snack():
    return render_template('snack.html')

@app.route('/picking/')
def picking():
    return render_template('picking.html')

@app.route('/surrounding_scenic/')
def surrounding_scenic():
    return render_template('surrounding_scenic.html')



@app.route('/populardiary/')
def populardiary():
    context = {
        'diarys': Diary.query.all()
        # 'questions':Question.query.order_by('create_time').all()
    }
    return render_template('populardiary.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login_regist.html')

    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return render_template('homepage.html')
            # return redirect(url_for('index'))
        else:
            return '用户名或密码错误，请确认后再登录！'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('login_regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #手机号码验证，如果已经注册过，则不能再次注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已经注册，请更换手机号码'
        else:
            #两个密码相等才可以
            if password1 != password2:
                return '两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()

                # 返回到登录界面
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    # 删除sesion的id
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.route('/write_diary/',methods=['GET','POST'])
def write_diary():
    if request.method == 'GET':
        return render_template('write_diary.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        diary = Diary(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        diary.user = user
        db.session.add(diary)
        db.session.commit()
        # create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        return redirect(url_for('populardiary'))

@app.route('/diary_detail/<diary_id>')
def diary_detail(diary_id):
    diary_model = Diary.query.filter(Diary.id == diary_id).first()
    return render_template('diary_detail.html',diary=diary_model)


@app.route('/add_comment/',methods=['POST'])
def add_comment():
    content = request.form.get('comment_content')
    diary_id = request.form.get('diary_id')
    comment = Comment(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.user = user
    diary = Diary.query.filter(Diary.id == diary_id).first()
    comment.diary = diary
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('diary_detail',diary_id=diary_id))


@app.route('/diary_search/')
def diary_search():
    q = request.args.get('q')
    diarys = Diary.query.filter(or_(Diary.title.contains(q),Diary.content.contains(q)))
    return render_template('populardiary.html', diarys=diarys)

    # 与的查询
    # questions = Question.query.filter(Question.title.contains(q),Question.content.contains(q))


# @app.before_request
# def my_before_request():
#     if session.get('username'):
#         pass
#     else:
#         if  request.method == 'GET':
#             pass
#         else:
#             return redirect(url_for('login'))



@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
