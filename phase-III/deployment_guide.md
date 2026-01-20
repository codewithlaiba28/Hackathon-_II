# Vercel Deployment Guide - Phase III Todo AI Chatbot

This guide provides step-by-step instructions for deploying the Todo AI Chatbot. We use a **dual-project strategy**: one Vercel project for the FastAPI backend and another for the Next.js frontend.

## 🚀 Prerequisite: Database Setup

Vercel functions are stateless and the filesystem is read-only. **SQLite will not work**.
1. Create a free PostgreSQL database on [Neon.tech](https://neon.tech).
2. Copy the **Connection String** (e.g., `postgresql://user:pass@ep-cool-name.us-east-2.aws.neon.tech/neondb?sslmode=require`).
3. You will use this as `DATABASE_URL` in both projects.

---

## 🛠️ Step 1: Backend Deployment (FastAPI)

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New > Project**.
2. Connect your GitHub repository.
3. **Configure Project**:
   - **Project Name**: `todo-api`
   - **Root Directory**: `phase-III` (Vercel will detect `vercel.json` and `backend/main.py`)
4. **Environment Variables**:
   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | Your Neon Connection String |
   | `CEREBRAS_API_KEY` | Your Cerebras API Key |
   | `BETTER_AUTH_SECRET` | A random 32-character string |
   | `CEREBRAS_BASE_URL` | `https://api.cerebras.ai/v1` |
   | `CEREBRAS_MODEL` | `llama3.1-8b` |
5. Click **Deploy**.
6. Once deployed, note your **Production URL** (e.g., `https://todo-api.vercel.app`).

---

## 💻 Step 2: Frontend Deployment (Next.js)

1. Go to Vercel Dashboard again and click **Add New > Project**.
2. Select the **same** GitHub repository.
3. **Configure Project**:
   - **Project Name**: `todo-chat`
   - **Root Directory**: `phase-III/frontend`
   - **Framework Preset**: Next.js
4. **Environment Variables**:
   | Variable | Value |
   |----------|-------|
   | `NEXT_PUBLIC_API_URL` | `https://todo-api.vercel.app` (From Step 1) |
   | `DATABASE_URL` | Your Neon Connection String |
   | `BETTER_AUTH_SECRET` | Same string used in Step 1 |
   | `BETTER_AUTH_URL` | `https://todo-chat.vercel.app` (This project's URL) |
5. Click **Deploy**.

---

## 🧪 Verification & Health Check

1. **Backend**: Visit `https://todo-api.vercel.app/api/health`. Should return `{"status": "healthy"}`.
2. **Database**: The app will automatically create tables on first run. 
3. **Frontend**: Open your frontend URL, sign up, and try adding a task via the chatbot.

---

## ⚠️ Troubleshooting

- **CORS Errors**: Ensure `NEXT_PUBLIC_API_URL` in the frontend setup matches the backend URL exactly (with `https://` and no trailing slash).
- **Infinite Loading**: Check if the `DATABASE_URL` includes `?sslmode=require`. Neon requires SSL for connections from Vercel.
- **Auth Issues**: Ensure `BETTER_AUTH_SECRET` is identical in both projects.
