from celery import Celery
from settings.settings import Settings

celery_app = Celery(
    'tasks',
    broker=Settings().CELERY_BROKER_URL,
    backend=Settings().CELERY_RESULT_BACKEND,
    include=['apps.users.tasks']  # Указываем, где искать задачи
)
