FROM public.ecr.aws/lambda/python:3.13@sha256:a7f9e29cd3900d6cc3461457e585f857604219f339003d8f7bb17786951c41a3 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:a7f9e29cd3900d6cc3461457e585f857604219f339003d8f7bb17786951c41a3 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
