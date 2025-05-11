import uuid

from sqlalchemy import select, delete
from src.models.file_data import FileMetadata
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.file_schema import FileMetadataCreate


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, file_metadata: FileMetadataCreate) -> FileMetadata:
        file_data = file_metadata.model_dump()
        db_obj = FileMetadata(**file_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj


async def get_by_id(self, file_id: uuid.UUID) -> FileMetadata:
    query = select(FileMetadata).where(FileMetadata.id == file_id)
    result = await self.session.execute(query)
    return result.scalar_one_or_none()


async def get_all(self, skip: int = 0, limit: int = 100) -> list[FileMetadata]:
    query = select(FileMetadata).offset(skip).limit(limit)
    result = await self.session.execute(query)
    return result.scalars().all()


async def delete_file(self, file_id: uuid.UUID) -> bool:
    query = delete(FileMetadata).where(FileMetadata.id == file_id)
    result = await self.session.execute(query)
    await self.session.commit()
    return result.rowcount > 0
