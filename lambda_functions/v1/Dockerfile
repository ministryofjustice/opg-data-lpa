FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:044c120ac73fd263df0e1eeb8b2938a8b7038c8f045747091ee21f60eef38615 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
