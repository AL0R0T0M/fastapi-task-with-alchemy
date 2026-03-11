import pytest
from unittest.mock import Mock, AsyncMock

from apps.users.services import User_services
from apps.users.schemas import create_User


@pytest.fixture
def mock_user_repo():
    repo = Mock()
    repo.get_users = AsyncMock(return_value=[{"name": "test"}, {"name": "test2"}])
    return repo


@pytest.fixture
def user_service(mock_user_repo):
    return User_services(mock_user_repo)


def test_create_user_calls_celery_task(user_service, monkeypatch):
    mock_task = Mock()
    monkeypatch.setattr("apps.users.services.create_user_task.delay", mock_task)
    
    user_data = create_User(name="john", username="john_doe", password="password", email="john@example.com")
    user_service.create(user_data)
    
    mock_task.assert_called_once_with(user_data.model_dump())

@pytest.mark.asyncio
async def test_read_users(user_service, mock_user_repo):
    result = await user_service.read_users()
    mock_user_repo.get_users.assert_awaited_once()
    assert len(result) == 2
    assert result[0]["name"] == "test"