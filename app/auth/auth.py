import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, Dict
from utils import hash_password
from app.schemas import Token


load_dotenv()

ALGORITHM = "HS256"
token_secret_key = os.getenv("TOKEN_SECRET_KEY")

# TODO: Replace the username and password with your own
# In-memory storage for user data
users_db: Dict[str, str] = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "password": hash_password("user1password"),
        "role": "user",
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "password": hash_password("adminpassword"),
        "role": "admin",
    },
}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The time duration after which the token will expire.
                                            If not provided, the token will expire in 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodes a JWT access token to extract the username.
    Args:
        token (str): The JWT access token to decode.
    Returns:
        str: The username extracted from the token.
    Raises:
        HTTPException: If the token has expired or is invalid.
    """
    try:
        payload = jwt.decode(token, token_secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_token_response(username: str):
    """
    Generates an access token for the given username and sets it as an HTTP-only cookie in the response.

    Args:
        username (str): The username for which the access token is generated.
        response (Response): The response object where the access token cookie will be set.

    Returns:
        Token: An object containing the access token and its type.
    """
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
