FROM ghcr.io/astral-sh/uv@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 AS uv
FROM public.ecr.aws/lambda/python:3.14@sha256:51985f11b2fb1949619bda27d121f38ef7d4db64423ca6189ab1d7e632527d27 AS base

FROM base AS build

WORKDIR /app

RUN dnf install -y unzip && \
    curl -L https://github.com/aws-observability/aws-otel-python-instrumentation/releases/download/v0.20.0/layer.zip -o /tmp/otel-layer.zip && \
    echo 'ad69218f4d5ba149ff50a794b785f9b4fa81b8f1d4ebfdbd6a36004a989b2b25  /tmp/otel-layer.zip' | sha256sum -c - && \
    unzip /tmp/otel-layer.zip -d /opt/ && \
    chmod -R 755 /opt/ && \
    rm /tmp/otel-layer.zip && \
    dnf clean all

ENV UV_MALWARE_CHECK=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=lambda_functions/v1/deps/uv.lock,target=uv.lock \
    --mount=type=bind,source=lambda_functions/v1/deps/pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target "/app"

FROM base AS runtime

RUN dnf upgrade -y --releasever=latest && \
    dnf clean all

# Remove python packages from the lambda that we didn't explicitly add
RUN pip uninstall -y -r <(pip freeze)

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}
ENV AWS_LAMBDA_EXEC_WRAPPER=/opt/otel-instrument

COPY --from=build /opt/ /opt/
COPY --from=build /app/ ${LAMBDA_TASK_ROOT}/

COPY lambda_functions/v1/functions/lpa/ ${LAMBDA_TASK_ROOT}

CMD ["app.lpa.lambda_handler"]
