from uuid import UUID
from pydantic import BaseModel


class FileMetadataCreate(BaseModel):
    filename: str
    content_type: str
    size: int
    url: str
    hash: str


class FileMetadataResponse(BaseModel):
    id: UUID
    url: str

    class Config:
        orm_mode = True
        from_attributes = True
