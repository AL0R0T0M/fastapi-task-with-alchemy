from .repository import Auth_Repository
from .schemas import Token, login_user
from utils.jwt import create_access_token, create_refresh_token, read_token


class Auth_services:
    def __init__(self, repo: Auth_Repository):
        self.repo = repo
    async def register(self, data: dict):
        return await self.repo.register_new_user(data)
    
    async def login(self, data: login_user):
        user = await self.repo.authenticate(data)
        if not user:
            return None
        
        token_data = {'sub': user.username, 'user_id': user.user_id}

        access = create_access_token(token_data)
        refresh = create_refresh_token(token_data)
        return Token(access_token=access, refresh_token=refresh)
    
    def refresh(self, token: str):
        payload = read_token(token)
        if not payload:
            return None
        
        if payload.get('type') != 'refresh':
            return None
        
        token_data = {'sub': payload.get('sub'), 'user_id': payload.get('user_id')}

        access = create_access_token(token_data)
        refresh = create_refresh_token(token_data)

        return Token(access_token=access, refresh_token=refresh)
