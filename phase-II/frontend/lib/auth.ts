// lib/auth.ts
import { authClient } from './auth-client';

// Get token from custom auth client
export const getToken = async (): Promise<string | null> => {
  if (typeof window !== 'undefined') {
    const session = await authClient.getSession();
    const token = session?.session?.token || null;
    console.log('Retrieved token from custom auth session:', token ? `${token.substring(0, 10)}...` : 'null');
    return token;
  }
  console.log('Window is not defined, returning null for token');
  return null;
};

// Remove token from custom auth client
export const removeToken = async (): Promise<void> => {
  if (typeof window !== 'undefined') {
    console.log('Removing token from custom auth session');
    try {
      await authClient.signOut();
    } catch (error) {
      console.error('Error during signOut:', error);
      // Fallback to localStorage cleanup if signOut fails
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    }
  } else {
    console.log('Window is not defined, cannot remove token');
  }
};

// Check if user is authenticated
export const isAuthenticated = async (): Promise<boolean> => {
  const token = await getToken();
  return token !== null;
};