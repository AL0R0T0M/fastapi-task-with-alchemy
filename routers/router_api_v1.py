from fastapi import APIRouter
from apps.users.routers import UserRouter
from apps.auth.routers import AuthRouter

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(UserRouter)
router.include_router(AuthRouter)