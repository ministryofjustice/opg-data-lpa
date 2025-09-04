FROM python:alpine@sha256:9ba6d8cbebf0fb6546ae71f2a1c14f6ffd2fdab83af7fa5669734ef30ad48844

RUN apk add --no-cache gcc rust cargo musl-dev libffi-dev openssl-dev && \
    pip install moto[server] && \
    apk del gcc rust cargo musl-dev libffi-dev openssl-dev


CMD moto_server secretsmanager -H 0.0.0.0 -p 4566

