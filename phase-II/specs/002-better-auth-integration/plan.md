# Implementation Plan: Better Auth Integration

**Branch**: `002-better-auth-integration` | **Date**: 2025-12-10 | **Spec**: [link to specs/002-better-auth-integration/spec.md]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of Better Auth integration to replace the current manual JWT authentication system. This will provide standardized authentication with improved security practices, proper session management, and better integration between the Next.js frontend and FastAPI backend.

## Technical Context

**Language/Version**: TypeScript/JavaScript for Next.js, Python for FastAPI
**Primary Dependencies**: better-auth, next, fastapi, sqlmodel, python-jose, passlib
**Storage**: Shared SQLite database (todo_app.db) for both auth and tasks
**Testing**: Jest/React Testing Library for frontend, pytest for backend
**Target Platform**: Web application with Next.js frontend and FastAPI backend
**Performance Goals**: Maintain current performance while improving security
**Constraints**: Must maintain compatibility with existing user data and API contracts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ SPEC-FIRST RULE: Following spec-first approach as per constitution
- ✅ TECHNOLOGY RULES: Using Better Auth as required, with Next.js and FastAPI
- ✅ MONOREPO RULE: Maintaining proper frontend/backend structure in monorepo
- ✅ SIMPLICITY & BEAUTY RULE: Designing clean authentication flow
- ✅ AUTH RULE: Implementing standardized authentication with Better Auth
- ✅ SECURITY RULE: Following industry-standard authentication practices

## Project Structure

### Documentation (this feature)
```text
specs/002-better-auth-integration/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Research findings
├── data-model.md        # Updated data model
├── quickstart.md        # Quickstart guide
├── contracts/           # API contracts
└── tasks.md             # Implementation tasks
```

### Source Code Changes

**Frontend Changes:**
```text
frontend/
├── lib/
│   ├── auth.ts              # [MODIFY] Better Auth initialization
│   ├── auth-client.ts       # [NEW] Better Auth client initialization
│   └── api.ts               # [MODIFY] Update API client to use Better Auth
├── app/
│   └── api/
│       └── auth/
│           └── [...all]/
│               └── route.ts # [NEW] Better Auth API route handler
└── components/
    └── common/
        └── AuthButton.tsx   # [MODIFY] Update to use Better Auth
```

**Backend Changes:**
```text
backend/
├── auth.py                 # [MODIFY] Remove manual JWT endpoints, add Better Auth validation
├── better_auth_config.py   # [EXISTING] Better Auth server configuration
├── db.py                   # [MODIFY] Ensure database compatibility
└── main.py                 # [MODIFY] Add authentication middleware
```

## Architecture Design

### Frontend Authentication Flow
1. Better Auth client is initialized in the frontend
2. Authentication state is managed by Better Auth
3. API requests include Better Auth tokens in headers
4. Protected routes check authentication state via Better Auth

### Backend Token Validation
1. Better Auth creates sessions in the shared database
2. FastAPI endpoints validate tokens by checking session table
3. User information is retrieved from session data
4. Unauthorized requests return 401 status

### Database Integration
- Use shared SQLite database for both auth and application data
- Better Auth creates its own tables for session management
- Maintain existing user data compatibility

## Implementation Approach

### Phase 1: Frontend Integration
- Initialize Better Auth client in Next.js
- Set up API route handlers for auth endpoints
- Update existing auth.ts to work with Better Auth
- Update API client to use Better Auth tokens

### Phase 2: Backend Integration
- Update auth.py to validate Better Auth sessions
- Remove manual JWT login/signup endpoints
- Ensure token validation works with Better Auth format
- Update middleware to work with Better Auth tokens

### Phase 3: Integration & Testing
- Test complete authentication flow
- Verify token validation between frontend and backend
- Ensure existing functionality continues to work
- Test migration from old JWT to Better Auth

## Security Considerations

- Use proper secret management for Better Auth configuration
- Ensure secure token storage and transmission
- Implement proper session validation in backend
- Follow Better Auth security best practices

## Migration Strategy

- Maintain backward compatibility during transition
- Ensure existing user accounts continue to work
- Provide smooth transition for current users
- Test migration path thoroughly