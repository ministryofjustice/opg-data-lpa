FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS build

COPY --from=ghcr.io/astral-sh/uv@sha256:df4cae8f3a96d175e2e5f992e597550000edbe78fdc2594d5cd8de1a217f504c /uv /uvx /bin/

WORKDIR /app
COPY lambda_functions/v1/deps/pyproject.toml lambda_functions/v1/deps/uv.lock ./
RUN uv export --frozen --no-dev -o requirements.txt

FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS runtime

RUN dnf upgrade -y --releasever=latest && \
    dnf clean all

COPY --from=build /app/requirements.txt requirements.txt
RUN python -m pip install --target "${LAMBDA_TASK_ROOT}" --requirement requirements.txt

COPY lambda_functions/v1/functions/lpa/ ${LAMBDA_TASK_ROOT}

CMD ["app.lpa.lambda_handler"]
