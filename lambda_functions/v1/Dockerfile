FROM public.ecr.aws/lambda/python:3.13@sha256:5b6484af58c9c6a1d6626c7d32275d0f439be3a3f9c221a0966ca4f930be13c0 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:5b6484af58c9c6a1d6626c7d32275d0f439be3a3f9c221a0966ca4f930be13c0 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
