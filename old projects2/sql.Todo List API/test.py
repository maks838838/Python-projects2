import secrets
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Disable rate limiting for the normal tests.
    # Otherwise 5 requests/minute can interfere with the tests.
    app.config["RATELIMIT_ENABLED"] = False

    with app.test_client() as client:
        yield client


def create_test_user(client):
    random_value = secrets.token_hex(4)

    response = client.post("/register", json={
        "email": f"test{random_value}@example.com",
        "password": "password",
        "login": f"user{random_value}"
    })

    assert response.status_code == 201

    data = response.get_json()

    return data["token"]


def test_register(client):
    random_value = secrets.token_hex(4)

    response = client.post("/register", json={
        "email": f"test{random_value}@example.com",
        "password": "password",
        "login": f"user{random_value}"
    })

    assert response.status_code == 201

    data = response.get_json()

    assert "id" in data
    assert "login" in data
    assert "token" in data


def test_register_duplicate_email(client):
    random_value = secrets.token_hex(4)

    user = {
        "email": f"test{random_value}@example.com",
        "password": "password",
        "login": f"user{random_value}"
    }

    response = client.post("/register", json=user)

    assert response.status_code == 201

    response = client.post("/register", json={
        "email": user["email"],
        "password": "anotherpassword",
        "login": f"another{random_value}"
    })

    assert response.status_code == 400


def test_register_missing_data(client):
    response = client.post("/register", json={})

    assert response.status_code == 400


def test_register_short_password(client):
    random_value = secrets.token_hex(4)

    response = client.post("/register", json={
        "email": f"test{random_value}@example.com",
        "password": "abc",
        "login": f"user{random_value}"
    })

    assert response.status_code == 400


def test_login(client):
    random_value = secrets.token_hex(4)

    user = {
        "email": f"test{random_value}@example.com",
        "password": "password",
        "login": f"user{random_value}"
    }

    register_response = client.post("/register", json=user)

    assert register_response.status_code == 201

    response = client.post("/login", json={
        "email": user["email"],
        "password": user["password"]
    })

    assert response.status_code == 201

    data = response.get_json()

    assert "token" in data
    assert data["login"] == user["login"]


def test_login_wrong_password(client):
    random_value = secrets.token_hex(4)

    user = {
        "email": f"test{random_value}@example.com",
        "password": "password",
        "login": f"user{random_value}"
    }

    client.post("/register", json=user)

    response = client.post("/login", json={
        "email": user["email"],
        "password": "wrongpassword"
    })

    assert response.status_code == 401


def test_login_missing_password(client):
    random_value = secrets.token_hex(4)

    response = client.post("/login", json={
        "email": f"test{random_value}@example.com"
    })

    assert response.status_code == 400


def test_create_todo(client):
    token = create_test_user(client)

    response = client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Buy groceries",
            "description": "Buy milk and bread"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "id" in data
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Buy milk and bread"


def test_create_todo_without_token(client):
    response = client.post(
        "/todos",
        json={
            "title": "Buy groceries",
            "description": "Buy milk"
        }
    )

    assert response.status_code == 401


def test_create_todo_invalid_token(client):
    response = client.post(
        "/todos",
        headers={"Authorization": "fake_token"},
        json={
            "title": "Buy groceries",
            "description": "Buy milk"
        }
    )

    assert response.status_code == 401


def test_create_todo_missing_data(client):
    token = create_test_user(client)

    response = client.post(
        "/todos",
        headers={"Authorization": token},
        json={}
    )

    assert response.status_code == 400


def test_get_todos(client):
    token = create_test_user(client)

    client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Todo 1",
            "description": "Description 1"
        }
    )

    response = client.get(
        "/todos",
        headers={"Authorization": token}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "data" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data


def test_get_todos_without_token(client):
    response = client.get("/todos")

    assert response.status_code == 401


def test_update_todo(client):
    token = create_test_user(client)

    create_response = client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Old title",
            "description": "Old description"
        }
    )

    todo_id = create_response.get_json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        headers={"Authorization": token},
        json={
            "title": "New title",
            "description": "New description"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == todo_id
    assert data["title"] == "New title"
    assert data["description"] == "New description"


def test_update_nonexistent_todo(client):
    token = create_test_user(client)

    response = client.put(
        "/todos/999999",
        headers={"Authorization": token},
        json={
            "title": "New title",
            "description": "New description"
        }
    )

    assert response.status_code == 403


def test_update_todo_without_token(client):
    response = client.put(
        "/todos/1",
        json={
            "title": "New title",
            "description": "New description"
        }
    )

    assert response.status_code == 401


def test_delete_todo(client):
    token = create_test_user(client)

    create_response = client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Delete me",
            "description": "This will be deleted"
        }
    )

    todo_id = create_response.get_json()["id"]

    response = client.delete(
        f"/todos/{todo_id}",
        headers={"Authorization": token}
    )

    assert response.status_code == 204


def test_delete_nonexistent_todo(client):
    token = create_test_user(client)

    response = client.delete(
        "/todos/999999",
        headers={"Authorization": token}
    )

    assert response.status_code == 404


def test_delete_todo_without_token(client):
    response = client.delete("/todos/1")

    assert response.status_code == 401


def test_pagination(client):
    token = create_test_user(client)

    for i in range(5):
        client.post(
            "/todos",
            headers={"Authorization": token},
            json={
                "title": f"Todo {i}",
                "description": f"Description {i}"
            }
        )

    response = client.get(
        "/todos?page=1&limit=2",
        headers={"Authorization": token}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["data"]) == 2
    assert data["total"] >= 5


def test_filtering(client):
    token = create_test_user(client)

    client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Buy milk",
            "description": "Go to the shop"
        }
    )

    client.post(
        "/todos",
        headers={"Authorization": token},
        json={
            "title": "Go running",
            "description": "Run for 30 minutes"
        }
    )

    response = client.get(
        "/todos?term=milk",
        headers={"Authorization": token}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["total"] >= 1

    for todo in data["data"]:
        assert (
            "milk" in todo["title"].lower()
            or "milk" in todo["description"].lower()
        )