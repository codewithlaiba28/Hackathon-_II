import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    // Use NEXT_PUBLIC_API_URL for production, fallback to localhost for development
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

    return [
      {
        // Proxy all /api requests to the backend, EXCEPT those belonging to the frontend
        // This avoids CORS issues by making backend calls same-origin
        source: '/api/:path((?!auth|proxy|token).*)',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
