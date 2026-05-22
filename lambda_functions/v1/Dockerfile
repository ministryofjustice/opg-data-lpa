FROM public.ecr.aws/lambda/python:3.13@sha256:af9ce86c1e2a510244f53a874a5791e2995b38fb512843a3b9069e16777c266f AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:af9ce86c1e2a510244f53a874a5791e2995b38fb512843a3b9069e16777c266f AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
