import datetime
from typing import List
from schemas import User
from dotenv import load_dotenv
from utils import hash_password
from db import connect_to_mongo
from loguru import logger

load_dotenv()

db = connect_to_mongo()
collection = db["users"]

# Delete all documents from the 'users' collection to avoid duplicates
collection.delete_many({})

dummy_users: List[User] = [
    User(
        username="admin",
        full_name="Admin User",
        password=hash_password("adminpassword"),
        email="admin@gmail.com",
        created_at=str(datetime.datetime.now()),
        role="admin",
    ),
    User(
        username="user1",
        full_name="User One",
        password=hash_password("user1password"),
        email="user1@gmail.com",
        created_at=str(datetime.datetime.now()),
        role="user",
    ),
    User(
        username="user2",
        full_name="User Two",
        password=hash_password("user2password"),
        email="user2@gmail.com",
        created_at=str(datetime.datetime.now()),
        role="user",
    ),
]

# Insert dummy users into MongoDB
collection.insert_many([dict(user) for user in dummy_users])

logger.success("### Dummy Users Created Successfully! ###")
