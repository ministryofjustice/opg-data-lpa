FROM public.ecr.aws/lambda/python:3.13@sha256:707eb125244dbc708baa32968d7a743d8ad523d1feb5e64039447ac02870b892 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:707eb125244dbc708baa32968d7a743d8ad523d1feb5e64039447ac02870b892 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
