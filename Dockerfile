# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Optional if using static files (like Django Admin)
RUN mkdir -p /vol/web/static

CMD ["gunicorn", "rentbuy.wsgi:application", "--bind", "0.0.0.0:8000"]
