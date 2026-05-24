FROM public.ecr.aws/lambda/python:3.13@sha256:278e37350e7308e98001c355a8526186b47300dbdd5fcb0e24a6ed92570e9d4a AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:278e37350e7308e98001c355a8526186b47300dbdd5fcb0e24a6ed92570e9d4a AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
