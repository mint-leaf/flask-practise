from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import validators, ValidationError
from ..models import Role


class NameForm(Form):
    name = StringField(" what is your name? ", validators=[Required()])
    submit = SubmitField("submit")


class EditProfileForm(Form):
    name = StringField("Real Name", validators=[Length(0, 64)])
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")


class EditProfileAdmin(Form):
    email = StringField("Email", validators=[Required(), Length(1, 64), Email()])
    username = StringField("Username", validators=[Required(), Length(1, 64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0, 'username must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField("Confirmed")
    role = SelectField("Role", coerce=int)
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About me")
    submit = SubmitField("submit")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdmin, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError("email has already been registered")

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError("Username has already been used")

