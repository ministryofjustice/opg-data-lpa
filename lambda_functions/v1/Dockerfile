FROM public.ecr.aws/lambda/python:3.13@sha256:c9423ce89cdee6b92cd134aa067f4ac86c17a1eb2f7a98f9447a7d52824ec49b AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:c9423ce89cdee6b92cd134aa067f4ac86c17a1eb2f7a98f9447a7d52824ec49b AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
