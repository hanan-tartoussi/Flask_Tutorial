import os
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
file_path = 'C:/Users/HP/Desktop/Internship/Flask Tutorial/Flask-admin/admin_db.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)


class Comment(db.Model):
    # column_display_pk = True  # optional, but I like to see the IDs in the list
    # column_hide_backrefs = False
    # column_list = ('id', 'comment_text', 'user_id')

    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    form_columns = ['id', 'comment_text', 'user_id']

    def get_user(view, context, model, name):
        return model.user.username

    column_list = ('id', 'comment_text', 'user_id')
    column_labels = dict(user='User Name')
    column_formatters = dict(user=get_user)

    # user = db.relationship(
    #     'User', backref=db.backref('commenty', lazy='dynamic'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

if __name__ == '__main__':
    app.run(debug=True)
