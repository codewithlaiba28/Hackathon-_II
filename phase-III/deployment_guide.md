# Vercel Deployment Guide - Phase III Todo AI Chatbot

Follow these steps to deploy your application to Vercel. We will use a **dual-project strategy** for the best performance and reliability.

## 🚀 Prerequisite: Database Migration

Vercel filesystem read-only hota hai, isliye **SQLite (`todo_app.db`) kaam nahi karega**.

1. [Neon.tech](https://neon.tech) par ek free account banayein.
2. Ek naya project create karein aur **PostgreSQL Connection String** (`DATABASE_URL`) copy kar lein.
3. Save it somewhere safe - hum isay Vercel mein paste karenge.

---

## 🛠️ Step 1: Backend Deployment (FastAPI)

1. Vercel Dashboard mein **Add New > Project** par click karein.
2. Apna GitHub repo select karein.
3. **Project Settings**:
   - **Project Name**: `todo-api` (ya koi bhi name)
   - **Root Directory**: `phase-III` 
4. **Environment Variables** add karein:
   - `DATABASE_URL`: (Neon Connection String)
   - `CEREBRAS_API_KEY`: (Aapki Cerebras API Key)
   - `BETTER_AUTH_SECRET`: (Aapki Better Auth Secret)
   - `CEREBRAS_BASE_URL`: `https://api.cerebras.ai/v1`
   - `CEREBRAS_MODEL`: `llama3.1-8b`
5. **Deploy** par click karein.
6. Deployment ke baad, **Production URL** copy kar lein (e.g., `https://todo-api.vercel.app`).

---

## 💻 Step 2: Frontend Deployment (Next.js)

1. Vercel Dashboard mein **Add New > Project** par click karein.
2. Dobara wahi GitHub repo select karein.
3. **Project Settings**:
   - **Project Name**: `todo-chat`
   - **Root Directory**: `phase-III/frontend`
   - **Framework Preset**: Next.js
4. **Environment Variables** add karein:
   - `NEXT_PUBLIC_API_URL`: (Step 1 wali Backend URL - e.g., `https://todo-api.vercel.app`)
   - `DATABASE_URL`: (Wahi Neon Connection String)
   - `BETTER_AUTH_SECRET`: (Wahi Better Auth Secret)
   - `BETTER_AUTH_URL`: (Aapki is project ki URL - e.g., `https://todo-chat.vercel.app`)
5. **Deploy** par click karein.

---

## 🧪 Verification

1. **Backend Health Check**:
   `https://todo-api.vercel.app/api/health` par jayein. Agar `{"status": "healthy"}` nazar aa raha hai, to backend set hai!

2. **Chat Testing**:
   Frontend URL par jayein, login/signup karein aur chatbot se baatein karke dekhein. Try: "Add a task to buy groceries".

---

## ⚠️ Important Troubleshooting

- **CORS Errors**: Agar frontend backend ko call nahi kar pa raha, to verify karein ke Step 1 ki API URL `NEXT_PUBLIC_API_URL` mein sahi hai aur `https://` include hai.
- **Database Connection**: Neon dashboard mein check karein ke connections aa rahe hain ya nahi.
- **Auth Logout**: Agar session persist nahi ho raha, check karein ke `BETTER_AUTH_URL` aur `BETTER_AUTH_SECRET` dono projects mein identical hain.

---

**Status**: ✅ **Configurations Ready!** Aap ab deploy kar sakte hain. 🚀
