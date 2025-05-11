# src/services/minio_service.py

import io
import hashlib
from datetime import timedelta

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from src.config.settings import settings


class MinioService:
    def __init__(self, client: Minio):
        self.client = client
        self.bucket = settings.MINIO_BUCKET_NAME

    async def upload_file(self, file: UploadFile) -> tuple[str, str, int]:
        data = await file.read()
        size = len(data)
        h = hashlib.sha256(data).hexdigest()
        path = f"{h}/{file.filename}"

        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=path,
                data=io.BytesIO(data),
                length=size,
                content_type=file.content_type,
            )
        except S3Error as e:
            raise RuntimeError(f"MinIO upload error: {e}") from e
        finally:
            await file.seek(0)

        return path, h, size

    def generate_presigned_url(self, path: str, expires_minutes: int = 30) -> str:
        try:
            return self.client.presigned_get_object(
                bucket_name=self.bucket,
                object_name=path,
                expires=timedelta(minutes=expires_minutes),
            )
        except S3Error as e:
            raise RuntimeError(f"MinIO presign error: {e}") from e
