from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from . import db, login_manager
from datetime import datetime
import hashlib
import os


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICALES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINSTER = 0x80


class Role(db.Model):
    __tablename__ = "roles"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role')
    default = db.Column(db.Boolean, default=False, index=True)
    # 设置角色,只有admin才是True
    permissions = db.Column(db.Integer)
    # 设置角色权利,采用二进制表示,
    # 关注用户    "0b0x01"
    # 在他人的文章中发表评论    "0b0x02"
    # 写文章    "0b0x04"
    # 管理他人的评论    "0b0x08"
    # 管理员权限    "0b0x80"
    users = db.relationship("User", backref="role", lazy='dynamic')

    def __repr__(self):
        return ("<role %r>" % (self.name))

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS | Permission.MODERATE_COMMENTS,False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.ID"))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(20), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 继承基类的构造方法
        if self.role is None:
            # Role的relationship那里
            if self.email == os.environ.get("flask_admin"):
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avater_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

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
        db.session.commit()
        return True

    def can(self, permissions):
        return (self.role is not None and (self.role.permissions & permissions) == permissions)

    def is_admin(self):
        return self.can(Permission.ADMINSTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def change_email(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False
        if(data.get("confirm") != self.ID):
            return False
        self.email = data.get("newemail")
        self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()
        try:
            db.session.add()
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True

    def gravator(self, size=100, default="identicon", rating="g"):
        if request.is_secure:
            url = "https://secure.gravatar.com/avatar"
        else:
            url = "http://www.gravatar.com/avatar"
        hash = self.avatar_hash or hashlib.md5(self.email.encode("utf-8")).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(ID):
    user = User.query.get(int(ID))
    return user
    """
    Login要求实现回调函数,必须返回用户对象或者None
    """
