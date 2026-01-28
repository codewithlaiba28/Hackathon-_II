import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session, select
import models
import schemas
from db import get_session

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

# Shared secret for Better Auth token verification
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

if not SECRET_KEY:
    logger.warning("BETTER_AUTH_SECRET not set, authentication may fail in production.")

def decode_token(token: str) -> Optional[schemas.TokenData]:
    """
    Decode and verify Better Auth JWT session token.
    """
    if not SECRET_KEY:
        return None
        
    try:
        # Decode the token using the shared secret
        # Better Auth JWTs usually don't have audience specified in the same way, so we skip verify_aud
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        # Better Auth JWT plugin puts session data in the payload
        # The session contains userId
        user_id = payload.get("userId") or payload.get("sub") or payload.get("id")

        if user_id:
            return schemas.TokenData(user_id=user_id)
        
        logger.warning(f"Token payload missing user ID: {payload.keys()}")
        return None
    except JWTError:
        # It is normal to fail JWT decoding if the token is an opaque session token
        return None

def verify_session_token(token: str, db: Session) -> Optional[schemas.TokenData]:
    """
    Verify opaque session token against database.
    """
    try:
        # Handle signed tokens (token.signature) - typically used in cookies
        # The DB stores only the raw token part (before the dot)
        clean_token = token
        if "." in token:
            clean_token = token.split(".")[0]

        statement = select(models.Session).where(models.Session.token == clean_token)
        session_record = db.exec(statement).first()

        if not session_record:
            return None
        
        if session_record.expiresAt < datetime.utcnow():
            logger.info("Session token expired")
            return None
            
        return schemas.TokenData(user_id=session_record.userId)
    except Exception as e:
        logger.error(f"Database session verification failed: {str(e)}")
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    session: Session = Depends(get_session)
) -> models.User:
    """
    Dependency to get the current authenticated user from Better Auth token.
    """
    token = credentials.credentials
    token_data = decode_token(token)
    
    if not token_data:
        # Fallback: Check if it's an opaque session token in the DB
        token_data = verify_session_token(token, session)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(models.User, token_data.user_id)
    if not user:
        # User should exist in the database as Better Auth creates them
        logger.warning(f"User {token_data.user_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user
