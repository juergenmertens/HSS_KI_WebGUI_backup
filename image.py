import os

import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, render_template, request, current_app, session
from tensorflow import keras
from werkzeug.utils import secure_filename

from image_helper import load_image_as_grayscale, process_image

imageki = Blueprint('imageki', __name__)


@imageki.get('/picture')
def picture_get():
    return render_template('image.html')


@imageki.post('/upload')
def upload():
    file = request.files['file']
    filename = ''
    if file:
        filename = secure_filename(file.filename)
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        session['filename'] = filename
        return predict()
    else:
        render_template('image.html')


def predict():
    filename = ''
    if 'filename' in session:
        filename = session['filename']
        results = prediction(filename)
        session.pop('filename', None)
    else:
        result = "No valid image!"

    return render_template('image.html', image=filename, results=results)


def prediction(image_path):

    # Bild laden
    image = load_image_as_grayscale(image_path)

    # process_image() bearbeitet das Bild nach den MNIST Vorgaben
    # - Ein freier Rand im Bild wird entfernt
    # - Das Bild wird auf 20x20 skaliert
    # - Der Schwerpunkt der Pixel wird ermittelt
    # - Das Bild wird in ein 28x28 Bild eingefügt, so dass
    #   der Schwerpunkt in der Mitte liegt
    image = process_image(image)

    # Bild speichern, weitere Verwendung unklar
    image.save(image_path)

    # ToDo: Modell laden.
    # Funktion keras.models.load_model()

    # ToDo: Numpy array mit Image vorbereiten
    # siehe jupyter-notebook

    # ToDo: predict
    # siehe jupyter-notebook

    # ToDo: Resultate besser lesbar gestalten
    # Schleife über results und formatieren als
    # Prozentzahl mit je 2 Nachkommastellen

    # results sollte ein Array mit 10 Strings sein.
    # results wird auf der Seite dargestellt
    return results
