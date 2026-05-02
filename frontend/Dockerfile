# ─── Build stage ──────────────────────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app

# VITE_API_URL se inlinea en el bundle al hacer `vite build`.
# - Default: URL publica del backend en EasyPanel (funciona out-of-the-box).
# - Override: pasar `--build-arg VITE_API_URL=...` para apuntar a otro backend.
ARG VITE_API_URL=https://n8n-nuevo-optimizar-back.3buyoj.easypanel.host
ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ─── Runtime stage (nginx servir static) ──────────────────────────────────────
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
