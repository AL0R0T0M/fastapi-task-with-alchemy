from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    TEST_DB_HOST: str = 'localhost'
    TEST_DB_PORT: int = 5433

    JWT_ALGO: str
    JWT_SECRET_KEY: str
    JWT_EXCPIRE_MINUTE: int

    REDIS_URL: str
    
    model_config = SettingsConfigDict(
        env_file='.env',
    )

    @property
    def URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def TEST_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.DB_NAME}_test'


    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"{self.REDIS_URL}/0"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"{self.REDIS_URL}/1"
