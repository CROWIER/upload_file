import pytest
from uuid import uuid4
from src.config.app import app
from src.models.user import User
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock
from src.services.file_service import FileService
from src.schemas.file_schema import FileMetadataResponse
from src.api.dependencies import get_file_service, get_current_active_user

pytestmark = pytest.mark.asyncio


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_file_service():
    mock = MagicMock(spec=FileService)
    mock.upload_file = AsyncMock()
    return mock


@pytest.fixture
def mock_current_user():
    user = User(id=1, username="testuser", email="test@example.com", is_active=True)
    return user


@pytest.fixture(autouse=True)
def override_dependencies(mock_file_service, mock_current_user):
    app.dependency_overrides[get_file_service] = lambda: mock_file_service
    app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
    yield
    app.dependency_overrides.clear()


async def test_upload_file_success(client, mock_file_service):
    file_content = b"test content"
    file_name = "test.pdf"
    mock_response = FileMetadataResponse(
        id=uuid4(),
        url="http://minio/test.pdf",
    )
    mock_file_service.upload_file.return_value = mock_response

    response = client.post(
        "/api/files/",
        files={"file": (file_name, file_content, "application/pdf")}
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json() == {
        "id": str(mock_response.id),
        "url": "http://minio/test.pdf",
    }, f"Response JSON: {response.json()}"
    mock_file_service.upload_file.assert_awaited_once()


async def test_upload_file_unsupported_extension(client, mock_file_service):
    file_content = b"test content"
    file_name = "test.txt"
    mock_file_service.upload_file.side_effect = HTTPException(
        400, "Unsupported file extension"
    )

    response = client.post(
        "/api/files/",
        files={"file": (file_name, file_content, "text/plain")}
    )

    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    assert response.json() == {"detail": "Unsupported file extension"}, f"Response JSON: {response.json()}"
    mock_file_service.upload_file.assert_awaited_once()


async def test_upload_file_server_error(client, mock_file_service):
    file_content = b"test content"
    file_name = "test.pdf"
    mock_file_service.upload_file.side_effect = HTTPException(
        500, "Error uploading file: Server error"
    )

    response = client.post(
        "/api/files/",
        files={"file": (file_name, file_content, "application/pdf")}
    )

    assert response.status_code == 500, f"Expected 500, got {response.status_code}: {response.text}"
    assert response.json() == {"detail": "Error uploading file: Server error"}, f"Response JSON: {response.json()}"
    mock_file_service.upload_file.assert_awaited_once()
