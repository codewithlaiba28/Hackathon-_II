# Optimized Multi-stage Dockerfile for Next.js Frontend
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Install compatibility libraries
RUN apk add --no-cache libc6-compat

# Copy package files (using npm as package-lock.json is present)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL
ARG BETTER_AUTH_SECRET
ENV BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET
ARG BETTER_AUTH_URL
ENV BETTER_AUTH_URL=$BETTER_AUTH_URL
ARG NEXT_PUBLIC_BASE_URL
ENV NEXT_PUBLIC_BASE_URL=$NEXT_PUBLIC_BASE_URL

# Build the Next.js app
# NEXT_PRIVATE_BUILD_WORKERS=1 helps prevent OOM in resource-constrained environments
# NEXT_OTEL_FETCH_DISABLED=1 can also help speed up builds
RUN NEXT_PRIVATE_BUILD_WORKERS=1 npm run build

# Stage 2: Runtime
FROM node:20-alpine AS runtime

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy necessary runtime files from builder
# We include next.config.ts and public folder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/next.config.ts ./next.config.ts

# Set ownership to non-root user
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose Next.js port
EXPOSE 3000

# Standard environment variables
ENV NODE_ENV=production
ENV PORT=3000
# NEXT_TELEMETRY_DISABLED should be 1 to speed up builds and avoid privacy issues
ENV NEXT_TELEMETRY_DISABLED=1

# Start the application
CMD ["npm", "start"]