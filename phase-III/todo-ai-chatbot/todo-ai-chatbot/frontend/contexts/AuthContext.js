// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock authentication - in a real app, this would connect to Better Auth
  useEffect(() => {
    // Simulate checking for existing auth session
    const checkAuth = async () => {
      try {
        // In a real implementation, this would call the backend auth API
        // For now, we'll simulate a user being logged in
        const mockUser = {
          id: 'user-123',
          email: 'user@example.com',
          name: 'Demo User'
        };
        setUser(mockUser);
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    // In a real app, this would call the backend login API
    const mockUser = {
      id: 'user-123',
      email,
      name: email.split('@')[0]
    };
    setUser(mockUser);
    return mockUser;
  };

  const logout = async () => {
    // In a real app, this would call the backend logout API
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};