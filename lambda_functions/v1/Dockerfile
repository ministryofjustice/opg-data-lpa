FROM public.ecr.aws/lambda/python:3.13@sha256:7b163711d34f9a6d687da388afa5659ea42cb5990deb7b38a7abb09829f08f9e AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:7b163711d34f9a6d687da388afa5659ea42cb5990deb7b38a7abb09829f08f9e AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
