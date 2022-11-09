from flask import Blueprint, render_template
from __init__ import create_app
import joblib

main = Blueprint('main', __name__)

# TODO
# Eingabefelder eintragen
fields = ['Field 1', 'Field 2', 'Field 3', 'Field 4']
# TODO
# Name des Modells festlegen
model_file='model.dt'

@main.route('/')
def index_get():
    return render_template('index.html')

@main.route('/', methods=['Post'])
def index_post():

    # TODO
    # Model laden
    model = joblib.load(model_file)

    # TODO
    # Daten aus Form Request laden, evtl. konvertieren

    # TODO
    # Model mit Daten aufrufen
    model.predict()

    # TODO
    # Ergebnis für Ausgabe vorbereiten
    # result = ...

    return render_template('index.html', inputfields = fields, result = result)

if __name__ == '__main__':
    create_app().run(debug=True)

