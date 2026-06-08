FROM public.ecr.aws/lambda/python:3.13@sha256:848e60fa6f070804e1a1b69a1625960ca7bc8c76b2497ca4ce8ac7b71ceda63a AS build

WORKDIR /app

COPY lambda_functions/v1/requirements/requirements.txt requirements.txt

RUN pip install --upgrade pip -t python/
RUN pip install -r requirements.txt -t python/

COPY lambda_functions/v1/functions/lpa/ python/

FROM public.ecr.aws/lambda/python:3.13@sha256:848e60fa6f070804e1a1b69a1625960ca7bc8c76b2497ca4ce8ac7b71ceda63a AS runtime

WORKDIR /var/task

COPY --from=build /app/python ./

RUN rm -f /usr/local/bin/aws-lambda-rie

CMD [ "app.lpa.lambda_handler" ]
