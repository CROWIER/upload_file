from fastapi import APIRouter, Depends, UploadFile, File

from src.schemas.file_schema import FileMetadataResponse
from src.services.file_service import FileService
from src.models.user import User
from src.api.dependencies import get_file_service, get_current_active_user


router = APIRouter(tags=["files"])


@router.post("/", response_model=FileMetadataResponse)
async def upload_file(
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service),
    current_user: User = Depends(get_current_active_user),
):
    return await service.upload_file(file)
