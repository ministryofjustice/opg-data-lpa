FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS build

COPY --from=ghcr.io/astral-sh/uv@sha256:77280f2f771df71f90786c314fe1bbc1e023feac652969bbf139c280babf2eb7 /uv /uvx /bin/

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
