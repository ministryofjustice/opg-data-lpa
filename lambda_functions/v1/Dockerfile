FROM public.ecr.aws/lambda/python:3.13@sha256:67b32eb858d2124326e3887fa825a0db934cbbd22f2b0ce489ee1def49020cfe AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:67b32eb858d2124326e3887fa825a0db934cbbd22f2b0ce489ee1def49020cfe AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
