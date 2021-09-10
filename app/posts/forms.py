from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.utils.custom_validators import UsernameExists, EmailExists, EmailDoesNotExist


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Your thoughts', validators=[DataRequired()])
    submit = SubmitField('Post')
