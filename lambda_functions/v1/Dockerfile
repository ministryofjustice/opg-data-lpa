FROM public.ecr.aws/lambda/python:3.13@sha256:f769f1f81b8ee38c2e09130a7f2e3c2a3643eba3e48ec15a6f93fb6f44947254 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:f769f1f81b8ee38c2e09130a7f2e3c2a3643eba3e48ec15a6f93fb6f44947254 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
