from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList, ValidationError
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MyScret!'
# app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True


class YearForm(Form):
    year = StringField('year')
    total = StringField('total')


class PhoneForm(Form):
    country_code = IntegerField('country code')
    area_code = IntegerField('area code')
    number = StringField('number')


class LoginForm(FlaskForm):
    # specify the fiels in the form:
    username = StringField('username', validators=[
                           InputRequired('A username is required!'), Length(min=4, max=8, message='Mut be between 4 and 8 characters')])
    password = PasswordField('password', validators=[
                             InputRequired(), AnyOf(values=['secret', 'password'])])
    age = IntegerField('age', default=24)
    true = BooleanField('Click here')
    email = StringField('email', validators=[Email()])
    home_phone = FormField(PhoneForm)
    mobile_phone = FormField(PhoneForm)
    years = FieldList(FormField(YearForm))

    # def validate_username(form, field):
    #     if field.data != 'Hanan':
    #         raise ValidationError('You do not have the right username')


class NameForm(LoginForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email


@app.route('/', methods=['GET', 'POST'])  # Where I will display this form
def index():
    myuser = User('Hanan', 22, 'hanan@gmail.com')  # prepopulation

    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2005, 1989)
    g2 = group(2000, 1876)
    g3 = group(2001, 5000)
    years = {'years': [g1, g2, g3]}  # field list

    # instantiate the form:
    form = NameForm(obj=myuser, data=years)

    ######## To Delete a Field ############
    del form.mobile_phone

    # when a POST request is sent to the same route of form data -->
    # the form data is combined with the html and the validation stuff
    # So, to validate the request data:
    if form.validate_on_submit():
        yearsOutput = '<h2>'
        for y in form.years:
            yearsOutput += f'year= {y.year.data} total= {y.total.data} <br>'
        yearsOutput += '</h2>'
        return f'<h1>username: {form.username.data} password: {form.password.data} age: {form.age.data}\
            true: {form.true.data} email: {form.email.data}</h1> \
            <h1>Home Phone Information </h1> \
            <h2>Country code: {form.home_phone.country_code.data}, Area Code: {form.home_phone.area_code.data} \
            Number: {form.home_phone.number.data}\
                <h1>Years:</h1> {yearsOutput}'
    return render_template('index.html', form=form)


@app.route('/dynamic', methods=['POST', 'GET'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    names = ['middle_name', 'last_name', 'nickname']

    for name in names:
        setattr(DynamicForm, name, StringField(name))

    DynamicForm.name = StringField('name')

    form = DynamicForm()

    if form.validate_on_submit():
        return f'<h1>Name: {form.name.data}</h1>'

    return render_template('dynamic.html', form=form, names=names)


if __name__ == "__main__":
    app.run(debug=True)
