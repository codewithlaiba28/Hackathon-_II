import { auth } from '@/lib/better-auth';
import { toNextJsHandler } from "better-auth/next-js";

// Force Node.js runtime and dynamic behavior
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

// This API route will handle Better Auth endpoints
export const { GET, POST } = toNextJsHandler(auth.handler);
