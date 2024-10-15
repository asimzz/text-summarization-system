from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from model import summarizer
from dotenv import load_dotenv
from schemas import UserCredentials, User, Text, RequestLog
from app.auth import generate_token_response, get_authenticated_user
from app.auth import JWTBearer
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
users_collection = get_collection(db, "users")
logs_collection = get_collection(db, "logs")


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
    user.created_at = datetime.now()
    user.password = hash_password(user.password)
    result = users_collection.insert_one(dict(user))
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
    if user:
        matched = verify_password(credentials.password, user["password"])
    if not user or not matched:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_token_response(user["username"])


@app.post("/summarize", dependencies=[Depends(JWTBearer())])
async def summarize_text(originalTexts: Text, request: Request):
    """
    Summarizes a given text.
    Args:
        request (Text): The request object containing the text to be summarized.

    Returns:
        dict: A dictionary containing the summarized text.
    """
    username = get_authenticated_user(request)
    user = User.model_validate(users_collection.find_one({"username": username}))

    summary = summarizer(
        originalTexts.text, max_length=1000, min_length=30, do_sample=False
    )

    summary_result = {"summary": summary}

    request_log = RequestLog(
        username=user.username,
        user_id=str(user._id),
        time=str(datetime.now()),
        endpoint=request.url.path,
        request_body=dict(originalTexts),
        request_headers=dict(request.headers),
        response_body=dict(summary_result),
    )

    log_result = logs_collection.insert_one(dict(request_log))
    if not log_result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request logging failed",
        )
    return summary_result["summary"][0]
