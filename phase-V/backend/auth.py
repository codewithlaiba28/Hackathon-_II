import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, jwk
from jose.utils import base64url_decode
from sqlmodel import Session, select, text
import models
import schemas
from db import get_session

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

# Shared secret for Better Auth token verification (HS256 fallback)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

if not SECRET_KEY:
    logger.warning("BETTER_AUTH_SECRET not set, authentication may fail in production.")

# Cache for JWKS keys to avoid DB lookups on every request
_jwks_cache: dict = {}
_jwks_cache_time: Optional[datetime] = None
JWKS_CACHE_TTL = timedelta(minutes=10)


def _get_jwks_from_db(db: Session) -> list:
    """
    Read JWKS public keys from the Better Auth jwks table in the shared database.
    Better Auth's JWT plugin stores signing keys in the 'jwks' table.
    """
    global _jwks_cache, _jwks_cache_time
    
    now = datetime.utcnow()
    if _jwks_cache and _jwks_cache_time and (now - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache.get("keys", [])
    
    try:
        result = db.exec(text('SELECT "publicKey", "id" FROM "jwks" ORDER BY "createdAt" DESC'))
        rows = result.all()
        
        keys = []
        for row in rows:
            try:
                pub_key = json.loads(row[0]) if isinstance(row[0], str) else row[0]
                keys.append(pub_key)
            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Failed to parse JWKS key {row[1]}: {e}")
        
        _jwks_cache = {"keys": keys}
        _jwks_cache_time = now
        logger.info(f"Loaded {len(keys)} JWKS keys from database")
        return keys
    except Exception as e:
        logger.error(f"Failed to load JWKS from database: {e}")
        return _jwks_cache.get("keys", [])


def decode_token_jwks(token: str, db: Session) -> Optional[schemas.TokenData]:
    """
    Decode and verify Better Auth JWT using JWKS public keys from the database.
    Better Auth's JWT plugin signs tokens with RS256 using keys stored in the jwks table.
    """
    try:
        # Get the token header to find the key ID (kid)
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        alg = header.get("alg", "RS256")
        
        logger.debug(f"JWT header: alg={alg}, kid={kid}")
        
        # Get JWKS keys from database
        keys = _get_jwks_from_db(db)
        
        if not keys:
            logger.warning("No JWKS keys found in database")
            return None
        
        # Find the matching key
        matching_key = None
        for key in keys:
            if kid and key.get("kid") == kid:
                matching_key = key
                break
        
        # If no kid match, try the first key
        if not matching_key and keys:
            matching_key = keys[0]
        
        if not matching_key:
            logger.warning("No matching JWKS key found")
            return None
        
        # Decode the token with the JWKS public key
        payload = jwt.decode(
            token, 
            matching_key, 
            algorithms=[alg, "RS256", "ES256"],
            options={"verify_aud": False}
        )
        
        # Better Auth JWT plugin puts user data in the payload
        user_id = payload.get("sub") or payload.get("userId") or payload.get("id")
        
        if user_id:
            logger.info(f"Successfully verified JWT for user: {user_id}")
            return schemas.TokenData(user_id=user_id)
        
        logger.warning(f"JWT payload missing user ID. Keys: {list(payload.keys())}")
        return None
    except JWTError as e:
        logger.debug(f"JWKS JWT verification failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during JWKS JWT verification: {e}")
        return None


def decode_token(token: str) -> Optional[schemas.TokenData]:
    """
    Decode and verify Better Auth JWT session token using HS256 (legacy fallback).
    """
    if not SECRET_KEY:
        return None
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        user_id = payload.get("userId") or payload.get("sub") or payload.get("id")

        if user_id:
            return schemas.TokenData(user_id=user_id)
        
        logger.warning(f"Token payload missing user ID: {payload.keys()}")
        return None
    except JWTError:
        # Normal to fail if token is not HS256
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
    Tries verification in order:
    1. JWKS-based JWT verification (Better Auth JWT plugin - RS256)
    2. HS256 JWT verification (legacy fallback)
    3. Opaque session token lookup in database
    """
    token = credentials.credentials
    
    # 1. Try JWKS-based JWT verification (Better Auth JWT plugin uses RS256)
    token_data = decode_token_jwks(token, session)
    
    # 2. Fallback: Try HS256 JWT verification
    if not token_data:
        token_data = decode_token(token)
    
    # 3. Fallback: Check if it's an opaque session token in the DB
    if not token_data:
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
