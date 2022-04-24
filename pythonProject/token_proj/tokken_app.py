from flask import Flask, request, jsonify
from token_hash import hash_pass
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
#app.secret_key = b'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/token'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'User: ' + str(self.id)

class Books(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    name = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#db.create_all()
key='jdjdvlkdklx'

def id_token(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'token' in request.headers:
            encoded_token=request.headers['token']
            try:

                decoded_token=jwt.decode(encoded_token, key, algorithms="HS256")

                u_id=decoded_token['id']

            except:
                return jsonify('invalid token'), 401
        else:
            return jsonify('a valid token is missing'), 401
        return f(u_id, *args, **kwargs)
    return inner





@app.route('/signup/', methods=['Post'])
def signup():
    errors={}

    data = request.json
    if not data['username'] or not data['password']:
        errors['invalid']='username / password empty'
    if User.query.filter_by(username=data['username']).first():
        errors['invalid']='username already exists'
    if len(errors)>0:
        return jsonify(errors), 401
    user=User(username=data['username'], password=hash_pass(str(data['password'])))
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return jsonify({'sucsesfully signup':user.id}), 201

@app.route('/login/', methods=['Post'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    errors = {}
    if not username or not password:
        errors['invalid'] = 'username / password empty'
    if len(errors):
        return jsonify(errors), 401
    user = User.query.filter_by(username=username).first()
    if user.password != hash_pass(str(password)):
        return jsonify('invalid username or password'), 400

    token = jwt.encode({'id': user.id, 'username': username, 'password': hash_pass(str(password))}, key,
                       algorithm="HS256")
    return jsonify({'token':token}), 200

@app.route('/addbook/', methods=['Post'])
@id_token
def add_book(u_id):
    #errors={}

    data = request.json
    author=data['author']
    name=data['name']

    if not author or not name:
        return jsonify('no book')
    book=Books.query.filter_by(user_id=u_id, name=name).first()

    if book:
        return jsonify('book already exists'), 400

    # if len(errors)>0:
    #     return jsonify(errors), 401
    book=Books(author=author, name=name, user_id=u_id)
    db.session.add(book)
    db.session.commit()
    #db.session.refresh(user)
    return jsonify('book sucsesfully added'), 201


if __name__=='__main__':
    app.run(debug=True)


#inchi json() ev json tarber request ev responsum???
#len(erroers)????? 0 1