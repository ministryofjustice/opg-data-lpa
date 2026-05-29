FROM public.ecr.aws/lambda/python:3.13@sha256:f21217f9ae211394a9cf22c154ba64a9e49898bda4234773fd47258729d396b5 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:f21217f9ae211394a9cf22c154ba64a9e49898bda4234773fd47258729d396b5 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
