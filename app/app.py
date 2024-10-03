from fastapi import FastAPI, Depends, HTTPException, status
from model import summarizer
from dotenv import load_dotenv
from app.schemas import UserCredentials, Text
from app.auth import generate_token_response, users_db, JWTBearer
from utils import verify_password


load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    """
    The root endpoint.
    """
    return {"message": "Hello, Text Summarizer! V.1.0"}


@app.post("/login")
async def login(credentials: UserCredentials):
    """
    Authenticates a user and generates an access token.
    Args:
        credentials (UserCredentials): The user's login credentials.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        dict: A dictionary containing the access token.
    """
    user = users_db.get(credentials.username)
    matched = verify_password(credentials.password, user["password"])
    if not user or not matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_token_response(user["username"])


@app.post("/summarize", dependencies=[Depends(JWTBearer())])
async def summarize_text(request: Text):
    """
    Summarizes a given text.
    Args:
        request (Text): The request object containing the text to be summarized.

    Returns:
        dict: A dictionary containing the summarized text.
    """
    summary = summarizer(request.text, max_length=1000, min_length=30, do_sample=False)
    return {"summary": summary}
