# Feature Specification: Revert to Custom Backend Authentication

**Feature**: Revert to Custom Backend Authentication
**Branch**: `003-revert-better-auth`
**Date**: 2025-12-10
**Status**: Draft
**Input**: User request to revert Better Auth implementation and return to custom backend auth

## Overview

Revert the current Better Auth implementation and return to the original custom authentication system where login/signup endpoints are handled by the Python FastAPI backend. This ensures consistency between frontend and backend authentication methods.

## User Stories

### User Story 1: Login with Backend Authentication (P1)
As a user, I want to login through the backend authentication system so that I can access the todo application with my credentials.

**Acceptance Criteria:**
- User can login with email and password
- Backend validates credentials against stored user data
- Successful login returns JWT token
- Failed login returns appropriate error message

### User Story 2: Signup with Backend Authentication (P1)
As a new user, I want to create an account through the backend authentication system so that I can use the todo application.

**Acceptance Criteria:**
- User can signup with email, password, and name
- Backend creates new user in the database
- Passwords are properly hashed before storage
- Successful signup returns JWT token
- Duplicate email registration is prevented

### User Story 3: Backend Token Validation (P1)
As a system, I want to validate JWT tokens issued by the backend so that all API requests are properly authenticated and authorized.

**Acceptance Criteria:**
- Backend endpoints can validate JWT tokens issued by auth endpoints
- Unauthorized requests are rejected with proper HTTP status codes
- Valid authentication tokens allow access to protected endpoints
- User information can be extracted from the authentication token

## Success Criteria

- Login and signup endpoints are available on the backend
- Frontend communicates with backend auth endpoints instead of Better Auth
- JWT tokens issued by backend are properly validated by backend
- Authentication state is managed through localStorage
- All existing functionality continues to work without disruption

## Out of Scope

- OAuth provider integration
- Password reset functionality
- Two-factor authentication
- Social login providers

## Constraints and Assumptions

- The existing SQLModel User model will continue to be used
- JWT tokens will be issued and validated using python-jose
- Passwords will continue to be hashed with passlib
- Frontend will store tokens in localStorage
- Environment variables will be used for sensitive configuration

## Technical Requirements

- Backend must provide /api/auth/login endpoint
- Backend must provide /api/auth/signup endpoint
- Backend must validate JWT tokens for protected endpoints
- Frontend must use apiClient for login/signup instead of Better Auth client
- Frontend must store JWT tokens in localStorage
- Frontend must check localStorage for authentication state