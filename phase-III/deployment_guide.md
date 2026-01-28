# 🚀 Complete Vercel Deployment Setup (Monorepo)

This guide provide the ONE-CLICK deployment setup for Phase III. By using the root `vercel.json`, both your Frontend (Next.js) and Backend (FastAPI) will live in the same project.

## 🛠️ Step 1: Database Setup (Neon PostgreSQL)
Vercel is stateless; SQLite won't save your data.
1. Create a free project at [Neon.tech](https://neon.tech).
2. Copy your **Connection String**:
   `postgresql://user:pass@ep-cool-name.us-east-1.aws.neon.tech/neondb?sslmode=require`
3. **Important**: Ensure `?sslmode=require` is at the end.

## 🛠️ Step 2: Vercel Project Configuration
1. Go to [Vercel](https://vercel.com/dashboard) -> **Add New** -> **Project**.
2. Select your GitHub Repository.
3. **Configure Project**:
   - **Framework Preset**: `Next.js` (Vercel will detect it).
   - **Root Directory**: `phase-III` (This is crucial, set it to the root of Phase III).
4. **Environment Variables**: Add these exact keys:

| Variable | Recommended Value |
|----------|-------|
| `DATABASE_URL` | Your Neon Connection String |
| `CEREBRAS_API_KEY` | Your Cerebras API Key |
| `BETTER_AUTH_SECRET` | A random 32-character string |
| `BETTER_AUTH_URL` | `https://your-app-name.vercel.app` |
| `NEXT_PUBLIC_API_URL` | `https://your-app-name.vercel.app` (Same as above) |

## 🛠️ Step 3: Deployment
1. Click **Deploy**.
2. Vercel will build your Next.js frontend and your FastAPI backend simultaneously.

---

## ✅ Post-Deployment Checklist
- [ ] **Health Check**: Visit `https://your-app.vercel.app/api/health`. Should return `{"status": "healthy"}`.
- [ ] **Auth Sync**: Log in/Sign up. If it works, Better Auth is correctly hitting Neon.
- [ ] **Chat Speed**: Type "Add task 'Finish Hackathon'". You should see the response **stream** in instantly.

---

## 🔧 Why this works (The Setup)
- **Unified Routing**: The root `vercel.json` routes `/api/(.*)` to the Python backend and everything else to Next.js.
- **Stateless Persistence**: All data (Tasks, Conversations, Messages) is stored in Neon, so server restarts won't lose history.
- **CORS-Free**: Since both live on the same domain, you won't face CORS "Failed to fetch" errors.

> [!TIP]
> **Proactive Troubleshooting**: If you see "Internal Server Error", check the Vercel **Function Logs**. Most likely the `DATABASE_URL` is missing the SSL parameter.
