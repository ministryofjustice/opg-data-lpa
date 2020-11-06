FROM python:alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev && \
    pip install moto[server] && \
    apk del gcc musl-dev libffi-dev openssl-dev


CMD moto_server secretsmanager -H 0.0.0.0 -p 4566

