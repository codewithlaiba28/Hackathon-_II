from fastapi import FastAPI
from .routes import chat
from .middleware.auth_middleware import auth_middleware

app = FastAPI(title="AI Todo Chatbot API", version="1.0.0")

# Add middleware
app.middleware("http")(auth_middleware)

# Include routes
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "AI Todo Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}