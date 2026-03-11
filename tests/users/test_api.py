import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_read_user(ac: AsyncClient, prepare_database, celery_eager):

    response = await ac.post("/api/v1/users/", json={
        "name": "api_user",
        "username": "api_username",
        "password": "password123",
        "email": "api@example.com"
    })
    assert response.status_code == 200
    assert response.json() == {'ok': True, 'msg': 'user created!'}

    response = await ac.get("/api/v1/users/")
    assert response.status_code == 200
    users = response.json()
    assert any(user['username'] == 'api_username' for user in users)
    assert any(user['email'] == 'api@example.com' for user in users)