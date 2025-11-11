import pytest
from unittest.mock import AsyncMock
from app.domain.services.video_service import VideoService


@pytest.mark.asyncio
async def test_delete_video_successful():
    mock_repo = AsyncMock()
    mock_repo.delete_video.return_value = True
    service = VideoService(mock_repo)

    result = await service.delete_video("uid123", 10)

    mock_repo.delete_video.assert_awaited_once_with("uid123", 10)
    assert result is True


@pytest.mark.asyncio
async def test_delete_video_failure():
    mock_repo = AsyncMock()
    mock_repo.delete_video.return_value = False
    service = VideoService(mock_repo)

    result = await service.delete_video("uid123", 11)

    mock_repo.delete_video.assert_awaited_once_with("uid123", 11)
    assert result is False


@pytest.mark.asyncio
async def test_delete_video_raises_exception():
    mock_repo = AsyncMock()
    mock_repo.delete_video.side_effect = Exception("Delete failed")
    service = VideoService(mock_repo)

    with pytest.raises(Exception, match="Delete failed"):
        await service.delete_video("uid123", 12)
