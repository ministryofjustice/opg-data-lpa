FROM ghcr.io/astral-sh/uv@sha256:606e70c71c852d03f611b1e56a195d08648507018a7057fab82c4974c4eae105 AS uv

FROM public.ecr.aws/lambda/python:3.13@sha256:0fddf7542198843bd5a488b17e35473659fdf69f0788c7b3563f0231edf3384d AS build

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

FROM public.ecr.aws/lambda/python:3.13@sha256:0fddf7542198843bd5a488b17e35473659fdf69f0788c7b3563f0231edf3384d AS runtime

RUN dnf upgrade -y --releasever=latest && \
    dnf clean all

# Remove python packages from the lambda that we didn't explicitly add
RUN pip uninstall -y -r <(pip freeze)

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

COPY --from=build /app/ ${LAMBDA_TASK_ROOT}/

COPY lambda_functions/v1/functions/lpa/ ${LAMBDA_TASK_ROOT}

CMD ["app.lpa.lambda_handler"]
