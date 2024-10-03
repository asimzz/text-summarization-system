from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Text(BaseModel):
    text: str