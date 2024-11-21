FROM node:23-bookworm AS build

WORKDIR /home/react

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /home/react/build /usr/share/nginx/html

RUN addgroup -S nginxuser && adduser -S -G nginxuser nginxuser
RUN chown -R nginxuser:nginxuser /usr/share/nginx/html
USER nginxuser

CMD ["nginx", "-g", "daemon off;"]