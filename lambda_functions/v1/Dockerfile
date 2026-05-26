FROM public.ecr.aws/lambda/python:3.13@sha256:a38d4baf1ad679e45834753aa19fa0885e3521c5446af0d4bd99a4b0212bd3d8 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:a38d4baf1ad679e45834753aa19fa0885e3521c5446af0d4bd99a4b0212bd3d8 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
