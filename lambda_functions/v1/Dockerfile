FROM public.ecr.aws/lambda/python:3.13@sha256:549f9348d9f8cddb3d98f60303433a4d2b61d1cbdbde1df60e1299e5e8349de9 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:549f9348d9f8cddb3d98f60303433a4d2b61d1cbdbde1df60e1299e5e8349de9 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
