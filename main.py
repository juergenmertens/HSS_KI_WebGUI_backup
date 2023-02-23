from flask import Blueprint, render_template

from __init__ import create_app

main = Blueprint('main', __name__)


@main.route('/')
def index_get():
    return render_template('index.html')


if __name__ == '__main__':
    create_app().run(debug=True, host="0.0.0.0")
