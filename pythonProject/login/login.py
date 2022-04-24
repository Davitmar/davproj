from flask import Flask
from flask import session, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from pass_code import coding

app = Flask(__name__)
app.secret_key = b'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/test_post'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path + '/users_db.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    psw = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return 'user ' + f'{self.id}'


class Note2(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(60), nullable=True)
    us_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return 'note ' + f'{self.id}'


#db.create_all()


def login_t(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return redirect(url_for('profile'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
@login_t
def home():
    # if not session.get('user'):
    #     return redirect('login')
    return redirect('profile')


@app.route('/login', methods=['GET', 'POST'])
@login_t
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
            # print(user)
            if user is None:
                errors['form_error'] = 'Invalid credentials.'

            if user is not None:
                if user.psw != coding(password):
                    errors['form_error'] = 'Invalid credentials.'

        if len(errors):
            return render_template('login.html', errors=errors, form_data=form_data), 400

        session['user'] = {'id': user.id, 'username': user.username}

        return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    current_user = session.get('user')
    img=None
    if not current_user:
        return redirect(url_for('login'))
    if Note2.query.filter_by(us_id=current_user['id']).first():
        img='..\media\\'+Note2.query.filter_by(us_id=current_user['id']).first().file
    #return f'{img}'
    return render_template('profile.html', current_user=current_user, img=img)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    s_form_data = {}
    errors = {}

    if request.method == 'GET':
        return render_template('signup.html', s_form_data=s_form_data, errors=errors)

    if request.method == 'POST':
        s_form_data = request.form
        s_username = s_form_data.get('s_username')
        s_password = s_form_data.get('s_password')
        conf_pass = s_form_data.get('conf_pass')
        if not s_username:
            errors['s_username'] = 'Username is required.'

        if not s_password:
            errors['s_password'] = 'Password is required.'

        if s_password and len(s_password) < 3:
            errors['pass_length'] = 'weak password.'

        if not conf_pass:
            errors['conf_pass'] = 'Confirm password is required.'

        if conf_pass and s_password != conf_pass and s_password:
            errors['different_pass'] = 'different passwords'

        if len(errors) == 0:
            user = User.query.filter_by(username=s_username).first()
            if user is None:
                user = User(username=s_username, psw=coding(s_password))
                db.session.add(user)
                db.session.commit()



            else:
                errors['exist'] = f'username {s_username} already exists'

        if len(errors):
            return render_template('signup.html', errors=errors, s_form_data=s_form_data), 400

        return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form_data = {}
    errors = {}

    if request.method == 'GET':
        return render_template('add.html', form_data=form_data, errors=errors)

    if request.method == 'POST':
        form_data = request.form
        title = form_data.get('title')
        desc = form_data.get('desc')
        user_id = session.get('user')
        file = request.files.get('file')
        if not title:
            errors['title'] = 'title is required.'

        # if not file:
        #     errors['no_file'] = 'There is not choosen file'

        if len(errors) == 0:
            note = Note2.query.filter_by(title=title).first()
            if note is None:
                if file:
                    file_path = app.root_path + '\media' + '\\' + file.filename
                    file.save(file_path)
                note = Note2(title=title, desc=desc, us_id=user_id['id'], file=file.filename)
                #return f'{form_data.get("title")}#, {title}#, {desc}#, {user_id["id"]}#, {file.filename} '
                db.session.add(note)
                db.session.commit()
                return redirect(url_for('profile'))
            else:
                errors['exist'] = 'title already exists'

        if len(errors):
            return render_template('add.html', errors=errors, form_data=form_data), 400




if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()

# skzbum graca exel redirect(url_for('profile'), isk decoratorum redirect 'profile' ??????????
# create chexav anel consolic
# secret keyn incha anum?
# urish db i vraya gnum u asum file not database
# postgresql in chexav kpnel
# class atributnery vonc enq talis instancic
