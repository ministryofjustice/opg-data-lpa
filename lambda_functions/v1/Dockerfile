FROM public.ecr.aws/lambda/python:3.13@sha256:b18d09590cead2dff65c7427c4f0fc056fd882f3997cdad96223da497658e573 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:b18d09590cead2dff65c7427c4f0fc056fd882f3997cdad96223da497658e573 AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
