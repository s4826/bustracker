import logging

from flask import Blueprint, flash, render_template, redirect
from app import db, app_bp
from .forms import LoginForm

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        name = login.username.data
        pw = login.password.data
        if db.session.query(User).filter_by(username = name).first():
            flash('Username already in use. Please choose another.')
            return redirect(url_for('login_bp.create_account'))
        else:
            db.session.add(User(username=name, password=pw))
            db.session.commit()
            return redirect(url_for('app_bp.index'))

    return render_template('login/create_account.html', login_form=login_form)
