FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apps ./apps
COPY ./settings ./settings
COPY ./main.py .
COPY ./alembic.ini .
COPY ./alembic ./alembic

EXPOSE 8000

CMD ["tail", "-f", "/dev/null"]
