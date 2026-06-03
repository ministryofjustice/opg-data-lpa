FROM public.ecr.aws/lambda/python:3.13@sha256:687a994092d7bce8164d307bb32230762e3d2325b37cc3fbe4edd14c553cc9d1 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:687a994092d7bce8164d307bb32230762e3d2325b37cc3fbe4edd14c553cc9d1 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
