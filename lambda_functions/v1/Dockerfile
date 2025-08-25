FROM python:3.11-slim-buster@sha256:c46b0ae5728c2247b99903098ade3176a58e274d9c7d2efeaaab3e0621a53935
WORKDIR /var/www/lambda_functions/v1

# Install Python Dependencies
COPY requirements requirements
RUN cat ./requirements/*.txt | uniq | grep -v "#" > ./requirements/local-requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements/local-requirements.txt

EXPOSE 4343

WORKDIR /var/www/lambda_functions/v1/functions/lpa/app

ENV FLASK_APP "lpa_local.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True


CMD flask run --host=0.0.0.0 --port=4343



