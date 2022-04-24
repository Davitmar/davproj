from app.countries.models import Country
from app.db import db


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    score = db.Column(db.Float(1), nullable=False)
