from flask import Flask, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = '/pictures'

configure_uploads(app, photos)


@app.route('/uploads', methods=['POST', 'GET'])
def upload():
    return render_template('upload.html')


if __name__ == "__main__":
    app.run()
