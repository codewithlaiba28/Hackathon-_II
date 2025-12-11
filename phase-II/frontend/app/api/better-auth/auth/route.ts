// frontend/app/api/better-auth/auth/route.ts
import { auth } from '@/lib/better-auth';
import { GET, POST } from 'better-auth/next-js';

export const { GET, POST } = auth;