from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, EqualTo


class AddPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10)])
    image = FileField("Images")
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


