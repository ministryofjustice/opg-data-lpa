FROM public.ecr.aws/lambda/python:3.13@sha256:65e24e10948f4fa5b215855f2d370ad57b6c9fa4ce838a5bab9e7d392e151b28 AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:65e24e10948f4fa5b215855f2d370ad57b6c9fa4ce838a5bab9e7d392e151b28 AS runtime

RUN dnf update -y glibc-0:2.34-231.amzn2023.0.4 --releasever 2023.11.20260413

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
