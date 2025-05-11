from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user import User
from src.schemas.auth import Token, UserCreate, User as UserSchema
from src.services.auth import AuthService
from src.api.dependencies import get_auth_service, get_current_active_user

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login_user(form_data.username, form_data.password)

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.create_user(user)

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user
