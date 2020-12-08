FROM python:3.8-slim-buster
WORKDIR /var/www/lambda_functions/v1

#AWS CodeArtifact login

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

RUN pip install awscli

RUN aws codeartifact login --tool pip --repository opg-pip-shared-code-dev --domain opg-moj --domain-owner 288342028542 --region eu-west-1


# Install Python Dependencies
COPY requirements requirements
RUN cat ./requirements/*.txt | uniq | grep -v "#" > ./requirements/local-requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements/local-requirements.txt

EXPOSE 4343

WORKDIR /var/www/lambda_functions/v1/functions/lpa/app

ENV FLASK_APP "lpa_local.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True


CMD flask run --host=0.0.0.0 --port=4343



