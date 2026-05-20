FROM public.ecr.aws/lambda/python:3.13@sha256:3e5bbb3c5f9855cb6156c87bce117f10b334678bcf9a1ac13e2726023ddae14a AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:3e5bbb3c5f9855cb6156c87bce117f10b334678bcf9a1ac13e2726023ddae14a AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
