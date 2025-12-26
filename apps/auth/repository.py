from apps.users.repository import User_Repository
from apps.users.schemas import create_User
from .schemas import register_user, login_user
from utils.security import pwd_context


class Auth_Repository:
    def __init__(self, user_repo: User_Repository):
        self.user_repo = user_repo
    
    async def register_new_user(self, payload: register_user):
        exists = await self.user_repo.get_user_by_username(payload.username)
        if exists:
            raise ValueError('User with this username is exists')

        hashed = pwd_context.hash(payload.password)
        new_user_data = create_User(
            username=payload.username,
            name=payload.name,
            password=hashed,
            email=payload.email
        )
        await self.user_repo.input_data(new_user_data)
        return await self.user_repo.get_user_by_username(payload.username)
    
    async def authenticate(self, payload: login_user):
        exists = await self.user_repo.get_user_by_username(payload.username)
        if not exists:
            return None
        if not pwd_context.verify(payload.password, exists.hashed_password):
            return None
        return exists
