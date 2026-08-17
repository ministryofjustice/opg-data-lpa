FROM ghcr.io/astral-sh/uv@sha256:b46b03ddfcfbf8f547af7e9eaefdf8a39c8cebcba7c98858d3162bd28cf536f6 AS uv

FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS build

WORKDIR /app

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

FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS runtime

RUN dnf upgrade -y --releasever=latest && \
    dnf clean all

COPY --from=build /app/ ${LAMBDA_TASK_ROOT}/

COPY lambda_functions/v1/functions/lpa/ ${LAMBDA_TASK_ROOT}

CMD ["app.lpa.lambda_handler"]
