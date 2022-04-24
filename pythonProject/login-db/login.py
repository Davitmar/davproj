from flask import Flask, session, request, render_template, url_for, redirect, send_from_directory
from functools import wraps
from password import hash_password
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'abc'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path + '/users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost/test_users'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path + '/users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'User: ' + str(self.id)


class Note(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.Text, nullable=True)


@app.context_processor
def inject_user():
    current_user = session.get('user')
    return dict(current_user=current_user)


def require_anonymous(function):
    @wraps(function)
    def inner(*args, **kwargs):
        if session.get('user'):
            return redirect('profile')
        return function(*args, **kwargs)

    return inner


def require_login(function):
    @wraps(function)
    def inner(*args, **kwargs):
        if not session.get('user'):
            return redirect('login')
        return function(*args, **kwargs)

    return inner


@app.route('/')
@require_login
def home():
    return redirect(url_for('profile'))


@app.route('/add-note', methods=['GET', 'POST'])
@require_login
def add_note():
    file_path = None
    form_data = {}
    errors = {}

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            errors['title'] = 'Title is required'

        if len(errors):
            return render_template('note.html', form_data=form_data, errors=errors)

        note_file = request.files.get('note_file')
        if note_file:
            file_path = app.root_path + '/media/' + note_file.filename
            note_file.save(file_path)

        user = session.get('user')
        note = Note(title=title, description=description, file=note_file.filename, user_id=user['id'])
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('note.html', form_data=form_data, errors=errors)


@app.route('/download/<note_id>')
@require_login
def download(note_id):
    user_id = session.get('user')['id']
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note is None:
        return redirect(url_for('profile'))
    return send_from_directory(app.root_path + '/media/', note.file)


@app.route('/login', methods=['GET', 'POST'])
@require_anonymous
def login():
    form_data = {}
    errors = {}

    if request.method == 'GET':
        return render_template('login.html', form_data=form_data, errors=errors)

    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        password = form_data.get('password')

        if not username:
            errors['username'] = 'Username is required.'

        if not password:
            errors['password'] = 'Password is required.'

        if len(errors) == 0:
            user = User.query.filter_by(username=username).first()

            if user is None:
                errors['form_error'] = 'Invalid credentials.'

            if user is not None:
                if hash_password(password) != user.password:
                    errors['form_error'] = 'Invalid credentials.'

        if len(errors):
            return render_template('login.html', errors=errors, form_data=form_data), 400

        session['user'] = {'id': user.id, 'username': user.username}

        return redirect(url_for('profile'))


@app.route('/profile')
@require_login
def profile():
    notes = Note.query.filter_by(user_id=session.get('user')['id'])
    return render_template('profile.html', notes=notes)


@app.route('/logout')
@require_login
def logout():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
@require_anonymous
def signup():
    form_data = {}
    errors = {}

    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username')
        password = form_data.get('password')
        confirm_password = form_data.get('confirm_password')

        if not username:
            errors['username'] = 'Username is required!'

        if not password:
            errors['password'] = 'Password is required!'

        if not confirm_password:
            errors['confirm_password'] = 'Confirm password is required!'

        if password and password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match!'

        if password and len(password) < 6:
            errors['password'] = 'Passwords length must be greater than 6 '

        if len(errors) == 0:
            user = User.query.filter_by(username=username).first()

            if user:
                errors['username'] = 'Username is already exists'
            else:
                user = User(username=username, password=hash_password(password))
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))

    return render_template('signup.html', form_data=form_data, errors=errors)
