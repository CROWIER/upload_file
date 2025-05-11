from pathlib import Path

from fastapi import UploadFile
from fastapi import HTTPException

from src.services.minio_service import MinioService
from src.repositories.file_repository import FileRepository
from src.schemas.file_schema import FileMetadataCreate, FileMetadataResponse


class FileService:
    def __init__(self, repository: FileRepository, minio_service: MinioService):
        self.repository = repository
        self.minio_service = minio_service

    def _validate_file(self, file: UploadFile):
        allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".dcm"}
        ext = Path(file.filename).suffix.lower()
        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Unsupported file extension")

    async def upload_file(self, file: UploadFile) -> FileMetadataResponse:
        try:
            self._validate_file(file)
            file_path, file_hash, file_size = await self.minio_service.upload_file(file)
            file_url = self.minio_service.generate_presigned_url(file_path)

            file_metadata = FileMetadataCreate(
                filename=file.filename,
                content_type=file.content_type,
                url=file_url,
                hash=file_hash,
                size=file_size,
            )
            db_file = await self.repository.save(file_metadata)
            return FileMetadataResponse(id=db_file.id, url=file_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
