FROM public.ecr.aws/lambda/python:3.13@sha256:536cd2f64c41dede36aa5fcf82dbbfefbef75db178ff4eb631ad0f07bd4e935f AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:536cd2f64c41dede36aa5fcf82dbbfefbef75db178ff4eb631ad0f07bd4e935f AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
