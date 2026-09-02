FROM node:24-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci && npm prune --omit=dev

COPY server.js ./

FROM node:24-alpine AS production

WORKDIR /app

COPY --from=builder --chown=node:node /app/package*.json ./
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/server.js ./

USER node
EXPOSE 3000

CMD ["npm", "start"]
