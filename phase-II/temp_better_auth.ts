import { betterAuth } from 'better-auth';

// Better Auth configuration that will work with our FastAPI backend
export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET || 'c4f04665bdfd926af97a01aa5b67bf76',
    database: {
        provider: 'sqlite',
        url: process.env.DATABASE_URL || './auth.db',
    },
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
    },
    // Hooks to synchronize with our FastAPI backend
    hooks: {
        after: [
            {
                // When a user signs up in Better Auth, sync with our backend
                event: "signUp",
                handler: async (ctx) => {
                    // Make request to our FastAPI backend to sync the user
                    try {
                        const response = await fetch(`${'${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}`}/api/auth/sync-better-auth-user`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                email: ctx.user.email,
                                name: ctx.user.name || ctx.user.email.split('@')[0]
                            })
                        });

                        if (!response.ok) {
                            console.error('Failed to sync user with backend:', await response.text());
                        }
                    } catch (error) {
                        console.error('Error syncing user with backend:', error);
                    }
                }
            },
            {
                // When a user signs in, make sure they exist in our backend
                event: "signIn",
                handler: async (ctx) => {
                    // Check if user exists in our backend, if not create them
                    // For now, we'll just log in to our backend
                    try {
                        // We can't get the plain password here, so we'll need to handle this differently
                        // This is a limitation of the approach - let's handle it at the frontend level
                    } catch (error) {
                        console.error('Error during sign in sync:', error);
                    }
                }
            }
        ]
    }
});
