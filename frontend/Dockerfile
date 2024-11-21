FROM node:23-bookworm AS build

WORKDIR /home/react

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

# Copy  build files
COPY --from=build /home/react/build /usr/share/nginx/html

# Add non-root user
RUN addgroup -S nginxuser && \
    adduser -S -G nginxuser nginxuser
RUN chown -R nginxuser:nginxuser /usr/share/nginx/html

# Set ownership and permissions for cache directories
RUN mkdir -p /var/cache/nginx && \
    chown -R nginxuser:nginxuser /var/cache/nginx

USER nginxuser

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]