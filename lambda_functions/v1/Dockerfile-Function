FROM public.ecr.aws/lambda/python:3.13@sha256:38d3ac05ffdf36bff2d2edc8860221b67a94256914a4346c5d783637091a23c3 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:38d3ac05ffdf36bff2d2edc8860221b67a94256914a4346c5d783637091a23c3 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
