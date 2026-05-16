FROM public.ecr.aws/lambda/python:3.13@sha256:68403b483362ff281e4aa12c5ea27377cb6ea7ca1c2ea6d62ce2b74589fd12d6 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:68403b483362ff281e4aa12c5ea27377cb6ea7ca1c2ea6d62ce2b74589fd12d6 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
