import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b'href="/create' not in response.data
    assert b'href="/1/update' not in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"Test title" in response.data
    assert b"Year: 1999, Rating: 9.9" in response.data
    assert b'href="/1/update' in response.data
    assert b'href="/create' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize(
    "path",
    (
        "/4/update",
        "/5/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    response = client.post(path)
    assert response.status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    response = client.post(
        "/create",
        data={
            "title": "Created",
            "year": "2000",
            "rating": "1.0",
            "url": "https://testsite.com",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM movies").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    response = client.post(
        "/1/update", data={"title": "Updated", "year": "2000", "rating": "", "url": ""}
    )
    assert response.status_code == 302

    with app.app_context():
        db = get_db()
        movie = db.execute("SELECT * FROM movies WHERE id = 1").fetchone()
        assert movie["title"] == "Updated"
        assert movie["year"] == 2000


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(
        path, data={"title": "", "year": "", "rating": "", "url": ""}
    )
    assert b"Title is required." in response.data


def test_print_response(client, auth):
    auth.login()
    response = client.get("/")
    print(response.data)
    print(type(response.data))


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        movie = db.execute("SELECT * FROM movies WHERE id = 1").fetchone()
        assert movie is None
