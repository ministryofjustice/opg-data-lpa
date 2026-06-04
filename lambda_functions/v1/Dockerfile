FROM public.ecr.aws/lambda/python:3.13@sha256:899f05ee2ac63bf38b2a42053981dba678cba9866ed7ec9de6c70a3e7646f1d7 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:899f05ee2ac63bf38b2a42053981dba678cba9866ed7ec9de6c70a3e7646f1d7 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
