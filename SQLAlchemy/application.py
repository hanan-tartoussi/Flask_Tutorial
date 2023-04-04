from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)

    # create a virtual column in the other table (in this case : Order) (in sqlalchemy not in the database)
    # lazy: how the relationship query is generated
    orders = db.relationship('Order', backref='member', lazy='dynamic')
    courses = db.relationship(
        'Course', secondary='user_courses', backref='member', lazy='dynamic')

    def __repr__(self):
        return f'Member {self.username}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    # Order.member: get back the member_id that the order belongs to


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # has a virtual column of members (we can say that this is a virtual list because can have multiple member)


# I don't want to manipulate directly to this table, SQLAlchemy will take care of it
db.Table('user_courses',
         db.Column('member_id', db.Integer, db.ForeignKey('member.id')),
         db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
         )

if __name__ == '__main__':
    app.run()
