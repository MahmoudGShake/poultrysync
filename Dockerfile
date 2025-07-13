# Dockerfile
FROM python:3.11-slim

# system deps for mysqlclient
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
#RUN mkdir -p /app/logs
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["gunicorn", "poultrysync.wsgi:application", "-b", "0.0.0.0:8000"]
