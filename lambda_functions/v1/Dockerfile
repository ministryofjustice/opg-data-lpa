FROM public.ecr.aws/lambda/python:3.13@sha256:9eb2a3f2166cd62588dc63e24d1a61047072f9a3436e958904109426251d69c3 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:9eb2a3f2166cd62588dc63e24d1a61047072f9a3436e958904109426251d69c3 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
