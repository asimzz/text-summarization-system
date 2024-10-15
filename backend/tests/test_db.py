import pytest
from unittest.mock import patch, MagicMock
from db import connect_to_mongo, get_collection
from pymongo.database import Database, Collection


# Test for the connect_to_mongo function
@patch("db.MongoClient")
def test_connect_to_mongo(mock_mongo_client):
    # Mock the MongoDB client
    mock_client = MagicMock()
    mock_db = MagicMock()
    
    # Set up the mock to return the mocked database
    mock_mongo_client.return_value = mock_client
    mock_client.__getitem__.return_value = mock_db

    # Call the function
    db = connect_to_mongo()

    # Ensure the MongoClient was called
    mock_mongo_client.assert_called_once()

    # Ensure the ping command was called on the admin database
    mock_client.admin.command.assert_called_once_with("ping")

    # Assert that the database returned is the mock database
    assert db == mock_db


# Test for the get_collection function
def test_get_collection():
    mock_db = MagicMock(spec=Database)
    mock_collection = MagicMock(spec=Collection)

    # Set the database to return a mock collection when accessing a collection name
    mock_db.__getitem__.return_value = mock_collection

    # Call the function
    collection = get_collection(mock_db, "users")

    # Assert that the correct collection was accessed
    mock_db.__getitem__.assert_called_once_with("users")
    assert collection == mock_collection
