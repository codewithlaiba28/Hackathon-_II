# Elite Docker Patterns for Microservices

To build reliable and performant distributed systems, your container strategy must focus on size, security, and build-time configuration.

## 1. Multi-Stage Builds (The "Gold Standard")
Always separate the build environment from the runtime environment.

```dockerfile
# BUILDER STAGE
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# RUNTIME STAGE
FROM python:3.11-slim
WORKDIR /app
# Only copy the installed dependencies from the builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Copy only necessary code files
COPY main.py .
COPY database.py .
# ...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## 2. Handling Build Arguments (Baking in URLs)
For frontend apps (like Next.js), API URLs must often be baked in at build time.

```dockerfile
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build
```

## 3. Signal Handling and Graceful Shutdown
Ensure your application can catch `SIGTERM` from Kubernetes.
- **Python/Uvicorn**: Use `@app.on_event("shutdown")` or the `lifespan` context manager.
- **Docker**: Avoid using `ENTRYPOINT ["sh", "-c", "uvicorn ..."]` because shell doesn't pass signals. Use `ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]` instead.

## 4. Layer Scoping
Keep frequently changing files (like your logic) at the bottom of the Dockerfile. Keep stable files (like `package.json` or `requirements.txt`) at the top. This maximizes Docker's layer cache and reduces build times from minutes to seconds.
