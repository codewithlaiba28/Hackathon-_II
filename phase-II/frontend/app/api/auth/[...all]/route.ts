import { auth } from '../../../../lib/better-auth';

import { toNextJsHandler } from "better-auth/next-js";

// Force Node.js runtime (required for better-sqlite3)
// Edge runtime doesn't support native modules like better-sqlite3
export const runtime = 'nodejs';

// This API route will handle Better Auth endpoints
export const { GET, POST } = toNextJsHandler(auth);