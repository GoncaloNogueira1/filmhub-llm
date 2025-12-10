# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production=false

# Copy source and build (VITE_API_BASE_URL must be set at build time)
COPY . .

RUN npm run build

# Production stage
FROM node:20-alpine AS runner

RUN npm install -g serve@14.2.1

WORKDIR /app

COPY --from=builder /app/dist ./dist

EXPOSE 3000

# Serve production build
CMD ["serve", "-s", "dist", "-l", "3000", "--single"]
