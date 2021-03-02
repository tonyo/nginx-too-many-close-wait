FROM nginx:1.19.7

RUN apt update && apt install -y procps net-tools

RUN rm -rf /etc/nginx/conf.d/*
COPY nginx.conf /etc/nginx/nginx.conf
