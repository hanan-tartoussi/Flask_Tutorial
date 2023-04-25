from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restless import APIManager


app = Flask(__name__)
app.app_context().push()
file_path = 'C:/Users/HP/Desktop/Internship/Flask Tutorial/Flask-restless/api.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET', 'POST'])
manager.create_api(
    Item, methods=['GET', 'POST', 'DELETE', 'PUT'], allow_delete_many=True, allow_patch_many=True)

if __name__ == '__main__':
    app.run(debug=True)
