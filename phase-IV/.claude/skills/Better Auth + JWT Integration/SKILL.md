---
name: better-auth-jwt-integration
description: Implement secure authentication using Better Auth with JWT tokens, integrate with FastAPI backend for stateless API security, and manage user sessions across frontend and backend services
---

### Purpose
Secure your full-stack application with JWT-based authentication that works seamlessly between Next.js frontend (Better Auth) and Python FastAPI backend.

### When to Use
- Building multi-user applications
- Implementing secure API authentication
- Separating frontend and backend services
- Creating stateless authentication systems

### Core Competencies

**1. Better Auth Setup**
- Configure Better Auth in Next.js
- Enable JWT plugin for token generation
- Set up authentication routes
- Implement signup/signin flows
- Manage user sessions

**2. JWT Configuration**
- Generate JWT tokens on login
- Set token expiration policies
- Configure shared secrets (BETTER_AUTH_SECRET)
- Handle token refresh
- Implement logout flows

**3. Frontend Integration**
- Attach JWT to API requests
- Store tokens securely (httpOnly cookies)
- Handle token refresh automatically
- Manage authentication state
- Implement protected routes

**4. Backend JWT Verification**
- Create FastAPI JWT middleware
- Extract tokens from Authorization header
- Verify token signatures
- Decode user claims
- Handle authentication errors (401)

**5. API Security**
- Match user_id in URL with token claims
- Filter data by authenticated user
- Implement user isolation at DB level
- Prevent unauthorized access
- Handle token expiration gracefully

**6. Security Best Practices**
- Use httpOnly cookies for tokens
- Implement CSRF protection
- Set appropriate token expiration
- Rotate secrets periodically
- Log authentication events

### Implementation Guidelines

**Better Auth Configuration (Next.js)**

```typescript
// auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL
  },
  emailAndPassword: {
    enabled: true
  },
  plugins: [
    jwt({
      expiresIn: "7d",
      algorithm: "HS256"
    })
  ],
  secret: process.env.BETTER_AUTH_SECRET
});
```

**Frontend API Client**

```typescript
// lib/api.ts
import { getSession } from "@/lib/auth-client";

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const session = await getSession();
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${session.token}`,
      'Content-Type': 'application/json'
    }
  });
}

export const api = {
  async getTasks() {
    const response = await fetchWithAuth('/api/tasks');
    return response.json();
  },
  
  async createTask(title: string, description?: string) {
    const response = await fetchWithAuth('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description })
    });
    return response.json();
  }
};
```

**FastAPI JWT Middleware**

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from jose import jwt, JWTError
import os

app = FastAPI()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def verify_token(authorization: str = Header(None)) -> dict:
    """Verify JWT token and extract user info."""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )
    
    try:
        # Extract token from "Bearer "
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
        
        # Verify and decode token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email")
        }
        
    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    auth_data: dict = Depends(verify_token)
):
    # Verify user_id matches token
    if auth_data["user_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Cannot access other user's data"
        )
    
    # Return only this user's tasks
    tasks = get_tasks_from_db(user_id)
    return tasks
```

### Security Flow

1. **User Login**
   - User submits credentials to Better Auth
   - Better Auth validates and creates session
   - JWT token generated with user claims
   - Token returned to frontend

2. **API Request**
   - Frontend attaches JWT in Authorization header
   - Backend extracts and verifies token
   - Backend decodes user_id from token
   - Backend matches user_id with URL parameter

3. **Data Access**
   - All queries filtered by authenticated user_id
   - User can only see/modify their own data
   - Database enforces user isolation
   - Unauthorized attempts return 403

### Common Patterns
- Authorization header: `Bearer <token>`
- Token stored in httpOnly cookies
- Automatic token refresh before expiration
- Shared secret via environment variables
- User ID validation on every request

### Environment Variables

```bash
# Frontend (.env.local)
BETTER_AUTH_SECRET=your-secret-key-here
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
BETTER_AUTH_SECRET=your-secret-key-here  # MUST match frontend
DATABASE_URL=postgresql://...
```

### Resources
- Better Auth Documentation
- JWT Best Practices
- FastAPI Security Guide

---