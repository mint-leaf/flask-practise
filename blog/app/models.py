from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db, login_manager


class Role(db.Model):
    __tablename__ = "roles"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return ("<role %r>" % (self.name))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.ID"))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(20), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

    def get_id(self):
            return str(self.ID)

    def __repr__(self):
        return ("<role %r>" % (self.username))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.ID})

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if(data.get("confirm") != self.ID):
            return False
        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(ID):
    user = User.query.get(int(ID))
    return user
    """
    Login要求实现回调函数,必须返回用户对象或者None
    """
