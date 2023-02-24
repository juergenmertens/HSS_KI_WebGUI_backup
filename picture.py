import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from flask import Blueprint, render_template, request, current_app, session
from tensorflow import keras
from werkzeug.utils import secure_filename

from image_helper import load_image_as_grayscale, process_image

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
    filename = ''
    if 'filename' in session:
        filename = session['filename']
        result = prediction(filename)
        session.pop('filename', None)
    else:
        result = "No valid image!"

    return render_template('picture.html', image=filename, result=result)


def prediction(image_path):
    image = load_image_as_grayscale(image_path)

    # plt.imshow(image, cmap='Greys')
    # plt.show()

    image = process_image(image)
    image.save(image_path)

    model = keras.models.load_model('ziffern.model')
    image_size = 28 * 28
    img = np.asarray(image).astype('float32')
    img = (255 - img)
    img = img / np.amax(img)
    img = img.reshape((1, image_size))
    result = model.predict(img)

    result_str=''
    for i in range(10):
        result_str += ("{0}: {1:5.2f} %\n".format(i, result[0][i] * 100))

    return result_str
