# our base image
FROM python:3.13-slim@sha256:27f90d79cc85e9b7b2560063ef44fa0e9eaae7a7c3f5a9f74563065c5477cc24

WORKDIR /var/www/
COPY requirements.txt .
RUN pip install -r requirements.txt



ENV FLASK_APP=mock_sirius_backend/app.py
ENV FLASK_ENV=development

CMD ["python", "mock_sirius_backend/app.py"]
