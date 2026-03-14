FROM node:20-alpine

WORKDIR /app

COPY mcp/package.json mcp/package-lock.json ./
RUN npm ci --production

COPY mcp/dist/ ./dist/
COPY prompts/ ./prompts/

CMD ["node", "dist/index.js"]
