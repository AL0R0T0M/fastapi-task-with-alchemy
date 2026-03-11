import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_read_user(ac: AsyncClient):
    """
    Сквозной тест:
    1. Отправляет POST-запрос для создания пользователя.
    2. Отправляет GET-запрос для проверки, что пользователь был создан (косвенно).
    """
    # Временно переводим Celery в синхронный режим для теста
    from apps.users.celery_worker import celery_app
    celery_app.conf.update(task_always_eager=True)

    # 1. Создаем пользователя через API
    response = await ac.post("/users/", json={
        "name": "api_user",
        "username": "api_username",
        "password": "password123",
        "email": "api@example.com"
    })
    assert response.status_code == 200
    assert response.json() == {'ok': True, 'msg': 'user created!'}

    # 2. Получаем список пользователей и проверяем, что наш пользователь там есть
    response = await ac.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert any(user['username'] == 'api_username' for user in users)
    assert any(user['email'] == 'api@example.com' for user in users)

    # Возвращаем Celery в асинхронный режим
    celery_app.conf.update(task_always_eager=False)