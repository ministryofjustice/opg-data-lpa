FROM public.ecr.aws/lambda/python:3.13@sha256:33938bc0100013314db321321dd2244ef6dc2921042f5cea6d0c52e78f65dcfc AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:33938bc0100013314db321321dd2244ef6dc2921042f5cea6d0c52e78f65dcfc AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
