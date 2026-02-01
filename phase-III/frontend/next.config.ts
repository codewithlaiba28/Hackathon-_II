import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // No rewrites needed for separated backend/frontend deployment.
  // We rely on NEXT_PUBLIC_API_URL for all backend communication.
  async rewrites() {
    return [];
  },
};

export default nextConfig;
