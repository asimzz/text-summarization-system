import pytest
from fastapi.testclient import TestClient
from app import app   

# Create a TestClient instance for your FastAPI app

client = TestClient(app)


def test_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Text Summarizer! v1"}


def test_register_user():
    """
    Test user registration.
    """
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "password": "strongpassword123",
        "email": "testuser@example.com",
        "role": "user",
        "created_at": "2021-01-01T00:00:00"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["result"] == "User registered successfully"


def test_login_successful():
    """
    Test a successful login.
    """
    login_data = {
        "username": "Lee",
        "password": "waai99#"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    """
    Test login failure for incorrect credentials.
    """
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_summarize_unauthorized():
    """
    Test summarization without authentication.
    """
    text_data = {
        "text": "This is a test text to be summarized."
    }
    response = client.post("/summarize", json=text_data)
    assert response.status_code == 403  # Should return forbidden as it requires authentication
