from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from . import models, schemas, db
from .db import get_session
import os
from passlib.context import CryptContext
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET", "c4f04665bdfd926af97a01aa5b67bf76")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback for different hash formats
        from passlib.hash import pbkdf2_sha256
        try:
            return pbkdf2_sha256.verify(plain_password, hashed_password)
        except:
            # If all methods fail, return False
            return False

def get_password_hash(password: str) -> str:
    # Truncate password to 72 bytes to comply with bcrypt limits
    truncated_password = password[:72] if len(password) > 72 else password
    try:
        return pwd_context.hash(truncated_password)
    except Exception:
        # Complete fallback to pbkdf2_sha256 if bcrypt fails completely
        from passlib.hash import pbkdf2_sha256
        return pbkdf2_sha256.hash(truncated_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[schemas.TokenData]:
    """
    Decode and verify JWT token to extract user information.
    This function implements the token verification step in the authentication flow.
    """
    try:
        logger.info(f"Attempting to decode JWT token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token does not contain user ID in 'sub' field")
            return None
        token_data = schemas.TokenData(user_id=user_id)
        logger.info(f"Successfully decoded token for user_id: {user_id}")
        return token_data
    except JWTError as e:
        logger.error(f"JWT token verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during token decoding: {str(e)}")
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    """
    Get the current authenticated user based on the JWT token.
    This function implements the user identification step in the authentication flow.
    """
    token = credentials.credentials
    logger.info(f"Verifying user authentication with token")

    token_data = decode_token(token)
    if token_data is None:
        logger.warning("Token validation failed - could not decode token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Looking up user with ID: {token_data.user_id}")
    user = session.get(models.User, token_data.user_id)
    if user is None:
        logger.warning(f"User with ID {token_data.user_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Successfully authenticated user: {user.email}")
    return user

@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, session: Session = Depends(get_session)):
    # Find user by email
    user = session.query(models.User).filter(models.User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user_id in 'sub' field as required
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},  # Store user_id in 'sub' field as required
        expires_delta=access_token_expires
    )

    # Update last login time
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()

    return schemas.LoginResponse(
        token=access_token,
        user=schemas.UserResponse.from_orm(user)
    )

@router.post("/signup", response_model=schemas.LoginResponse)
def signup(request: schemas.SignupRequest, session: Session = Depends(get_session)):
    # Check if user already exists
    user = session.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = get_password_hash(request.password)
    user = models.User(
        email=request.email,
        password=hashed_password,
        name=request.name
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Login the new user immediately
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},  # Store user_id in 'sub' field as required
        expires_delta=access_token_expires
    )

    # Update last login time
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()

    return schemas.LoginResponse(
        token=access_token,
        user=schemas.UserResponse.from_orm(user)
    )

@router.post("/logout", response_model=schemas.LogoutResponse)
def logout(request: schemas.LogoutRequest):
    # In a real implementation, you might add the token to a blacklist
    # For now, we just return success
    return schemas.LogoutResponse(success=True)