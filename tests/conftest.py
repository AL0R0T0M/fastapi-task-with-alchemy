import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from apps.users.repository import get_session
from apps.users.models import Base
from main import app  # Предполагается, что ваш FastAPI app находится в main.py
from settings.settings import Settings
 
# --- Настройка тестовой БД ---
# Используем переменные окружения для тестовой БД
settings = Settings()
TEST_DATABASE_URL = settings.TEST_URL

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

# Переопределяем зависимость get_session для использования тестовой БД
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """
    Фикстура для создания и очистки таблиц в тестовой БД перед и после сессии тестов.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop(request):
    """Создает экземпляр event loop для всей тестовой сессии."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания асинхронного HTTP клиента."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура для получения асинхронной сессии к тестовой БД для каждого теста.
    """
    async with async_session_maker() as session:
        yield session