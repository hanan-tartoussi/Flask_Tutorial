from flask import Flask, jsonify, request, redirect, url_for, session, render_template, g
import sqlite3

# __name__ this is a reference to the name of the current module that I worked in (which is app.py)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecret'


def connect_db():
    sql = sqlite3.connect('C:/Users/HP/Documents/data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3'):
        g.sqlite_db.close()


@app.route('/viewresult')
def viewresult():
    db = get_db()
    cur = db.execute('SELECT * FROM users')
    results = cur.fetchall()
    return '<h1>The Id is: {}. The name is: {}. The location is: {}. </h1>'.format(results[1]['id'], results[1]['name'], results[1]['location'])


@app.route('/viewallresults')
def viewallresults():
    db = get_db()
    cur = db.execute('SELECT * FROM users')
    results = cur.fetchall()
    return render_template('view.html', results=results)

####### INSERT INTO THE DB #########


@app.route('/theform', methods=['GET', 'POST'])
def theform2():
    if request.method == 'GET':
        return '''<form action="/theform" method="POST">
                        <input type="text" name="name" placeholder="Enter ur name">
                        <input type="text" name="location" placeholder="Enter ur location">
                        <input type="submit" value="Submit"/>
                </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        db = get_db()
        db.execute('insert into users (name, location) values (?,?)', [
                   name, location])
        db.commit()
        return f'<h1>Hello {name}. You are from {location}. You have submitted the form successfuly</h1>'


if __name__ == "__main__":
    app.run()
