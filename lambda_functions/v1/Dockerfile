FROM public.ecr.aws/lambda/python:3.13@sha256:a452c076b15eef38cc0a7fc020d32b2b4d6964436d90c648e363acef6656c56e AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:a452c076b15eef38cc0a7fc020d32b2b4d6964436d90c648e363acef6656c56e AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
