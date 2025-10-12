FROM node:23-bookworm AS build

WORKDIR /home/react

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

# Copy build files
COPY --from=build /home/react/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

# Add non-root user
RUN addgroup -S nginxuser && \
    adduser -S -G nginxuser nginxuser

# Create writable directories
RUN mkdir -p /var/cache/nginx /run/nginx && \
    chown -R nginxuser:nginxuser /var/cache/nginx /run/nginx /usr/share/nginx/html

USER nginxuser

EXPOSE 80
STOPSIGNAL SIGQUIT

# Run Nginx
CMD ["nginx", "-g", "daemon off;"]