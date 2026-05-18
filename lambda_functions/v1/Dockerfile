FROM public.ecr.aws/lambda/python:3.13@sha256:db17c9446ac770df1ae29eb007ff51797426c2728acb44b89fa3a2a9b8dc2439 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:db17c9446ac770df1ae29eb007ff51797426c2728acb44b89fa3a2a9b8dc2439 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
