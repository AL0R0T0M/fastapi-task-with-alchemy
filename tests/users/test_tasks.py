import pytest
from unittest.mock import patch, AsyncMock

from apps.users.tasks import create_user_task
from apps.users.schemas import create_User


@pytest.mark.asyncio
async def test_create_user_task():
    """
    Тест для Celery-задачи create_user_task.
    Проверяет, что задача корректно валидирует данные и вызывает метод репозитория.
    """
    user_data_dict = {
        "name": "test_user",
        "username": "test_username",
        "password": "supersecret",
        "email": "test@example.com"
    }

    # Мокаем асинхронный менеджер контекста и репозиторий
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.commit = AsyncMock()

    with patch("apps.users.repository.async_session", return_value=mock_session):
        with patch("apps.users.tasks.User_Repository", return_value=mock_repo):
            # Запускаем задачу синхронно для теста
            create_user_task.s(user_data_dict).apply()

            # Проверяем, что метод input_data был вызван с правильными данными
            mock_repo.input_data.assert_awaited_once()
            # Аргумент, переданный в input_data, должен быть экземпляром create_User
            call_args = mock_repo.input_data.call_args[0][0]
            assert isinstance(call_args, create_User)
            assert call_args.username == "test_username"