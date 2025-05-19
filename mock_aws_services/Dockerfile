FROM python:alpine

RUN apk add --no-cache gcc rust cargo musl-dev libffi-dev openssl-dev && \
    pip install moto[server] && \
    apk del gcc rust cargo musl-dev libffi-dev openssl-dev && \
    apk update && \
    apk upgrade --no-cache


CMD moto_server secretsmanager -H 0.0.0.0 -p 4566

