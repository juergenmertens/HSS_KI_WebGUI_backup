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
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        session['filename'] = filename
    return render_template('picture.html', image=filename)


@pictureki.post('/predict')
def predict():
    if 'filename' in session:
        filename = session['filename']
        session.pop('filename', None)

    result = predict(filename)

    return render_template('picture.html', result=result)

def predict(filename):
    pass