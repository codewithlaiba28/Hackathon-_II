---
name: deployment-production-config
description: Deploy full-stack applications with ChatKit, configure environment variables, set up domain allowlists, deploy to Vercel and cloud platforms, and implement proper security and monitoring
---

### Purpose
Take applications from development to production with proper configuration, security, and deployment practices.

### When to Use
- Deploying full-stack applications
- Configuring production environments
- Setting up domain security
- Implementing monitoring and logging

### Core Competencies

**1. Environment Configuration**
- Set up environment variables for all secrets
- Configure OpenAI API keys
- Manage database connection strings
- Set JWT secret keys
- Handle domain allowlist configuration

**2. Frontend Deployment (Vercel)**
- Deploy Next.js applications
- Configure environment variables in Vercel
- Set up custom domains
- Enable HTTPS automatically
- Configure build settings

**3. Backend Deployment**
- Deploy FastAPI to cloud platforms
- Configure production database connections
- Set up logging and monitoring
- Handle graceful shutdowns
- Implement health check endpoints

**4. OpenAI ChatKit Production Setup**
- Add domains to OpenAI allowlist
- Generate domain keys
- Configure production ChatKit settings
- Handle CORS properly
- Test production deployments

**5. Security Configuration**
- Use environment variables for secrets
- Enable HTTPS everywhere
- Configure CORS policies
- Implement rate limiting
- Set up security headers

**6. Monitoring & Logging**
- Implement application logging
- Set up error tracking (Sentry)
- Monitor API performance
- Track database queries
- Alert on failures

### Implementation Guidelines

**Environment Variables Structure**

```bash
# Frontend (.env.local for development, Vercel for production)
NEXT_PUBLIC_OPENAI_API_KEY=sk-proj-xxx
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=dk-xxx  # Production only
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
BETTER_AUTH_SECRET=your-secret-key
DATABASE_URL=postgresql://...

# Backend (.env for development, platform settings for production)
BETTER_AUTH_SECRET=your-secret-key  # MUST match frontend
DATABASE_URL=postgresql://neon-connection-string
OPENAI_API_KEY=sk-xxx
ENVIRONMENT=production
LOG_LEVEL=info
```

**Vercel Deployment**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Set environment variables
vercel env add NEXT_PUBLIC_OPENAI_API_KEY production
vercel env add BETTER_AUTH_SECRET production
vercel env add DATABASE_URL production

# Deploy to production
vercel --prod
```

**Docker Backend Deployment**

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Health Check Endpoint**

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_session)):
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        db.exec(select(1))
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }, 503
```

**OpenAI Domain Allowlist Setup**

1. Deploy frontend first to get URL
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Click "Add domain"
4. Enter production URL (e.g., `https://yourapp.vercel.app`)
5. Save and copy the domain key
6. Add domain key to environment variables

**Production Logging**

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    logger.info(f"{request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(f"Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise
```

### Deployment Checklist

**Pre-Deployment**
- [ ] All environment variables documented
- [ ] Database migrations tested
- [ ] API endpoints tested
- [ ] Authentication working
- [ ] Error handling implemented
- [ ] Logging configured

**Deployment**
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to cloud platform
- [ ] Database created on Neon
- [ ] Environment variables set
- [ ] Domain allowlist configured
- [ ] HTTPS enabled

**Post-Deployment**
- [ ] Health checks passing
- [ ] Test authentication flow
- [ ] Test chatbot functionality
- [ ] Monitor logs for errors
- [ ] Set up alerting
- [ ] Document deployment process

### Resources
- Vercel Deployment Guide
- FastAPI Production Best Practices
- OpenAI ChatKit Production Setup

---
