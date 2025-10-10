FROM node:18.20.8-slim AS builder

COPY ./frontend /app/loonflow/
WORKDIR /app/loonflow
RUN yarn install && yarn build


FROM nginx:1.24.0-alpine
LABEL maintainer=blackholll@163.com

COPY docker_compose_deploy/loonflow-ui/nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /app/loonflow/build/ /usr/share/nginx/html/

RUN mkdir /var/log/loonflow/
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
