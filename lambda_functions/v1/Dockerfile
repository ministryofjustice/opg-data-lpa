FROM public.ecr.aws/lambda/python:3.13@sha256:338b7ff55c42151b5ba08142654cf6cb55fe71a79d093d99bfeac019c8083612 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:338b7ff55c42151b5ba08142654cf6cb55fe71a79d093d99bfeac019c8083612 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
