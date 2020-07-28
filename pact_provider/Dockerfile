FROM python:3.7.7-slim-buster
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir pact_provider
ADD https://github.com/pact-foundation/pact-ruby-standalone/releases/download/v1.82.3/pact-1.82.3-linux-x86_64.tar.gz pact-1.82.3-linux-x86_64.tar.gz
RUN tar xzf pact-1.82.3-linux-x86_64.tar.gz
WORKDIR pact_provider
COPY check_pact_deployable.py check_pact_deployable.py
COPY test test
WORKDIR /pact_provider/test/
CMD ["tail", "-f", "/dev/null"]
