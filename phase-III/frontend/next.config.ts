import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        // Proxy all /api requests to the backend, EXCEPT those belonging to the frontend
        // This avoids CORS issues by making backend calls same-origin
        source: '/api/:path((?!auth|proxy|token).*)',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
