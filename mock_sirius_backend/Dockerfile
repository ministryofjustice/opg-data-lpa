# our base image
FROM python:3.12-slim@sha256:d67a7b66b989ad6b6d6b10d428dcc5e0bfc3e5f88906e67d490c4d3daac57047

WORKDIR /var/www/
COPY requirements.txt .
RUN pip install -r requirements.txt



ENV FLASK_APP=mock_sirius_backend/app.py
ENV FLASK_ENV=development

CMD ["python", "mock_sirius_backend/app.py"]
