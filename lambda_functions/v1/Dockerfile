FROM public.ecr.aws/lambda/python:3.13@sha256:a64c11b6b710a3babeb0be218f4f29dd83ba58f8b3644345459bd45ecd02e963 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:a64c11b6b710a3babeb0be218f4f29dd83ba58f8b3644345459bd45ecd02e963 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
