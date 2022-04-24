from flask import Flask

from project.db import init_db


def create_app():
    app = Flask(__name__)
    app.secret_key = '*&^$%^680(*^&%^%ert78&()*(&*^%&^$%%&*^&('
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/univ'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from db import db
    db.init_app(app)

    app.cli.add_command(init_db)

    from routes import route_bp

    app.register_blueprint(route_bp)

    return app