from fastapi import FastAPI, Depends, HTTPException, status
from model import summarizer
from dotenv import load_dotenv
from schemas import UserCredentials, User, Texts
from app.auth import generate_token_response, JWTBearer 
from utils import verify_password
from db import connect_to_mongo, get_collection
from datetime import datetime
from utils import hash_password


load_dotenv()

version = "v1"

app = FastAPI(
    title="Text Summarizer",
    description="A simple text summarizer API.",
    version=version,
)

db = connect_to_mongo()


@app.get("/")
def root():
    """
    The root endpoint.
    """
    return {"message": f"Hello, Text Summarizer! {version}"}


@app.post("/register")
async def register(user: User):
    """
    Registers a new user.
    Args:
        user (UserCredentials): The user's registration details.

    Returns:
        dict: A dictionary containing the user's registration details.
    """

    collection = get_collection(db, "users")
    user.created_at = datetime.now()
    user.password = hash_password(user.password)
    result = collection.insert_one(dict(user))
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed",
        )

    return {"result": "User registered successfully"}


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
    collection = get_collection(db, "users")
    user = collection.find_one({"username": credentials.username})
    matched = verify_password(credentials.password, user["password"])
    if not user or not matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_token_response(user["username"])


@app.post("/summarize", dependencies=[Depends(JWTBearer())])
async def summarize_text(
    originalTexts: Texts,
):
    """
    Summarizes a given text.
    Args:
        request (Text): The request object containing the text to be summarized.

    Returns:
        dict: A dictionary containing the summarized text.
    """
    summary = summarizer(
        originalTexts.texts, max_length=1000, min_length=30, do_sample=False
    )
    return {"summary": summary}
