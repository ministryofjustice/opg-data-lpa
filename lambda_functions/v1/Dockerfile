FROM python:3.11-slim-buster
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



