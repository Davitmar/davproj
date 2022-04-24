from db import db

class Hamalsaran(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    rank = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    score = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'{self.rank}, {self.name}, {self.country}, {self.score}'