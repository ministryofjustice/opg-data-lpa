FROM public.ecr.aws/lambda/python:3.13@sha256:105a6ba559ee3d9897c798b7d85bea5ff924bf710dcf1dd0ff1ccab630c6fecd AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:105a6ba559ee3d9897c798b7d85bea5ff924bf710dcf1dd0ff1ccab630c6fecd AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
