from fastapi import APIRouter
from src.api.routes import files, auth

router = APIRouter()

router.include_router(files.router, prefix="/files")
router.include_router(auth.router, prefix="/auth")