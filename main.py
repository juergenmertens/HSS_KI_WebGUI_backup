from flask import Blueprint, render_template
from __init__ import create_app

main = Blueprint('main', __name__)

fields = [['anz', 'Anzahl Beschädigungen'], ['tiefe', 'Durchschnittl. Tiefe in mm']]

@main.route('/')
def index_get():
    return render_template('index.html', inputfields = fields )

@main.route('/', methods=['Post'])
def index_post():
    return render_template('index.html', inputfields = fields)

if __name__ == '__main__':
    create_app().run(debug=True)

