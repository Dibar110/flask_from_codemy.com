from flask import Flask, render_template, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/people'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/people'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('Password is not readable!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    email = StringField("What's your email?", validators=[DataRequired()])
    password_hash = PasswordField("What's your password?", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    skills = ['Flask', 'Django', 'JavaScript']
    return render_template('index.html', skills=skills)

@app.route('/add/user', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash('User added successfully!')
    all_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, all_users=all_users)

@app.route('/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500

@app.route('/name', methods=['GET', 'POST'])
def get_name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('You logged successfully!')
    return render_template('name_form.html', name=name, form=form)

#Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
        except:
            db.session.commit()
            flash('Error!')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
    
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        all_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, all_users=all_users)
    except:
        flash("Error to delete user.")
        return render_template('add_user.html', form=form, name=name, all_users=all_users)
    
@app.route('/test_password', methods=['GET', 'POST'])
def test_password():
    name = None
    email = None
    password = None
    user_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password_hash.data

        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''

        user_to_check = Users.query.filter_by(email=email).first()

        passed = check_password_hash(user_to_check.password_hash, password)
    return render_template('test_password.html', name=name, email=email, password=password, user_to_check=user_to_check, passed=passed, form=form)
