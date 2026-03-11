import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users.repository import User_Repository
from apps.users.schemas import create_User


@pytest.mark.asyncio
async def test_add_user_and_get_by_username(prepare_database, db_session: AsyncSession):
    repo = User_Repository(db_session)

    user_data = create_User(
        name="Test User",
        username="testuser",
        password="testpassword",
        email="test@user.com"
    )
    await repo.input_data(user_data)

    retrieved_user = await repo.get_user_by_username("testuser")

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@user.com"