from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email
from wtforms import validators


class NameForm(Form):
    name = StringField(" what is your name? ", validators=[Required()])
    submit = SubmitField("submit")



