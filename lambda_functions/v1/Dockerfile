FROM public.ecr.aws/lambda/python:3.13@sha256:c1c48889a63cda891a315702c08bb197d0dad4581a0f5c2e66c4f264b0662dc1 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:c1c48889a63cda891a315702c08bb197d0dad4581a0f5c2e66c4f264b0662dc1 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
