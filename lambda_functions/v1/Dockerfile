FROM public.ecr.aws/lambda/python:3.13@sha256:0e5e967eef19c90f871feef21c3e99f7ae62bc575de7314766a376af4c078510 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:0e5e967eef19c90f871feef21c3e99f7ae62bc575de7314766a376af4c078510 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
