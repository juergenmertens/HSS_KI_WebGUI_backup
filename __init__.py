from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'xcde234'

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from text import textki as textki_blueprint
    app.register_blueprint(textki_blueprint)

    from picture import pictureki as pictureki_blueprint
    app.register_blueprint(pictureki_blueprint)

    return app
