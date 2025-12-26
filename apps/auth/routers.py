from .services import Auth_services
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import login_user, register_user, Token
from apps.users.schemas import read_User
from apps.users.routers import get_user_service
from apps.users.services import User_services
from .repository import Auth_Repository

AuthRouter = APIRouter(
    prefix='/auth',
    tags=['AuthTools']
)

def get_auth_service(user_service: User_services = Depends(get_user_service)) -> Auth_services:
    auth_repo = Auth_Repository(user_service.repo)
    return Auth_services(auth_repo)

@AuthRouter.post('/login', response_model=Token)
async def login_usr(form_data: OAuth2PasswordRequestForm = Depends(), service: Auth_services = Depends(get_auth_service)):
    login_data = login_user(username=form_data.username, password=form_data.password)
    token = await service.login(login_data)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect login or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@AuthRouter.post('/register', response_model=read_User)
async def register(user: register_user, service: Auth_services = Depends(get_auth_service)):
    try:
        created = await service.register(user)
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@AuthRouter.post('/refresh', response_model=Token)
def refresh_token(data: str, service: Auth_services = Depends(get_auth_service)):
    token = service.refresh(data)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='incorrect token',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token