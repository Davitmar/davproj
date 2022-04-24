from flask import Flask
from app.db import db
from app.universities.views import bp as university_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(university_bp)
    # app.register_blueprint(universities_bp)
    return app