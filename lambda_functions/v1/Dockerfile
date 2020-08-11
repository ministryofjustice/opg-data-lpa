FROM python:3.8-slim-buster
WORKDIR /var/www/lambda_functions/v1



# Install Python Dependencies

COPY ./requirements requirements
RUN cat ./requirements/*.txt | uniq | grep -v "#" > ./requirements/local-requirements.txt
RUN pip install -r ./requirements/local-requirements.txt

EXPOSE 4343

WORKDIR /var/www/lambda_functions/v1



ENV FLASK_APP "mock_lambda.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

CMD flask run --host=0.0.0.0 --port=4343



