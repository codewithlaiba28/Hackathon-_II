import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session
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
    Decode and verify Better Auth session token.
    """
    try:
        # Decode the token using the shared secret
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        # Better Auth typically puts user ID in 'sub' or 'userId'
        user_id = payload.get("sub") or payload.get("userId") or payload.get("id")

        if user_id:
            return schemas.TokenData(user_id=user_id)
        
        logger.warning(f"Token payload missing user ID: {payload.keys()}")
        return None
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {str(e)}")
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(models.User, token_data.user_id)
    if not user:
        # If user doesn't exist in our DB but has a valid session, 
        # we might need to sync them. For now, raise 401.
        logger.warning(f"User {token_data.user_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/sync", response_model=schemas.UserResponse)
def sync_user(
    request: schemas.BetterAuthSyncRequest, 
    session: Session = Depends(get_session)
):
    """
    Sync user from Better Auth to our local database.
    Called by frontend after successful sign-in.
    """
    user = session.query(models.User).filter(models.User.email == request.email).first()
    
    if not user:
        # Minimalist user creation as Better Auth manages the rest
        user = models.User(
            email=request.email,
            name=request.name,
            password="EXTERNAL_AUTH" # Placeholder
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        if request.name and user.name != request.name:
            user.name = request.name
            session.add(user)
            session.commit()
            session.refresh(user)
            
    return user
