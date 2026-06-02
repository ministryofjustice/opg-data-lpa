FROM public.ecr.aws/lambda/python:3.13@sha256:dc9fe7159c5cb0334a804d686ab701a176d07ea2ac2e82028728cb7f30b5bbb7 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:dc9fe7159c5cb0334a804d686ab701a176d07ea2ac2e82028728cb7f30b5bbb7 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
