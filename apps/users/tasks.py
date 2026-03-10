import asyncio
from .celery_worker import celery_app
from .repository import User_Repository, async_session
from .schemas import create_User


@celery_app.task
def create_user_task(user_data: dict):
    """
    Celery-задача для создания пользователя в базе данных.
    Запускает асинхронный код внутри синхронной задачи.
    """
    async def create_user_async():
        async with async_session() as session:
            repo = User_Repository(session)
            user_schema = create_User.model_validate(user_data)
            await repo.input_data(user_schema)

    # Запускаем асинхронную функцию и дожидаемся её выполнения
    asyncio.run(create_user_async())
