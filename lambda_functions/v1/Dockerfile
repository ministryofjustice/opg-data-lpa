FROM public.ecr.aws/lambda/python:3.13@sha256:ba32ff42fc0c694aa03f7136c4fefb94e34eadefb1934305f111614064e2202c AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:ba32ff42fc0c694aa03f7136c4fefb94e34eadefb1934305f111614064e2202c AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
