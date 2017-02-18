from . import admin
from silverdynasty import login_manager
from silverdynasty.models import User
from silverdynasty.admin.forms import UserForm
from flask import flash, render_template, url_for, redirect, request
from flask_login import logout_user, login_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@admin.route('/', methods=['GET', 'POST'])
@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Sikeres bejelentkezés!', category='info')
            return redirect(request.args.get('next') or url_for('cat.list_cats'))
        flash('Hibás email vagy jelszó!  ')
    return render_template('/admin/login.html', form=form)


@admin.route('/logout')
def logout():
    logout_user()
    flash("Sikeres kijelentkezés!", category='info')
    return redirect(url_for('.login'))
