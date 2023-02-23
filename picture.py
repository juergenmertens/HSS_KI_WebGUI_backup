import os

from flask import Blueprint, render_template, request, current_app, session
from werkzeug.utils import secure_filename

pictureki = Blueprint('pictureki', __name__)


@pictureki.get('/picture')
def picture_get():
    return render_template('picture.html')
@pictureki.post('/upload')
def upload():
    file = request.files['file']
    filename = ''
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        session['filename'] = filename
    return render_template('index.html', filename=filename)


@pictureki.post('/predict')
def predict():
    if 'filename' in session:
        print(session['filename'])

    session.pop('filename', None)

    return render_template('index.html')
