from flask import redirect
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import current_user


class RegisterForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign in")


def redirect_unauthorized(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_active is False:
            return redirect('/login')
        else:
            return function(*args, **kwargs)

    return wrapper


def redirect_with_status(argument):
    def decorator(function):
        @wraps(function)
        def wrapper():
            if current_user.status < argument:
                return redirect('/')
            else:
                return function()

        return wrapper
    return decorator
