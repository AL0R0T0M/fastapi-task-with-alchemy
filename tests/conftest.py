import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from apps.users.repository import get_session
from apps.users.models import Base
from main import app
from apps.users.celery_worker import celery_app
from settings.settings import Settings
 
settings = Settings()
TEST_DATABASE_URL = settings.TEST_URL

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    maintenance_db_url = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
        f"{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/postgres"
    )
    test_db_name = settings.DB_NAME + "_test"

    maintenance_engine = create_async_engine(maintenance_db_url, isolation_level="AUTOCOMMIT")
    async with maintenance_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        await conn.execute(text(f"CREATE DATABASE {test_db_name}"))

    yield

    async with maintenance_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE {test_db_name}"))

app.dependency_overrides[get_session] = override_get_async_session

@pytest.fixture(scope='function')
async def prepare_database() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session(prepare_database) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope='function')
def celery_eager():
    celery_app.conf.update(task_always_eager=True)
    yield
    celery_app.conf.update(task_always_eager=False)

@pytest.fixture(autouse=True)
def patch_celery_db_url(monkeypatch):
    monkeypatch.setattr("apps.users.tasks.async_session", async_session_maker)