from flask import Flask, render_template, request, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import urljoin, urlparse
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
file_path = os.path.abspath(os.getcwd())+"\login.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
# app.config['USE_SESSION_FOR_NEXT'] = True
# app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)

login_manager = LoginManager(app)
# to redirect to login route when a non logged in user try to access other route
login_manager.login_view = 'login'
login_manager.login_message = 'You can\'t access that page. You need to login first.'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to log in again!'
db = SQLAlchemy(app)


def is_safe_url(target):  # helper function used in Flask applications to validate and ensure that the target URL of a user redirect is a safe and valid URL
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# UserMixin: flask-login will know which user belongs to the row in the database


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):  # connect the user id to an actual user in the database
    # return User.query.filter_by(id=int(user_id))
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return '<h1>user does not exist! </h1>'

        # remember will create a cookie that will persist even when the user close the browser
        login_user(user, remember=True)

        if 'next' in session:
            next = session['next']
            if is_safe_url(next) and next is not None:
                return redirect(next)

        return '<h1>You are now logged in!<h1>'

    session['next'] = request.args.get('next')
    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return f'<h1>You are in the protected area, {current_user.username} ! </h1>'


@app.route('/fresh')
@fresh_login_required
def fresh():
    return f'<h1>You have a fresh login </h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>Logout</h1>'


if __name__ == '__main__':
    app.run(debug=True)
