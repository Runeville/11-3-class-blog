from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import check_password_hash


class AddPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Create post")


class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Update post")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Change username")


class UpdatePasswordForm(FlaskForm):

    password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=8)])
    new_password_confirm = PasswordField("Confirm password",
                                         validators=[DataRequired(), EqualTo("new_password", "Password must match")])
    submit = SubmitField("Change password")


