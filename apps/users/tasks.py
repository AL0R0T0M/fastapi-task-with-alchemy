import asyncio
from .celery_worker import celery_app
from celery.signals import task_prerun
from .repository import User_Repository, async_session
from .schemas import create_User


@celery_app.task
def create_user_task(user_data: dict):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    async def _create():
        async with async_session() as session:
            await User_Repository(session).input_data(create_User.model_validate(user_data))

    if loop and loop.is_running():
        loop.run_until_complete(_create())
    else:
        asyncio.run(_create())
