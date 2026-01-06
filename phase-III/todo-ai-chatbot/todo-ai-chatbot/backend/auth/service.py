"""
Auth service for handling Better Auth session validation
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.settings import settings
from typing import Dict, Any

auth_scheme = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> str:
    """
    Validates the token (mimicking Better Auth validation)
    In a real app, you would verify the JWT signature or call Better Auth's session API
    """
    try:
        # For this hackathon, we'll assume the token is a simple user_id or a basic JWT
        # In production, use jwt.decode(token.credentials, settings.secret_key, algorithms=["HS256"])
        payload = {"sub": token.credentials} # Mock payload
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
