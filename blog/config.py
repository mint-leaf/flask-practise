import os
import pymysql


class Config():
    SECRET_KEY = os.environ.get("security_key") or "hard to guess string"
    Flask_Mail_Subject_prefix = '[Mint]'
    Flask_Mail_From = 'Mint Admin <925034647@qq.com>'
    Flask_Admin = os.environ.get("flask_admin")

    @staticmethod
    def init_app(app):
        pass


class Developmentconfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("mailname")
    MAIL_PASSWORD = os.environ.get("mailpwd")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mint:aptx@localhost/dev"


class Testconfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mint:aptx@localhost/datatest"


class Productionconfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mint:aptx@localhost/production"


config = {
    'development': Developmentconfig,
    'testing': Testconfig,
    'Production': Productionconfig,
    'default': Developmentconfig,
}
