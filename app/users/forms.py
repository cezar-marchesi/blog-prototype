from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.utils.custom_validators import UsernameExists, EmailExists, EmailDoesNotExist



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(
                                                       min=3, max=30, message='Must be between 3 and 30 characteres'),
                                                   UsernameExists()
                                                   ])
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             EmailExists()
                                             ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email()
                                             ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(
                                                       min=3, max=30, message='Must be between 3 and 30 characteres'),
                                                   UsernameExists()
                                                   ])
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             EmailExists()
                                             ])    
    image_file = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             EmailDoesNotExist()
                                             ])    

    submit = SubmitField('Request password reset')
                                            
class RequestPasswordForm(FlaskForm)                                            :
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])

    submit = SubmitField('Reset')