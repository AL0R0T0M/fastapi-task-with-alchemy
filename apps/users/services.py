from .repository import User_Repository
from .schemas import create_User


class User_services:
    def __init__(self, repo: User_Repository):
        self.repo = repo

    async def create(self, new_user: create_User):
        await self.repo.input_data(new_user)
    
    async def read_users(self):
        return await self.repo.get_users()
    
    async def read_user_username(self, username):
        return await self.repo.get_user_by_username(username)
    
    async def read_user_id(self, user_id):
        return await self.repo.get_user_by_id(user_id)
