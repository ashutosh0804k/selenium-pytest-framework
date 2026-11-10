import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_list_users_returns_page_one(api):
    resp = api.list_users(page=1)
    body = resp.json()
    assert resp.status_code == 200
    assert body["page"] == 1
    assert len(body["data"]) > 0


def test_list_users_pages_differ(api):
    first = api.list_users(page=1).json()["data"]
    second = api.list_users(page=2).json()["data"]
    assert {u["id"] for u in first}.isdisjoint({u["id"] for u in second})


def test_user_has_expected_fields(api):
    user = api.get_user(2).json()["data"]
    for field in ("id", "email", "first_name", "last_name", "avatar"):
        assert field in user
    assert user["id"] == 2


def test_missing_user_returns_404(api):
    resp = api.get_user(23)
    assert resp.status_code == 404
    assert resp.json() == {}


@pytest.mark.smoke
def test_create_user(api):
    resp = api.create_user("Ashutosh", "SDET")
    body = resp.json()
    assert resp.status_code == 201
    assert body["name"] == "Ashutosh"
    assert body["job"] == "SDET"
    assert "id" in body


def test_update_user(api):
    resp = api.update_user(2, "Ashutosh", "QA Lead")
    body = resp.json()
    assert resp.status_code == 200
    assert body["job"] == "QA Lead"
    assert "updatedAt" in body


def test_delete_user(api):
    assert api.delete_user(2).status_code == 204


def test_register_success_returns_token(api):
    resp = api.register({"email": "eve.holt@reqres.in", "password": "pistol"})
    assert resp.status_code == 200
    assert "token" in resp.json()


def test_register_without_password_fails(api):
    resp = api.register({"email": "sydney@fife"})
    assert resp.status_code == 400
    assert resp.json()["error"] == "Missing password"


def test_login_success_returns_token(api):
    resp = api.login({"email": "eve.holt@reqres.in", "password": "cityslicka"})
    assert resp.status_code == 200
    assert "token" in resp.json()


def test_login_without_password_fails(api):
    resp = api.login({"email": "peter@klaven"})
    assert resp.status_code == 400
    assert resp.json()["error"] == "Missing password"
