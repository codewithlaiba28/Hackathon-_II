import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { jwt } from 'better-auth/plugins';
import { db } from './db';
import * as schema from './auth-schema';

export const auth = betterAuth({
    database: drizzleAdapter(db, {
        provider: 'pg',
        schema: {
            user: schema.user,
            session: schema.session,
            account: schema.account,
            verification: schema.verification,
            jwks: schema.jwks,
        },
    }),
    // Base URL is REQUIRED for production deployments
    baseURL: process.env.BETTER_AUTH_URL || (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'),
    // Trusted origins for CORS
    trustedOrigins: [
        process.env.BETTER_AUTH_URL || 'http://localhost:3000',
        process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    ],
    secret: process.env.BETTER_AUTH_SECRET,
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
    },
    plugins: [
        jwt({
            jwt: {
                expirationTime: '7d',
            },
        }),
    ],
});
