from flask_mail import Message
from flask import current_app
from datetime import datetime
from . import mail
from config import Config
from threading import Thread
from flask import render_template


def aysn_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def sendmail(to, subject, template, **kwags):
    app = current_app._get_current_object()
    msg = Message(Config.Flask_Admin+subject, sender=Config.Flask_Mail_From, recipients=[to])
    msg.html = render_template(template, **kwags)
    t = Thread(target=aysn_send_mail, args=[app, msg])
    t.start()
    return t
