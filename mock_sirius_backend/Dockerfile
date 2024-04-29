# our base image
FROM python:3.10-slim

WORKDIR /var/www/
COPY requirements.txt .
RUN pip install -r requirements.txt



ENV FLASK_APP=mock_sirius_backend/app.py
ENV FLASK_ENV=development

CMD ["python", "mock_sirius_backend/app.py"]
