FROM public.ecr.aws/lambda/python:3.13@sha256:ec6c95a0dfa2e05c011a49ebff36f06642522f05f6a9281e6f89df6ddc2366d4 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:ec6c95a0dfa2e05c011a49ebff36f06642522f05f6a9281e6f89df6ddc2366d4 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
