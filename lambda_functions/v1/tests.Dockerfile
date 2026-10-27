FROM ghcr.io/astral-sh/uv@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 AS uv
FROM public.ecr.aws/lambda/python:3.14@sha256:fc4e15a5e09e2c9b6184810ea0fdc87afe1c1c734c98cbe27d739a35c3f15e7e AS base

FROM base AS deps

WORKDIR /app

ENV UV_MALWARE_CHECK=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=deps/uv.lock,target=uv.lock \
    --mount=type=bind,source=deps/pyproject.toml,target=pyproject.toml \
    uv export --frozen --group dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target "/app"


FROM base AS runner

COPY /functions/lpa/ ${LAMBDA_TASK_ROOT}/lambda_functions/v1/functions/lpa
COPY /tests/  ${LAMBDA_TASK_ROOT}/lambda_functions/v1/tests
COPY --from=deps /app/ ${LAMBDA_TASK_ROOT}/

RUN echo "2023.7.20250512" > /etc/dnf/vars/releasever && \
    dnf clean all && \
    dnf -y update sqlite-libs libxml2 && \
    dnf clean all

ENV PYTHONPATH "${PYTHONPATH}:${LAMBDA_TASK_ROOT}"

COPY --chmod=755 run-tests.sh run-tests.sh

ENTRYPOINT [ "./run-tests.sh" ]
