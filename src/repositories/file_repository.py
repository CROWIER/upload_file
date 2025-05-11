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
