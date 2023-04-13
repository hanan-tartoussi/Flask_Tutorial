import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:234Hanan109@localhost/migrate_db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    subscribed = db.Column(db.Boolean)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)


if __name__ == '__main__':
    app.run(debug=True)
