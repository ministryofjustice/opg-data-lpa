FROM public.ecr.aws/lambda/python:3.13@sha256:5e923dc6f72cb87d3da2b2ab3b1f3ebf7f22ed1196bb21cf9921a74f0da1c778 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:5e923dc6f72cb87d3da2b2ab3b1f3ebf7f22ed1196bb21cf9921a74f0da1c778 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
