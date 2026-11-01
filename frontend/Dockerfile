# Development image for Next.js (production multi-stage image comes in Phase 7).
FROM node:20-alpine

WORKDIR /app

# Install dependencies first so this layer is cached until package*.json change.
COPY package.json package-lock.json* ./
RUN npm install --fetch-retries=5 --fetch-timeout=120000

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]

