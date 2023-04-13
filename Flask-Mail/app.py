from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'hanan.tartousi12@gmail.com'
app.config['MAIL_PASSWORD'] = 'fyhvrwklgtxajtmd'
app.config['MAIL_DEFAULT_SENDER'] = 'hanan.tartousi12@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# mail = Mail()
# mail.init_app(app)


@app.route('/')
def index():
    msg = Message('Hey There', recipients=['hanan.tartousi12@gmail.com'])
    # msg.add_recipients('')
    msg.html = '<b>This is a test email sent</b>'
    # msg.body = '<b>This is a test email sent</b>'
    with app.open_resource('image.jpg') as image:
        msg.attach('image.jpg', 'image/jpeg', image.read())
    with app.open_resource('example.zip') as ex:
        msg.attach('example.zip', 'application/zip', ex.read())
    mail.send(msg)

    # other parameter:
    # msg = Message(
    #     subject='',
    #     recipients=[],
    #     body='',
    #     html='',
    #     sender='',
    #     cc=[],
    #     bcc=[],
    #     attachments=[],
    #     reply_to=[],
    #     date='date',
    #     charset='',
    #     extra_headers={'': ''},
    #     mail_options=[],
    #     rcpt_options=[]
    # )

    return 'Message has been sent!'


# @app('/bulk')
# def bulk():
#     users = [{'name': 'Hanan', 'email': 'hanan.tartousi12@gmail.com'}]
#     with mail.connect() as conn:
#         for user in users:
#             msg = Message('Bulk!', recipients=[user['email']])
#             msg.body = 'Hey'
#             conn.send(msg)
#     return 'Message has been sent!'


if __name__ == '__main__':
    app.run()
