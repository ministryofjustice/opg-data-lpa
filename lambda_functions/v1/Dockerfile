FROM public.ecr.aws/lambda/python:3.13@sha256:6b953badffa37f39801b5fa8e873af7fba78871207072cac746b0cbc46d5a0f5 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:6b953badffa37f39801b5fa8e873af7fba78871207072cac746b0cbc46d5a0f5 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
