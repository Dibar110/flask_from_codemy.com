from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, FileField
# from flask_wtf.file import FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author')
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    about_author = TextAreaField('About Author')
    profile_picture = FileField('Profile Picture')
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("What's your password?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')