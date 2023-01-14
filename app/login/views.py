import asyncio
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_user, logout_user, current_user
from sqlalchemy.orm.exc import NoResultFound
from itsdangerous import TimedSerializer
from itsdangerous.exc import SignatureExpired
from app.models import User
from .forms import LoginForm, RegisterForm
from app import db

from log_config import get_logger
logger = get_logger('debug')

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        pw = login_form.password.data
        try:
            user = db.session.query(User).filter_by(email=email).one()
            if user.verify_password(pw):
                login_user(user, remember=login_form.remember.data, force=True)
                logger.info(f'{current_user} logged in')
                flash('Logged in')
                return redirect(url_for('app_bp.index'))
            else:
                flash('Invalid password')
                return redirect(url_for('login_bp.login'))
        except NoResultFound:
            flash('Invalid username')
            return redirect(url_for('login_bp.login'))

    return render_template('login/login.html', login_form=login_form)


@login_bp.route('/logout', methods=['GET'])
def logout():
    logger.info(f'{current_user} logged out')
    logout_user()
    flash('Logged out')
    return redirect(url_for('app_bp.index'))


@login_bp.route('/register', methods=['GET', 'POST'])
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
            user = db.session.query(User).filter_by(email=email).first()
            if user is not None:
                flash('Email already registered')
                return redirect(url_for('login_bp.login'))
            else:
                new_user = User(email=email,
                                password=pw1)
                db.session.add(new_user)
                db.session.commit()
                logger.info(f'New user {new_user} registered')
                asyncio.run(new_user.send_confirmation_email())
                login_user(new_user, force=True)
                return redirect(url_for('app_bp.index'))
    return render_template('login/register.html', register_form=register_form)


@login_bp.route('/confirm_account/<token>', methods=['GET'])
def confirm_account(token):
    try:
        user = db.session.query(User).filter_by(id=token[0]).one()
    except NoResultFound:
        return redirect(url_for('app_bp.index'))
    serializer = TimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        flash('Invalid confirmation token')
        return redirect(url_for('app_bp.index'))

    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return render_template('login/successful_confirmation.html')
