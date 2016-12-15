# from flask import Flask, render_template, session, url_for, redirect
# from flask_script import Manager
# from flask_bootstrap import Bootstrap
# import datetime
# from flask_moment import Moment
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_mail import Mail
# from flask_mail import Message
# from threading import Thread
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
# manager = Manager(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['MAIL_SERVER'] = 'smtp.163.com.'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USERNAME'] = '18351993266@163.com'
# app.config['MAIL_PASSWORD'] = 'jiangyu1111'
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flask]'
# app.config['FLASKY_MAIL_SENDER'] = '18351993266@163.com'
# app.config['FLASK_ADMIN'] = '18351993266@163.com'
# mail = Mail(app)
# db = SQLAlchemy(app)
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role')
#
#     def __repr__(self):
#         return "<Role %r>" % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return "User %r" % self.username
#
#
# class UserForm(FlaskForm):
#     name = StringField('What is your name', validators=[DataRequired()])
#     submit = SubmitField('submit')
#
#
# def send_async_email(app, msg):
#     app_ctx = app.app_context()
#     app_ctx.push()
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = UserForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['know'] = False
#             if app.config['FLASK_ADMIN']:
#                 print '1'
#                 send_email(app.config['FLASK_ADMIN'], 'New User', 'mail/new_user', user=user)
#                 print 'success send'
#         else:
#             session['know'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, current_time=datetime.datetime.utcnow(),
#                            know=session.get('know', False),
#                            name=session.get('name'))
#
#
# # @app.route('/<string:username>')
# # def user(username):
# #     return render_template('index.html', username=username, title='User', current_time=datetime.datetime.utcnow())
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def invalid_error(e):
#     return render_template('500.html'), 500
#
#
# if __name__ == '__main__':
#     manager.run()
