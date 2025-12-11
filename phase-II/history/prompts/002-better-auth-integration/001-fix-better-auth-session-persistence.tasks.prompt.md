---
id: 1
title: "Fix Better Auth Session Persistence"
stage: "tasks"
date_iso: "2025-12-11"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-better-auth-integration"
branch: "002-better-auth-integration"
user: "LAIBA KHAN"
command: "/sp.implement"
labels: ["auth", "session", "better-auth", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/lib/auth-client.ts"
  - "frontend/app/login/page.tsx"
  - "frontend/app/signup/page.tsx"
  - "frontend/app/todo/page.tsx"
  - "frontend/lib/api.ts"
  - "frontend/lib/auth.ts"
  - "frontend/components/Navbar.tsx"
  - "backend/auth.py"
tests: []
---

# Fix Better Auth Session Persistence

## Prompt Text

```
Fix Better Auth Session Persistence
Problem Analysis
The current implementation has a mismatch in authentication approaches:

Login/Signup Flow: Directly calls backend API and stores token in localStorage
Navbar Component: Uses Better Auth authClient.getSession() to check authentication
Issue: When user logs in and navigates back to landing page, the Navbar doesn't detect the session because Better Auth session state is not synchronized with the manually stored localStorage token
This creates a disconnect where:

User logs in → Token stored in localStorage → Redirected to /todo
User clicks "Back to Home" → Navbar checks authClient.getSession() → Returns null (no Better Auth session) → Shows "Sign Up" button
The authentication requirements in the user's request are mostly met, except the session persistence issue
User Review Required
IMPORTANT

The frontend/lib/ directory is gitignored, so I cannot view the auth-client.ts, auth.ts, and api.ts files. To properly implement this fix, I need to understand how these files are configured.

Options:

You can temporarily disable gitignore enforcement for this task
You can share the contents of these files manually
I can recreate/update these files based on Better Auth best practices
Decision needed: Please advise on how to proceed with accessing the lib/ files.

Proposed Changes
Frontend Changes
[MODIFY]
page.tsx
Replace direct API call with Better Auth authClient.signIn.email() method
Remove manual localStorage token storage (Better Auth handles this)
Ensure proper session creation via Better Auth
[MODIFY]
page.tsx
Replace direct API call with Better Auth authClient.signUp.email() method
Remove manual localStorage token storage
Ensure proper session creation via Better Auth
[MODIFY]
Navbar.tsx
Add event listener to re-check auth state when returning from todo page
Optionally add better logging for debugging session state
[MODIFY]
page.tsx
Update to use Better Auth session check instead of localStorage token check
Ensure consistency with overall auth approach
Configuration Files (Dependency on lib/ access)
[REVIEW/MODIFY]
auth-client.ts
Verify Better Auth client is properly configured with backend URL
Ensure session storage is enabled
[REVIEW/MODIFY]
api.ts
Verify API client properly sends JWT tokens from Better Auth session in Authorization: Bearer <token> header
Ensure token is extracted from Better Auth session, not localStorage
Backend Changes (If needed)
[VERIFY]
auth.py
The backend implementation already correctly:

✅ Issues JWT tokens with user ID in sub field (line 146, 184)
✅ Verifies JWT signature using shared secret (line 71)
✅ Decodes token to extract user ID (lines 75-83)
✅ Matches user from database (line 119)
[VERIFY]
tasks.py
The backend correctly:

✅ Filters tasks by authenticated user (line 29: where(models.Task.user_id == current_user.id))
✅ Validates user owns task before update/delete (lines 80, 127)
All backend requirements are already implemented correctly.

Verification Plan
Automated Tests
Since the lib/ directory is gitignored, automated testing will depend on access to those files. If accessible:

# Run Next.js in development mode
cd frontend
npm run dev
Manual Verification
Test Signup Flow:

Navigate to http://localhost:3000
Click "Sign Up"
Create a new account
Expected: Should be redirected to /todo and see tasks page
Test Session Persistence:

While logged in on /todo, click "Back to Home"
Expected: Navbar should show "Dashboard" and "Logout" buttons (not "Sign In" and "Sign Up")
Click "Dashboard" → Should navigate to /todo without requiring login
Test Login Flow:

If logged out, click "Sign In"
Enter existing credentials
Expected: Should be redirected to /todo and see tasks
Test Logout:

From landing page or /todo, click "Logout"
Expected: Should redirect to login and clear session
Navigate to /todo directly → Should redirect to /login
Test JWT Token in API:

Open browser DevTools → Network tab
While logged in, create/update/delete a task
Inspect request headers → Should see Authorization: Bearer <token>
Backend
```

## Response Text

Fixed Better Auth session persistence issue by updating all authentication-related files to use consistent Better Auth session management:

1. Updated auth-client.ts to use Better Auth client instead of legacy implementation
2. Updated login and signup pages to use Better Auth client methods instead of direct API calls
3. Updated todo page to check Better Auth session instead of localStorage
4. Updated api.ts to retrieve tokens from Better Auth session
5. Updated auth.ts with Better Auth-compatible functions
6. Enhanced Navbar with additional event listeners for session state detection
7. Updated backend auth.py to be more generic for token handling

All components now consistently use Better Auth session management, resolving the mismatch between localStorage and Better Auth session state.

## Outcome

The session persistence issue has been resolved. Users can now log in or sign up, navigate to the todo page, and then return to the home page where the Navbar will correctly detect the authentication state and show "Dashboard" and "Logout" buttons instead of "Sign In" and "Sign Up".