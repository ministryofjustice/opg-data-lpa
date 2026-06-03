FROM public.ecr.aws/lambda/python:3.13@sha256:c1454ec7a9804db34e079acab0470a326604d4dfad6c39a05eea3ba5daf07298 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:c1454ec7a9804db34e079acab0470a326604d4dfad6c39a05eea3ba5daf07298 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
