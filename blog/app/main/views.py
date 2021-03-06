from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdmin
from .. import db
from ..models import User
from ..dec import is_admin


@main.route('/', methods=['GET', 'POST'])
def index():
    return(render_template('index.html'))


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None: 
        abort(404)
    return render_template("user.html", user=user)


@main.route("/edit-profile", methods=['GET', 'POST'])
@login_required
def editor_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(403, "message error")
        flash("your profile has been update")
        return redirect(url_for("main.user", username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("editor_profile.html", form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@is_admin
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdmin(user=user)
    if form.validate_on_submit():
        user.emial = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        try:
            db.session.add(user)
        except Exception as e:
            db.session.rollback()
            abort(403, "information error")
        flash("the profile has been updated")
        return redirect(url_for("main.user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.role.data = user.role_id
    return render_template("edit_profile.html", form=form, user=user)
