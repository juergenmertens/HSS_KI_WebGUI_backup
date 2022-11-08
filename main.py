from flask import Blueprint, render_template
from __init__ import create_app

main = Blueprint('main', __name__)

fields = ['Field 1', 'Field 2', 'Field 3', 'Field 4']

@main.route('/')
def index_get():
    return render_template('index.html')

@main.route('/', methods=['Post'])
def index_post():
    return render_template('index.html')

if __name__ == '__main__':
    create_app().run(debug=True)

