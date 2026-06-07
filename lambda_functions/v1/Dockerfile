FROM public.ecr.aws/lambda/python:3.13@sha256:f48813386e87ea5be92aa57844fb90f5a9db618ffd3a6fee86d432497cd787b4 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:f48813386e87ea5be92aa57844fb90f5a9db618ffd3a6fee86d432497cd787b4 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
