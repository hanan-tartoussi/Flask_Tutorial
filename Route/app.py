from flask import Flask, jsonify, request, redirect, url_for, session

# __name__ this is a reference to the name of the current module that I worked in (which is app.py)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecret'
######### Routing#################


# This is the decorator app.route to specify which route you want to write code for
# in the route: specify the location that you want to use for your route
# this is a placeholder --> we need to pass it as parameter to the function below
@app.route('/', defaults={'name': 'Default'})
@app.route('/<name>')
def index(name):
    session['name'] = name
    return f'<h1>Hello {name}!</h1>'


@app.route('/home')
def home():
    return f'<h1>Welcome Home!</h1>'

# if we want to return something else like json:
# First we need to import the jsonify function: from flask import Flask, jsonify


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession'
    # a dict maps to an object in json and a list maps to an array in json
    return jsonify({'key': 'value', 'listKey': [0, 1, 2, 3], 'name': name})

# Note: by default the only methods allowed is GET, and if we want to allow different method so,
# we need to use the methods parammeter and pass a list of the accepted methods for that particular route.


@app.route('/about', methods=['GET', 'POST'])
def about():
    return '<h1> About Page</h1>'

### Query String####


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hello {name}. You are from {location}. You are in the query page</h1>'


# Request Form Data##
# method 1:
@app.route('/theform')
def theform():
    return '''<form action="/process" method="POST">
                    <input type="text" name="name" placeholder="Enter ur name">
                    <input type="text" name="location" placeholder="Enter ur location">
                    <input type="submit" value="Submit"/>
                </form>'''


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return f'<h1>Hello {name}. You are from {location}. You have submitted the form successfuly</h1>'

# method 2:


@app.route('/theform2', methods=['GET', 'POST'])
def theform2():
    if request.method == 'GET':
        return '''<form action="/theform2" method="POST">
                        <input type="text" name="name" placeholder="Enter ur name">
                        <input type="text" name="location" placeholder="Enter ur location">
                        <input type="submit" value="Submit"/>
                </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return f'<h1>Hello {name}. You are from {location}. You have submitted the form successfuly</h1>'

############## request json data#


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomList = data['randomList']
    return jsonify({'result': 'success', 'name': name, 'location': location, 'randomList': randomList[1]})

######## REDIRECT AND URL_FOR###########


@app.route('/theredirect', methods=['GET', 'POST'])
def theredirect():
    if request.method == 'GET':
        return '''<form action="/theredirect" method="POST">
                        <input type="text" name="name" placeholder="Enter ur name">
                        <input type="text" name="location" placeholder="Enter ur location">
                        <input type="submit" value="Submit"/>
                </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('index', name=name, location=location))


if __name__ == "__main__":
    app.run()
