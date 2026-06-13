FROM public.ecr.aws/lambda/python:3.13@sha256:19c22cb947cec643605f2e6263fb6ef45f9b1bce4dc497df5591dfbe98b2de6d AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:19c22cb947cec643605f2e6263fb6ef45f9b1bce4dc497df5591dfbe98b2de6d AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
