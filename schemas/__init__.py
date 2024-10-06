from pydantic import BaseModel
from typing import List

class UserCredentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Text(BaseModel):
    text: str


class User(BaseModel):
    username: str
    full_name: str
    password: str
    email: str
    role: str
    created_at: str


class RequestLog(BaseModel):
    username: str
    user_id: str
    time: str
    endpoint: str
    status_code: int
    request_body: dict
    request_headers: dict
