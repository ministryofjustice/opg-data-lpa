FROM public.ecr.aws/lambda/python:3.13@sha256:dfb8a58c2dac557a1eb863d7272fbdf57d11a5e9c02534bd1bb5dd92335f8ba8 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:dfb8a58c2dac557a1eb863d7272fbdf57d11a5e9c02534bd1bb5dd92335f8ba8 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
