from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from model import summarizer
from dotenv import load_dotenv
from typing import Dict
from .schemas import User
from .auth import get_current_user, generate_token_response

load_dotenv()

app = FastAPI()

# In-memory storage for user data
users_db: Dict[str, str] = {}


@app.get("/")
def root():
    return {"message": "Hello, Text Summarizer!"}

@app.post("/signup")
async def signup(user: User, response: Response):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    users_db[user.username] = user.password
    return generate_token_response(user.username, response)

@app.post("/login")
async def login(user: User, response: Response):
    user_password = users_db.get(user.username)
    if not user_password or user_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_token_response(user.username, response)

@app.post("/token")
async def token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO: Replace the username and password with your own
    if form_data.username == "user" and form_data.password == "password":
         return generate_token_response(form_data.username, response)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/summarize/")
async def summarize_text(text: str, token: str = Depends(get_current_user)):
    summary = summarizer(text, max_length=1000, min_length=30, do_sample=False)
    return {"summary": summary}