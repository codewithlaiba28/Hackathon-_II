import { betterAuth } from 'better-auth';

// Better Auth WITHOUT database - uses session tokens only
// This eliminates all database adapter errors
export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET || 'c4f04665bdfd926af97a01aa5b67bf76',
    // NO DATABASE CONFIG - Better Auth will use stateless sessions
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
    },
});
