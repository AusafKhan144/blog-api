from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.config import SERVICE_KEY
from app.db import session_local


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def validate_token(token: str = Depends(HTTPBearer())) -> str:
    expected_token = SERVICE_KEY
    if token.credentials != expected_token:
        raise HTTPException(401, "Unauthorized")
    return token
