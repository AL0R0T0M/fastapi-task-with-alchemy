from .schemas import UserInDB
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .models import UserORM
from settings.settings import Settings


async_engine = create_async_engine(
    url=Settings().URL,
    echo=False,
)

async_session = async_sessionmaker(async_engine)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

class User_Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def input_data(self, data: dict):
        new_user = UserORM(
            name=data.name,
            username=data.username,
            hashed_password=data.password,
            email=data.email
        )
        self.session.add(new_user)
        await self.session.commit()

    async def get_users(self) -> List[UserORM]:
        result = await self.session.execute(select(UserORM))
        return result.scalars().all()
    
    async def get_user_by_username(self, username: str) -> UserORM | None:
        query = select(UserORM).where(UserORM.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_user_by_id(self, user_id: int) -> UserORM | None:
        return await self.session.get(UserORM, user_id)
