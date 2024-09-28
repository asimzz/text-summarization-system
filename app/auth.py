import os
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional, Dict
from .schemas import User, Token


load_dotenv()

ALGORITHM = "HS256"
token_secret_key =  os.getenv("TOKEN_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory storage for user data
users_db: Dict[str, str] = {}

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
    
    print("token", token)
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

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The access token used for authentication.

    Returns:
        dict: The payload extracted from the access token.
    """
    payload = decode_access_token(token)
    return payload


def generate_token_response(username:str, response: Response):
    """
    Generates an access token for the given username and sets it as an HTTP-only cookie in the response.

    Args:
        username (str): The username for which the access token is generated.
        response (Response): The response object where the access token cookie will be set.

    Returns:
        Token: An object containing the access token and its type.
    """
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return Token(access_token=access_token,token_type="bearer")

def register_user(user: User):
    """
    Registers a new user in the system.

    Args:
        user (User): The user object containing the username and password.

    Raises:
        HTTPException: If the username is already registered, an HTTP 400 error is raised.
    """
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    users_db[user.username] = user.password