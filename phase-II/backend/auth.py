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
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "LKA0MD6mwFSKmix2G7VrKmfYH8l8iO_Jsxo0T5bsLZM")
ALGORITHM = "HS256"

def decode_token(token: str) -> Optional[schemas.TokenData]:
    """
    Decode and verify Better Auth JWT session token.
    """
    try:
        print(f"DEBUG: Attempting to decode token: {token[:20]}...")
        # Decode the token using the shared secret
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        # Better Auth JWT plugin puts session data in the payload
        # The session contains userId
        user_id = payload.get("userId") or payload.get("sub") or payload.get("id")

        if user_id:
            return schemas.TokenData(user_id=user_id)
        
        logger.warning(f"Token payload missing user ID: {payload.keys()}")
        print(f"DEBUG: Token payload missing user ID: {payload.keys()}")
        return None
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        print(f"DEBUG: JWT verification failed: {str(e)}")
        # Check if it might be an opaque session token
        print("DEBUG: Checking if it's a database session token is NOT yet implemented in this block.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {str(e)}")
        print(f"DEBUG: Unexpected error decoding token: {str(e)}")
        # Check if it is a session token in the database
        try:
            with Session(get_session()) as session_db: # Use transient session for auth check
                # Note: get_session is a generator, so we need to handle it properly or just use a new engine connection
                # Simplified: assuming we can just use the token to query
                # Since get_session is a dependency, we might not be able to easy use it inside this synchronous function 
                # unless we change decode_token to async OR use a separate db helper.
                # However, decode_token is called by get_current_user which HAS a session.
                pass
        except:
            pass
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
            print(f"DEBUG: detected signed token, using clean part: {clean_token[:10]}...")

        statement = select(models.Session).where(models.Session.token == clean_token)
        session_record = db.exec(statement).first()

        if not session_record:
            print(f"DEBUG: Session token not found in DB: {token[:10]}...")
            return None
        
        if session_record.expiresAt < datetime.utcnow():
            print("DEBUG: Session token expired")
            # Optional: delete expired session
            return None
            
        return schemas.TokenData(user_id=session_record.userId)
    except Exception as e:
        logger.error(f"Database session verification failed: {str(e)}")
        print(f"DEBUG: Database session verification failed: {str(e)}")
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
