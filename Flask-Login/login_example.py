from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
file_path = os.path.abspath(os.getcwd())+"\login.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

serializer = URLSafeTimedSerializer(app.secret_key)


class User1(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

# unicode: built-in Python function that returns a string object that contains the unicode representation of the given object.
    def get_id(self):
        return str(self.session_token)


@login_manager.user_loader
def load_user(session_token):
    user = User1.query.filter_by(session_token=session_token).first()
    # first check if the session_token is valid
    # after 10 sec will raise an error : SignatureExpired
    try:
        serializer.loads(session_token, max_age=10)
    except SignatureExpired:
        user.session_token = None
        db.session.commit()
        return None

    return user


def createUser():
    user = User1(username='Hanan', password='password1',
                 session_token=serializer.dumps(['Hanan', 'password1']))  # generates a token of bytes type that includes both the username and password
    db.session.add(user)
    db.session.commit()


def update_token():
    user = User1.query.filter_by(username='Hanan').first()
    user.password = 'password2'
    user.session_token = serializer.dumps(['Hanan', 'password2'])
    db.session.commit()


@app.route('/')
def index():
    user = User1.query.filter_by(username='Hanan').first()
    user.session_token = serializer.dumps(['Hanan', 'password1'])
    db.session.commit()
    login_user(user, remember=True)
    return '<h1>You are now logged in!</h1>'


@app.route('/home')
@login_required
def home():
    return f'<h1>{current_user.username}, you are in the home page!</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>You are now logged out!</h1>'


if __name__ == "__main__":
    app.run(debug=True)
