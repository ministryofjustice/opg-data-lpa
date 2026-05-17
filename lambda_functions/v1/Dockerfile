FROM public.ecr.aws/lambda/python:3.13@sha256:fb9ece3f1ae89c5911f74d05011ba2cd1666eec8b4e2536422352af41528ec50 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:fb9ece3f1ae89c5911f74d05011ba2cd1666eec8b4e2536422352af41528ec50 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
