import logging

from flask import Blueprint, flash, render_template, redirect
from sqlalchemy.orm.exc import NoResultFound
from app import db, app_bp
from app.models import User
from .forms import LoginForm, RegisterForm

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        name = login_form.username.data
        pw = login_form.password.data
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

@login_bp.route('/register', methods = ['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        pw1 = register_form.password.data
        pw2 = register_form.confirm_password.data
        if pw1 != pw2:
            flash('Passwords do not match')
            return redirect(url_for('login_bp.register'))
        else:
            user = db.session.query(User).filter_by(email = email).first()
            if user is not None:
                flash('Email already registered')
                return redirect(url_for('login_bp.login'))
            else:
                new_user = User(email=email,
                                password=pw1)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('app_bp.index'))
    return render_template('login/register.html', register_form=register_form)
