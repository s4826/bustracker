import logging

from flask import Blueprint, flash, render_template, redirect
from sqlalchemy.orm.exc import NoResultFound
from app import db, app_bp
from .forms import LoginForm

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        name = login.username.data
        pw = login.password.data
        try:
            user = db.session.query(User).filter_by(username = name).one()
            if user.verify_password(pw):
                pass
            else:
                flash('Invalid password')
                return redirect(url_for('login_bp.login'))
        except NoResultFound:
            flash('Invalid username')
            return redirect(url_for('login_bp.login'))

    return render_template('login/login.html', login_form=login_form)
