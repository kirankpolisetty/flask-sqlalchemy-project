import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_user(client):
    response = client.post(
        "/users", json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_create_user_missing_fields(client):
    response = client.post("/users", json={"name": "Bob"})
    assert response.status_code == 400


def test_get_user(client):
    created = client.post(
        "/users", json={"name": "Carol", "email": "carol@example.com"}
    ).get_json()
    user_id = created["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["email"] == "carol@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_update_user(client):
    created = client.post(
        "/users", json={"name": "Dave", "email": "dave@example.com"}
    ).get_json()
    user_id = created["id"]

    response = client.put(f"/users/{user_id}", json={"name": "David"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "David"


def test_update_user_not_found(client):
    response = client.put("/users/9999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_user(client):
    created = client.post(
        "/users", json={"name": "Eve", "email": "eve@example.com"}
    ).get_json()
    user_id = created["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_create_user_duplicate_email(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    response = client.post(
        "/users", json={"name": "Alice2", "email": "alice@example.com"}
    )
    assert response.status_code == 409


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
