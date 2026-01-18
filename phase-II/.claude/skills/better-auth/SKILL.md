---
name: better-auth
description: |
  This skill creates a comprehensive authentication system using Better Auth for both frontend and backend integration, with proper synchronization between systems. Use this skill when you need to implement secure authentication with Better Auth in your full-stack application.
---

# Better Auth Integration Skill

This skill should be used when users need to implement a comprehensive authentication system using Better Auth for both frontend and backend integration, with proper synchronization between systems.

## Skill Type: Builder

## Domain: Authentication Systems with Better Auth

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, authentication setup, current auth implementation |
| **Conversation** | User's specific requirements, constraints, preferences for auth flows |
| **Skill References** | Better Auth documentation, integration patterns, security considerations |
| **User Guidelines** | Project-specific conventions, team standards, compliance requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

Better Auth is a full-stack authentication solution that provides:
- Email/password authentication
- OAuth providers
- Session management
- Database adapters
- TypeScript support
- Customizable UI components

## Authentication Architecture

Better Auth follows a client-server architecture where:
- The server handles authentication logic and token generation
- The client manages sessions and provides UI components
- Database integration for user/session storage
- Plugin system for extended functionality

## Implementation Steps

### 1. Backend Setup (FastAPI Integration)

First, create the Better Auth configuration for the backend:

```typescript
// backend/better_auth_server.ts
import { betterAuth } from "better-auth";
import { db } from "./db"; // your database connection
import { drizzleAdapter } from "better-auth/adapters/drizzle";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'postgresql', // or your database provider
    schema: {
      // Define your schema mappings
    },
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  socialProviders: {
    // Configure OAuth providers if needed
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
  },
  account: {
    accountLinking: {
      enabled: true,
    },
  },
});
```

### 2. Frontend Client Setup

Create the Better Auth client configuration:

```typescript
// frontend/lib/auth-client.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000/api/auth",
});

export const { useSession, signIn, signUp, signOut } = authClient;
```

### 3. Environment Variables

Create/update your environment files:

```bash
# backend/.env
BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-super-secret-key-here
DATABASE_URL=your-database-url

# frontend/.env.local
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. API Route Integration (Next.js App Router)

Create the authentication API route:

```typescript
// frontend/app/api/auth/[...betterAuth]/route.ts
import { auth } from "@/lib/better-auth";
import { GET, POST } from "better-auth/integrations/next-js";

export { GET, POST };
```

### 5. Session Provider Setup

Create a session provider for your Next.js app:

```typescript
// frontend/components/session-provider.tsx
'use client';

import { SessionProvider } from "better-auth/react";
import { authClient } from "@/lib/auth-client";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider client={authClient}>
      {children}
    </SessionProvider>
  );
}
```

### 6. Integrate with Root Layout

Update your main layout to include the auth provider:

```typescript
// frontend/app/layout.tsx
import { AuthProvider } from "@/components/session-provider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

### 7. Protect Routes

Create a protected route component:

```typescript
// frontend/components/protected-route.tsx
'use client';

import { useSession } from "better-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: session, isLoading } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !session) {
      router.push('/login');
    }
  }, [session, isLoading, router]);

  if (isLoading || !session) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
}
```

### 8. Update API Client for Authentication

Modify your API client to use Better Auth tokens:

```typescript
// frontend/lib/api.ts
import { authClient } from './auth-client';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private async request(endpoint: string, options: RequestInit = {}) {
    // Get session from Better Auth
    const { data: session } = await authClient.getSession();

    if (!session?.session) {
      throw new Error('Unauthorized: No active session');
    }

    const token = session.session.token;

    // Normalize endpoint
    const baseUrl = BACKEND_URL.replace(/\/$/, '');
    const url = `${baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    console.log(`🚀 API Request: ${options.method || 'GET'} ${url}`);

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        console.warn('Could not parse error response');
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  // ... rest of your API methods
}

export const apiClient = new ApiClient();
```

## Database Schema Integration

If using Drizzle ORM, create the necessary schema:

```typescript
// frontend/lib/auth-schema.ts
import { pgTable, serial, varchar, timestamp, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("user", {
  id: varchar("id").primaryKey().notNull(),
  email: varchar("email").notNull().unique(),
  emailVerified: boolean("email_verified").default(false),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const accounts = pgTable("account", {
  id: serial("id").primaryKey(),
  userId: varchar("user_id").notNull(),
  providerId: varchar("provider_id").notNull(),
  providerAccountId: varchar("provider_account_id").notNull(),
  refreshToken: varchar("refresh_token"),
  accessToken: varchar("access_token"),
  expiresAt: timestamp("expires_at"),
  tokenType: varchar("token_type"),
  scope: varchar("scope"),
  idToken: varchar("id_token"),
  sessionState: varchar("session_state"),
});

Based on our project, create a complete skills using skill-creator-pro, when to use, process steps, output format, and example. and create all in current



export const sessions = pgTable("session", {
  id: varchar("id").primaryKey().notNull(),
  userId: varchar("user_id").notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  ipAddress: varchar("ip_address"),
  userAgent: varchar("user_agent"),
});

export const verification = pgTable("verification", {
  id: varchar("id").primaryKey().notNull(),
  identifier: varchar("identifier").notNull(),
  value: varchar("value").notNull(),
  expiresAt: timestamp("expires_at").notNull(),
});

export const jwks = pgTable("jwks", {
  kid: varchar("kid").primaryKey().notNull(),
  publicKey: varchar("public_key").notNull(),
  privateKey: varchar("private_key").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

## Security Best Practices

1. **Secret Management**: Store `BETTER_AUTH_SECRET` securely in environment variables
2. **HTTPS in Production**: Always use HTTPS for authentication routes
3. **Session Expiration**: Set appropriate session expiration times
4. **Rate Limiting**: Implement rate limiting for auth endpoints
5. **Input Validation**: Validate all inputs on both client and server
6. **CORS Configuration**: Properly configure CORS for auth endpoints

## Testing the Implementation

Create a test component to verify authentication:

```typescript
// frontend/components/auth-test.tsx
'use client';

import { useSession, signIn, signOut } from 'better-auth/react';
import { useState } from 'react';

export function AuthTest() {
  const { data: session, isLoading } = useSession();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="p-4">
      {!session ? (
        <div>
          <h3>Login</h3>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border p-2 mr-2"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border p-2 mr-2"
          />
          <button
            onClick={() => signIn.email({ email, password })}
            className="bg-blue-500 text-white p-2"
          >
            Login
          </button>
          <button
            onClick={() => signIn.social({ provider: 'google' })}
            className="bg-green-500 text-white p-2 ml-2"
          >
            Google Login
          </button>
        </div>
      ) : (
        <div>
          <p>Welcome, {session.user.email}</p>
          <button
            onClick={() => signOut()}
            className="bg-red-500 text-white p-2"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
```

## Common Integration Issues and Solutions

1. **Cross-Origin Issues**: Ensure proper CORS configuration between frontend and backend
2. **Token Synchronization**: Implement proper token refresh mechanisms
3. **Database Sync**: Ensure user data is synchronized between Better Auth and your application
4. **Session Management**: Handle session persistence across page reloads
5. **SSR Compatibility**: Use proper hooks and providers for server-side rendering

## Validation Checklist

- [ ] Better Auth server configured with proper database adapter
- [ ] Environment variables set for both frontend and backend
- [ ] API routes created and accessible
- [ ] Session provider wrapped around application
- [ ] Authentication callbacks tested (login, signup, logout)
- [ ] Protected routes working correctly
- [ ] API calls properly authenticated with tokens
- [ ] Error handling implemented for auth failures
- [ ] Security best practices applied
- [ ] Cross-domain requests properly configured

## References

- Better Auth Documentation: https://better-auth.com/docs
- Database Adapters: https://better-auth.com/docs/database-adapters/overview
- Next.js Integration: https://better-auth.com/docs/frameworks/nextjs
- Security Best Practices: https://better-auth.com/docs/security

This skill provides a comprehensive approach to integrating Better Auth with both frontend and backend systems, ensuring secure authentication with proper session management and token synchronization.