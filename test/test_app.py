import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_hello_returns_200(client):
    response = client.get("/api/hello")
    assert response.status_code == 200


def test_hello_returns_json_with_message(client):
    response = client.get("/api/hello")
    data = response.get_json()
    assert data is not None
    assert data.get("message") == "hello"


def test_hello_content_type_is_json(client):
    response = client.get("/api/hello")
    assert response.content_type.startswith("application/json")


def test_hello_text_is_plain_and_distinct(client):
    response = client.get("/api/hello/text")
    assert response.status_code == 200
    assert response.content_type.startswith("text/plain")
    assert b"plain text" in response.data


def test_hello_ping_json_shape(client):
    response = client.get("/api/hello/ping")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"kind": "ping", "ok": True}


def test_hello_meta_lists_service_and_endpoints(client):
    response = client.get("/api/hello/meta")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("service") == "tests_in_CI"
    assert "/api/hello" in data.get("endpoints", [])
