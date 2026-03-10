from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .services import User_services
from .schemas import create_User, read_User
from typing import List
from .repository import User_Repository, get_session


UserRouter = APIRouter(
    prefix='/users',
    tags=['UserTools']
)

def get_user_service(session: AsyncSession = Depends(get_session)) -> User_services:
    repo = User_Repository(session)
    return User_services(repo)

@UserRouter.get('/', response_model=List[read_User])
async def get_users(service: User_services = Depends(get_user_service)):
    result = await service.read_users()
    return result

@UserRouter.post('/')
def create_new_user(data: create_User, service: User_services = Depends(get_user_service)):
    service.create(data)
    return {'ok': True, 'msg': 'user created!'}