from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import validators, ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField("Email", validators=[Required(), Length(1, 20), Email()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField("Keep me log in")
    submit = SubmitField("Login")


class RegisterForm(Form):
    email = StringField("Email", validators=[Required(), Length(1, 20), Email()])
    username = StringField("username", validators=[Required(), Length(1, 64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0, 'Username must only have letters, numbers, dots or underscores')])
    password = PasswordField("password", validators=[Required(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Commit password", validators=[Required()])
    Submit = SubmitField("Register")

    def validate_email(self, field):
        if (User.query.filter_by(email=field.data).first()):
            raise ValidationError("Email already been registered")

    def validate_username(self, field):
        if (User.query.filter_by(username=field.data).first()):
            raise ValidationError("username already in use")

