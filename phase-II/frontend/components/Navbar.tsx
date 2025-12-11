'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { removeToken } from '@/lib/auth';
import { authClient } from '@/lib/auth-client';

interface NavbarProps {
  scrolled: boolean;
  currentPath: string;
}

export default function Navbar({ scrolled, currentPath }: NavbarProps) {
  const [isAuthenticatedUser, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check authentication status on component mount
    const checkAuth = async () => {
      try {
        // Check for JWT token in localStorage (primary auth indicator)
        const jwtToken = localStorage.getItem('jwt_token');

        // Also check Better Auth session
        const session = await authClient.getSession();

        // User is authenticated if EITHER JWT token OR Better Auth session exists
        setIsAuthenticated(!!(jwtToken || session?.session));
      } catch (error) {
        console.error('Error checking auth status:', error);
        // Still check localStorage even if Better Auth fails
        const jwtToken = localStorage.getItem('jwt_token');
        setIsAuthenticated(!!jwtToken);
      }
    };

    checkAuth();

    // Add event listener for storage changes (in case auth state changes from other tabs)
    const handleStorageChange = async () => {
      try {
        const jwtToken = localStorage.getItem('jwt_token');
        const session = await authClient.getSession();
        setIsAuthenticated(!!(jwtToken || session?.session));
      } catch (error) {
        console.error('Error checking auth status on storage change:', error);
        const jwtToken = localStorage.getItem('jwt_token');
        setIsAuthenticated(!!jwtToken);
      }
    };

    // Add focus event to re-check auth state when user returns to the page
    const handleFocus = async () => {
      try {
        const jwtToken = localStorage.getItem('jwt_token');
        const session = await authClient.getSession();
        setIsAuthenticated(!!(jwtToken || session?.session));
      } catch (error) {
        console.error('Error checking auth status on focus:', error);
        const jwtToken = localStorage.getItem('jwt_token');
        setIsAuthenticated(!!jwtToken);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('focus', handleFocus);
    };
  }, []);

  const handleLogout = async () => {
    try {
      // Sign out from Better Auth
      await authClient.signOut();

      // Clear JWT token and user data from localStorage
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('user');

      setIsAuthenticated(false);
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Fallback: clear localStorage even if Better Auth fails
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('user');
      removeToken();
      setIsAuthenticated(false);
      router.push('/login');
    }
  };

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '#about' },
    { name: 'Features', href: '#features' },
    { name: 'Contact', href: '#contact' },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled
        ? 'bg-black/20 backdrop-blur-md border-b border-white/10'
        : 'bg-transparent'
        }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-red-600 to-red-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">T</span>
            </div>
            <span className="text-white font-bold text-xl">TodoPro</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-white/80 hover:text-white transition-colors ${currentPath === link.href ? 'text-white' : ''
                  }`}
              >
                {link.name}
              </Link>
            ))}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            {isAuthenticatedUser ? (
              <>
                <Link
                  href="/todo"
                  className="text-white/80 hover:text-white transition-colors hidden md:block"
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-gradient-to-r from-red-600 to-red-900 text-white px-4 py-2 rounded-lg hover:from-red-700 hover:to-red-950 transition-all duration-300 transform hover:scale-105"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-white/80 hover:text-white transition-colors hidden md:block"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="bg-gradient-to-r from-red-600 to-red-900 text-white px-4 py-2 rounded-lg hover:from-red-700 hover:to-red-950 transition-all duration-300 transform hover:scale-105"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}