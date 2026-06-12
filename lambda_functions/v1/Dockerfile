FROM public.ecr.aws/lambda/python:3.13@sha256:c669775f97d10613b96c7b03a6e7ac9507313c7359d19639b21d15feedf9c188 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:c669775f97d10613b96c7b03a6e7ac9507313c7359d19639b21d15feedf9c188 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
