import pytest
from fastapi import status
from datetime import datetime
from fastapi.testclient import TestClient
from app.app import app
from unittest.mock import patch, MagicMock
from schemas import UserCredentials, Text, User

client = TestClient(app)


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, Text Summarizer! v1"}


def test_register_user_success():
    # Mock the insert_one method on the collection object to simulate a successful insertion.
    with patch("db.get_collection") as mock_get_collection:
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection
        mock_collection.insert_one.return_value.inserted_id = "mocked_id"

        user = User(
            username="testuser",
            full_name="Test User",
            password="testpassword",
            email="user@test.com",
            role="user",
            created_at=str(datetime.now()),
        )
        response = client.post("/register", json=dict(user))
        assert response.status_code == 200
        assert response.json() == {"result": "User registered successfully"}

# @pytest.fixture
# def mock_collection(mocker):
#     # Create a mock for the collection
#     mock_collection = MagicMock()
#     # Patch 'get_collection' to return the mock collection
#     mocker.patch("app.get_collection", return_value=mock_collection)
#     return mock_collection

# def test_register_user_db_failure(mock_collection):
#     user = User(
#         username="testuser",
#         full_name="Test User",
#         password="testpassword",
#         email="user@test.com",
#         role="user",
#         created_at=str(datetime.now()),
#     )
#     # Simulate 'insert_one' returning a result without an inserted_id
#     mock_collection.insert_one.return_value = MagicMock(inserted_id=None)

#     # Send a POST request to the /register endpoint
#     response = client.post("/register", json=dict(user))

#     # Assert that the status code is 400 as expected
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.json() == {"detail": "User registration failed"}
