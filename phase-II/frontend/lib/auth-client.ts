import { createAuthClient } from 'better-auth/react';

// Initialize Better Auth client with environment-aware baseURL
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'),
});

export const { useSession, signIn, signUp, signOut } = authClient;
