# Базовый образ с Python 3.13
FROM python:3.13-slim

# Установка зависимостей системы (для Redis и Celery)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY ./apps ./apps
COPY ./settings ./settings
COPY ./main.py .
COPY ./alembic.ini .
COPY ./alembic ./alembic

# Открываем порт для FastAPI (только для сервиса app)
EXPOSE 8000

# Команда по умолчанию (будет переопределена в docker-compose)
CMD ["tail", "-f", "/dev/null"]
