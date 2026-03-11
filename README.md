# Тестовый проект FastAPI

Пример веб-приложения на FastAPI с использованием PostgreSQL, Redis, Celery и Docker.

## Требования

*   Docker и Docker Compose
*   Python 3.13+
*   `pip` или `uv` для управления зависимостями

## Установка и настройка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/AL0R0T0M/fastapi-task-with-alchemy.git
    cd test
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    При необходимости вы можете изменить значения в файле `.env`.

## Запуск и остановка

*   **Для запуска** всего стека приложений (FastAPI, Celery, PostgreSQL, Redis) выполните команду:
    ```bash
    docker-compose up --build
    ```
    Приложение будет доступно по адресу `http://localhost:8000/docs`.

*   **Для остановки** и удаления контейнеров, сетей и томов выполните:
    ```bash
    docker-compose down -v
    ```

## Тестирование

Перед запуском тестов убедитесь, что Docker-контейнеры запущены, так как тесты используют базу данных и Redis из Docker.

Для запуска тестов выполните команду:
```bash
pytest
```