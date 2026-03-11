import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.repository import User_Repository
from apps.users.schemas import create_User


@pytest.mark.asyncio
async def test_add_user_and_get_by_username(db_session: AsyncSession):
    """
    Интеграционный тест: проверяем добавление пользователя в БД
    и его последующее получение по имени пользователя.
    """
    repo = User_Repository(db_session)

    # 1. Создаем пользователя
    user_data = create_User(
        name="Test User",
        username="testuser",
        password="testpassword", # В реальном проекте пароль должен быть хеширован
        email="test@user.com"
    )
    await repo.input_data(user_data)

    # 2. Получаем пользователя из БД
    retrieved_user = await repo.get_user_by_username("testuser")

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@user.com"