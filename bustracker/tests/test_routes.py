from .fixtures import _app, client  # noqa: F401


def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_logout_route(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_reconfirm(client):
    response = client.get("/reconfirm")
    assert response.status_code == 200
