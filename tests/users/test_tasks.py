import pytest
from unittest.mock import patch, Mock

from apps.users.services import User_services
from apps.users.schemas import create_User


def test_create_user_service_calls_celery():
    user_data = create_User(
        name="test_user",
        username="test_username",
        password="supersecret",
        email="test@example.com",
    )

    with patch("apps.users.services.create_user_task.delay") as mock_delay:
        service = User_services(repo=Mock())
        service.create(user_data)
        mock_delay.assert_called_once_with(user_data.model_dump())