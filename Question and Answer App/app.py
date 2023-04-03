from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# This is a common user function. I need it in every route to check either the user has
# a session and so, I can get all the user info from DB to use it in each route


def get_current_user():
    user_result = None
    db = get_db()
    if 'user' in session:
        user = session['user']
        user_cur = db.execute(
            'select id, name, password, expert, admin from users where name=?', [user])
        user_result = user_cur.fetchone()
    return user_result


@app.route('/')
def index():
    user_info = get_current_user()
    db = get_db()
    questions_cur = db.execute(
        ''' select 
                questions.id as question_id, 
                questions.question_text, 
                askers.name as asker_name, 
                experts.name as expert_name 
            from questions 
            join users as askers on questions.asked_by_id = askers.id 
            join users as experts on experts.id = questions.expert_id 
            where questions.answer_text is not null''')
    questions_results = questions_cur.fetchall()
    return render_template('home.html', user=user_info, questions=questions_results)


@app.route('/register', methods=['POST', 'GET'])
def register():
    user_info = get_current_user()
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        existing_user_cur = db.execute(
            'select id from users where name=?', [name])
        existing_user = existing_user_cur.fetchone()

        if existing_user:
            return render_template('register.html', user=user_info, error='user already exist')
        hashedPassword = generate_password_hash(
            request.form['password'], method='sha256')
        db.execute('insert into users (name, password, expert, admin) values(?,?,?,?)', [
                   name, hashedPassword, '0', '0'])
        db.commit()
        session['user'] = request.form['name']
        return redirect(url_for('index'))
    return render_template('register.html', user=user_info)


@app.route('/login', methods=['POST', 'GET'])
def login():
    user_info = get_current_user()
    db = get_db()
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user_cur = db.execute(
            'select id, name, password from users where name=?', [name])
        user_result = user_cur.fetchone()

        if user_result:
            if check_password_hash(user_result['password'], password):
                session['user'] = user_result['name']
                return redirect(url_for('index'))
            else:
                error = 'The password is incorrect!'
        else:
            error = 'The username is incorrect!'

    return render_template('login.html', user=user_info, error=error)


@app.route('/question/<question_id>')
def question(question_id):
    user_info = get_current_user()
    db = get_db()
    question_cur = db.execute(
        ''' select 
                questions.question_text, 
                questions.answer_text, 
                asker.name as asker_name, 
                expert.name as expert_name 
            from questions 
            join users as asker on questions.asked_by_id= asker.id 
            join users as expert on questions.expert_id= expert.id 
            where questions.id=?''', [question_id])
    question_result = question_cur.fetchone()

    return render_template('question.html', user=user_info, question=question_result)


@app.route('/answer/<question_id>', methods=['POST', 'GET'])
def answer(question_id):
    user_info = get_current_user()
    if not user_info:
        return redirect(url_for('login'))

    if user_info['expert'] == 0:
        return redirect(url_for('index'))

    db = get_db()
    if request.method == 'POST':
        db.execute('update questions set answer_text = ? where id = ? ', [
            request.form['answer'], question_id])
        db.commit()
        return redirect(url_for('unanswered'))

    question_cur = db.execute(
        'select id, question_text from questions where id= ?', [question_id])
    question_result = question_cur.fetchone()
    return render_template('answer.html', user=user_info, question=question_result)


@app.route('/ask', methods=['POST', 'GET'])
def ask():
    user_info = get_current_user()
    if not user_info:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        question = request.form['question']
        expert_id = request.form['expert']
        db.execute(
            'insert into questions (question_text, asked_by_id, expert_id) values(?,?,?)',
            [question, user_info['id'], expert_id])
        db.commit()
        return redirect(url_for('index'))

    expert_users_cur = db.execute('select id, name from users where expert=1')
    expert_users_result = expert_users_cur.fetchall()
    return render_template('ask.html', user=user_info, expert_users=expert_users_result)


@app.route('/unanswered')
def unanswered():
    user_info = get_current_user()
    if not user_info:
        return redirect(url_for('login'))

    if user_info['expert'] == 0:
        return redirect(url_for('index'))

    db = get_db()
    questions_cur = db.execute(
        ''' select 
                questions.id, 
                questions.question_text, 
                users.name 
            from questions 
            join users on questions.asked_by_id = users.id 
            where questions.answer_text is null and questions.expert_id =?''', [user_info['id']])
    questions_results = questions_cur.fetchall()
    return render_template('unanswered.html', user=user_info, questions=questions_results)


@app.route('/users')
def users():
    user_info = get_current_user()
    if not user_info:
        return redirect(url_for('login'))

    if user_info['admin'] == 0:
        return redirect(url_for('index'))

    db = get_db()
    users_cur = db.execute('select id,name,admin,expert from users')
    users_result = users_cur.fetchall()
    return render_template('users.html', user=user_info, users=users_result)


@app.route('/promote/<user_id>')
def promote(user_id):
    user_info = get_current_user()
    if not user_info:
        return redirect(url_for('login'))

    if user_info['admin'] == 0:
        return redirect(url_for('index'))

    db = get_db()
    db.execute('update users set expert=1 where id=?', [user_id])
    db.commit()
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
