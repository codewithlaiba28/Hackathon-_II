import { useState, useEffect } from 'react';
import { createAuthClient } from 'better-auth/react';
import { auth } from './better-auth';

// Initialize Better Auth client
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
  fetch: globalThis.fetch,
});

// React hook to manage authentication state
export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check current session on component mount
    const checkSession = async () => {
      try {
        const session = await authClient.getSession();
        if (session?.session) {
          setIsAuthenticated(true);
          setUser(session.user);
        } else {
          setIsAuthenticated(false);
          setUser(null);
        }
      } catch (error) {
        console.error('Error checking session:', error);
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  return { isAuthenticated, user, loading, setIsAuthenticated, setUser };
};
