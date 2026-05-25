FROM public.ecr.aws/lambda/python:3.13@sha256:1615c5e9eb6756a41a76e10821ac5c56531fc15ac9051dd541a9acf860549416 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:1615c5e9eb6756a41a76e10821ac5c56531fc15ac9051dd541a9acf860549416 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
