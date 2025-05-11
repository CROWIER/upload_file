from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config.database import get_db
from src.config.minio_client import create_minio_client
from src.config.settings import settings
from src.models.user import User
from src.repositories.user import UserRepository
from src.repositories.file_repository import FileRepository
from src.schemas.auth import TokenData
from src.services.auth import AuthService
from src.services.file_service import FileService
from src.services.minio_service import MinioService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def get_minio_service(
    client = Depends(create_minio_client),
) -> MinioService:
    return MinioService(client)


async def get_file_service(
        db: AsyncSession = Depends(get_db),
        minio_svc: MinioService = Depends(get_minio_service),
) -> FileService:
    repo = FileRepository(db)
    return FileService(repository=repo, minio_service=minio_svc)


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_service: AuthService = Depends(get_auth_service),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await auth_service.user_repository.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
