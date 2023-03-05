from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'xcde234'
    app.config['UPLOAD_FOLDER'] = 'static/upload'

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from text import textki as textki_blueprint
    app.register_blueprint(textki_blueprint)

    from image import imageki as imageki_blueprint
    app.register_blueprint(imageki_blueprint)

    return app
