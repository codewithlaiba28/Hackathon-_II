import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    typescript: {
        ignoreBuildErrors: true,
    },
    eslint: {
        ignoreDuringBuilds: true,
    },
    async rewrites() {
        // Determine the internal API URL, fallback to backend service in K8s
        const internalApiUrl = process.env.INTERNAL_API_URL || 'http://todo-app-backend:80/api';
        return {
            beforeFiles: [
                {
                    // Exclude /api/auth from being proxied to backend
                    // This ensures better-auth handles these routes locally
                    source: '/api/:path((?!auth(?:/|$)).*)',
                    destination: `${internalApiUrl}/:path*`,
                },
            ],
        };
    },
};

export default nextConfig;
