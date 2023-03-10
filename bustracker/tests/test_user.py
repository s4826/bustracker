import asyncio
import email.parser
import logging
from functools import reduce

import pytest
import requests
from flask import session
from flask_login import current_user, login_user, logout_user
from itsdangerous import TimedSerializer
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

from bustracker.app import db
from bustracker.app.models import User


def test_password_verification(user):
    assert not user.verify_password("pass")
    assert user.verify_password("password")


def test_password_access(user):
    with pytest.raises(AttributeError):
        user.password


def test_flask_login(_app, user):
    with _app.app_context():
        with _app.test_request_context():
            assert not current_user.is_authenticated
            login_user(user)
            assert current_user.is_authenticated

    with _app.test_request_context():
        logout_user()
        assert not current_user.is_authenticated


def test_register_user(_app, _db, client, test_mail_server, caplog):
    with caplog.at_level(logging.CRITICAL):
        try:
            requests.get(test_mail_server)
        except ConnectionError:
            pytest.skip("No test mail server detected")

    _app.config["WTF_CSRF_ENABLED"] = False

    with client:
        response = client.post(
            "/register",
            data={
                "email": "user@test.com",
                "password": "password",
                "confirm_password": "password",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert db.session.query(User).filter_by(email="user@test.com").one()

    _app.config["WTF_CSRF_ENABLED"] = True


def test_confirmation_token(_app, user):
    with _app.app_context():
        serializer = TimedSerializer(_app.config["SECRET_KEY"])
        token = user.create_confirmation_token(serializer)
    assert serializer.loads(token) == user.id


def test_send_confirmation_email(_app, user, test_mail_server, caplog):
    # skip this test if no mail server is detected
    with caplog.at_level(logging.CRITICAL):
        try:
            requests.get(test_mail_server)
        except ConnectionError:
            pytest.skip("No test mail server detected")

    message_endpoint = "/api/v1/messages"
    with _app.app_context():
        asyncio.run(user.send_confirmation_email())

    auth = HTTPBasicAuth("test@test.com", "test")
    r = requests.get(test_mail_server + message_endpoint, auth=auth)
    assert r.json()

    message_id = r.json()[0]["ID"]
    r = requests.get(
        test_mail_server + message_endpoint + f"/{message_id}" + "/download", auth=auth
    )

    parser = email.parser.BytesParser()
    email_message = parser.parsebytes(r.content)
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            with _app.app_context():
                assert (
                    user.create_confirmation_token()
                    in part.get_payload(decode=True).decode()
                )


def test_reconfirm_invalid_email(_app, client):
    _app.config["WTF_CSRF_ENABLED"] = False
    with client:
        response = client.post(
            "/reconfirm", data={"email": "invalid@invalid.com"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert reduce(
            lambda x, y: x or y, ["Invalid email" in z for z in session["_flashes"]]
        )
    _app.config["WTF_CSRF_ENABLED"] = True
