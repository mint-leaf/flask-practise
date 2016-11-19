from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from .forms import LoginForm, RegisterForm
from ..models import User
from ..email import sendmail
import time


@auth.route('/login', methods=['GET', 'POST'])
def login():
    Form = LoginForm()
    if (Form.validate_on_submit()):
        user = User.query.filter_by(email=Form.email.data).first()
        if(user is not None and user.verify_password(Form.password.data)):
            login_user(user, Form.remember_me.data)
            return redirect(request.args.get('next') or url_for("main.index"))
        else:
            flash('Invalid username or password')
    return render_template("auth/Login.html", form=Form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("main.index"))


@auth.route('/register', methods=['GET', 'POST'])
def Register():
    Registerform = RegisterForm()
    if (Registerform.validate_on_submit()):
        user = User(email=Registerform.email.data, username=Registerform.username.data, password=Registerform.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        sendmail(user.email, "Confirm your account", "auth/")
        flash("a confirmation email has been sent to you")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=Registerform)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if (current_user.confirmed):
        return redirect(url_for("main.index"))
    if (current_user.confirm(token)):
        flash("you have confirmed successfully, thanks")
    else:
        flash("the confirmation link is invalid or has expired")
    time.sleep(3)
    return redirect(url_for("main.index"))