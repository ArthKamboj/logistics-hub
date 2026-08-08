FROM node:20-alpine AS base


FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci


FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_PUBLIC_API_URL=http://localhost:8000
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]