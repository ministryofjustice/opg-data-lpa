FROM public.ecr.aws/lambda/python:3.13@sha256:c21f77540024d0f2043362aba786ab03ec3d1b26de94a987a8ad1461e8e1c797 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:c21f77540024d0f2043362aba786ab03ec3d1b26de94a987a8ad1461e8e1c797 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
