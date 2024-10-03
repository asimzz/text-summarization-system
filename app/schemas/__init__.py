from pydantic import BaseModel


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
    role: str
