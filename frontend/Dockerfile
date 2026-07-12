# Stage 1 — Build Vue
FROM node:20-slim AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Removed hardcoded VITE_API_URL override to use actual .env file
RUN npm run build

# Stage 2 — Serve pakai Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80