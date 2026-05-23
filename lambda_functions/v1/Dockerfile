FROM public.ecr.aws/lambda/python:3.13@sha256:55be4d8261ca560bbd114fa54df20fa68421c56956a485ae30f31a7c2651887d AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:55be4d8261ca560bbd114fa54df20fa68421c56956a485ae30f31a7c2651887d AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
