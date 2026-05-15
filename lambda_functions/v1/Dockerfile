FROM public.ecr.aws/lambda/python:3.13@sha256:a03c72a756eb9aef9d55ced9f6d4105febf44e8a24ede73735485b7359319936 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:a03c72a756eb9aef9d55ced9f6d4105febf44e8a24ede73735485b7359319936 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
