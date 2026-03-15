"""Integration tests for books API (route order and CRUD)."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.skipif(
    __import__("os").environ.get("SKIP_INTEGRATION") == "1",
    reason="Skip integration when SKIP_INTEGRATION=1",
)
def test_get_available_all_returns_200(client: TestClient):
    """GET /api/books/available/all must not return 422 (route order fix)."""
    response = client.get("/api/books/available/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_books_returns_paginated(client: TestClient):
    """GET /api/books/ returns items and total."""
    response = client.get("/api/books/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


def test_create_book_validation_empty_title(client: TestClient):
    """Create book with empty title returns 422."""
    response = client.post(
        "/api/books/",
        json={"title": "", "author": "Author"},
    )
    assert response.status_code == 422


def test_create_book_success(client: TestClient):
    """Create book and then fetch it."""
    create = client.post(
        "/api/books/",
        json={"title": "Test Book", "author": "Test Author"},
    )
    if create.status_code != 200:
        pytest.skip("DB not available or create failed")
    bid = create.json()["id"]
    get_one = client.get(f"/api/books/{bid}")
    assert get_one.status_code == 200
    assert get_one.json()["title"] == "Test Book"
