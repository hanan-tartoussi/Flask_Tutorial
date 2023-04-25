from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join


app = Flask(__name__)
file_path = 'C:/Users/HP/Desktop/Internship/Flask Tutorial/Flask-admin/admin_db.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4')


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
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship(
    #     'User', backref=db.backref('comment', lazy='dynamic'))

    def __repr__(self):
        return '<Comment %r>' % (self.id)


class UserView(ModelView):
    column_exclude_list = []
    column_display_pk = False
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True

    # def on_model_change(self, form, model, is_create):
    #     model.password = 'test'


class CommentView(ModelView):
    create_modal = False
    form_columns = ['comment_text', 'user_id']
#     # column_display_pk = True  # optional, but I like to see the IDs in the list
    # column_hide_backrefs = False
    # column_list = [c_attr.key for c_attr in inspect(
    #     Comment).mapper.column_attrs]
    # column_list = ('comment_text', 'user_id')
    # form_widget_args = {
    #     'user_id': {
    #         'widget': Select2Widget(),
    #         'placeholder': 'Select user ID'
    #     }
    # }


admin.add_view(UserView(User, db.session))
admin.add_view(CommentView(Comment, db.session))

path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))


if __name__ == '__main__':
    app.run(debug=True)
