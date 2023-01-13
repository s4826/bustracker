from .fixtures import _app, client  # noqa: F401


def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_logout_route(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.location == "/"
