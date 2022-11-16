from flask import Blueprint, render_template, request
from __init__ import create_app
from sklearn import tree
import joblib

main = Blueprint('main', __name__)

# TODO
# Eingabefelder eintragen [Feldname, Anzeigetext]
fields = [['anz', 'Anzahl Beschädigungen'], ['tiefe', 'Durchschnittl. Tiefe in mm']]

# TODO
# Name des Modells festlegen
model_file='qm_model.dt'

@main.route('/')
def index_get():
    return render_template('index.html', inputfields = fields )

@main.route('/', methods=['Post'])
def index_post():

    # TODO
    # Daten aus Form Request laden, evtl. konvertieren
    input_values = []
    for input in fields:
        if input[0] in request.form.keys():
            input_values.append( float( request.form.get(input[0])))
    # TODO
    # Model mit Daten aufrufen
    model = joblib.load(model_file)
    result = model.predict([input_values])

    # TODO
    # Ergebnis für Ausgabe vorbereiten
    # result = result ...
    if result == 'N':
        result = "Nacharbeit"
    else:
        result = "Ausschuss"

    return render_template('index.html', inputfields = fields, result = result)

if __name__ == '__main__':
    create_app().run(debug=True)

