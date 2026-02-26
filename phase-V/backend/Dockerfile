# Optimized Multi-stage Dockerfile for Todo Backend
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies to a local path
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install runtime dependencies (libpq is needed for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Copy the application code
# IMPORTANT: When building, the root context should contain mcp-servers
# Or mcp-servers should be copied into the backend directory beforehand.
COPY . .

# Expose the API port
EXPOSE 8000

# Metadata
LABEL maintainer="Hackathon Team"
LABEL version="1.0"

# Use uvicorn directly to ensure signal handling (SIGTERM)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]