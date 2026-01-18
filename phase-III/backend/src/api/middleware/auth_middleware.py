import json
from fastapi import Request, HTTPException
from jose import jwt
from starlette.responses import JSONResponse
import os

SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret-key-for-development")
ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    """
    Middleware to validate JWT tokens for authenticated endpoints
    """
    # Skip authentication for public endpoints
    if request.url.path in ["/", "/health"]:
        response = await call_next(request)
        return response

    # Check for auth exempt paths (like static files, docs, etc.)
    if any(exempt_path in request.url.path for exempt_path in ["/docs", "/redoc", "/openapi.json"]):
        response = await call_next(request)
        return response

    # Look for Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": {"code": "MISSING_AUTH_HEADER", "message": "Authorization header missing or malformed"}}
        )

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Add user info to request state for downstream handlers
        request.state.user_id = payload.get("sub")
        if not request.state.user_id:
            return JSONResponse(
                status_code=401,
                content={"error": {"code": "INVALID_TOKEN", "message": "Invalid token: no user ID"}}
            )

    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"error": {"code": "TOKEN_EXPIRED", "message": "Token has expired"}}
        )
    except jwt.JWTError:
        return JSONResponse(
            status_code=401,
            content={"error": {"code": "INVALID_TOKEN", "message": "Could not validate token"}}
        )
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": {"code": "AUTH_ERROR", "message": "Authentication error"}}
        )

    response = await call_next(request)
    return response