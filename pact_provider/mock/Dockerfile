FROM python:3.7.7-slim-buster
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY mock_provider_flask.py mock_provider_flask.py
CMD ["python", "mock_provider_flask.py"]
