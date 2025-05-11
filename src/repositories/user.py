from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.models.user import User
from src.schemas.auth import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate, hashed_password: str):
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        self.session.add(db_user)
        try:
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user
        except SQLAlchemyError:
            await self.session.rollback()
            raise