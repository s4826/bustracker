"""Login views"""

import asyncio

from flask import (
    Blueprint,
    Markup,
    current_app,
    flash,
    redirect,
    render_template,
    session,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from itsdangerous import TimedSerializer
from itsdangerous.exc import SignatureExpired
from sqlalchemy.orm.exc import NoResultFound

from bustracker.app.extensions import db
from bustracker.app.models import User
from bustracker.log_config import get_logger

from .forms import LoginForm, RegisterForm, ResendConfirmation

logger = get_logger("debug")

login_bp = Blueprint("login_bp", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login view"""

    session.permanent = False

    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        pw = login_form.password.data
        remember = login_form.remember.data
        try:
            user = db.session.query(User).filter_by(email=email).one()
            if user.verify_password(pw):
                if user.confirmed:
                    login_user(user, remember=remember, force=True)
                    logger.info("%s logged in", current_user)
                    flash("Logged in")
                    return redirect(url_for("app_bp.index"))
                else:
                    flash("Unconfirmed account")
                    resend = "Resend confirmation link"
                    flash(Markup(f'<a href="/reconfirm">{resend}</a>'))
                    return redirect(url_for("login_bp.login"))
            flash("Invalid password")
            return redirect(url_for("login_bp.login"))
        except NoResultFound:
            flash("Invalid username")
            return redirect(url_for("login_bp.login"))

    return render_template("login/login.html", login_form=login_form)


@login_bp.route("/logout", methods=["GET"])
def logout():
    """Logout view"""
    logger.info("%s logged out", current_user)
    logout_user()
    flash("Logged out")
    return redirect(url_for("app_bp.index"))


@login_bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration view"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        password = register_form.password.data
        user = get_user_by_email(email)

        if user is not None:
            flash("Email already registered")
            return redirect(url_for("login_bp.register"))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        logger.info("New user %s registered", new_user)

        # Send a confirmation email to the user
        asyncio.run(new_user.send_confirmation_email())

        flash(
            f"A confirmation email was sent to {email}. "
            + "Please confirm your account to log in."
        )
        return redirect(url_for("app_bp.index"))
    return render_template("login/register.html", register_form=register_form)


@login_bp.route("/reconfirm", methods=["GET", "POST"])
def reconfirm():
    resend_form = ResendConfirmation()
    if resend_form.validate_on_submit():
        email = resend_form.email.data
        user = get_user_by_email(email)
        if user is not None:
            asyncio.run(user.send_confirmation_email())
            flash("Confirmation email sent")
            return redirect(url_for("app_bp.index"))
        else:
            flash("Invalid email")
            return redirect(url_for("login_bp.reconfirm"))
    return render_template(
        "login/resend_confirmation_email.html", resend_form=resend_form
    )


@login_bp.route("/confirm_account/<token>", methods=["GET"])
def confirm_account(token):
    """Account confirmation view"""

    serializer = TimedSerializer(current_app.config["SECRET_KEY"])
    try:
        user_id = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        flash("Invalid confirmation token")
        return redirect(url_for("app_bp.index"))

    try:
        user = db.session.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        flash("Invalid confirmation token")
        return redirect(url_for("app_bp.index"))

    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    login_user(user)
    logger.info("User %s confirmed account", user)
    return render_template("login/successful_confirmation.html")


def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()
