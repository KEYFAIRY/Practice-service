import pytest
from unittest.mock import AsyncMock
from app.domain.services.practice_metadata_service import PracticeMetadataService
from app.domain.entities.practice_metadata import PracticeMetadata


@pytest.mark.asyncio
async def test_get_practice_metadata_returns_object():
    mock_repo = AsyncMock()
    mock_repo.get_practice_metadata.return_value = PracticeMetadata(
        id_practice=10,
        video_in_local="local/video1.mp4",
        report="Good posture",
        video_done=True,
        audio_done=True
    )
    service = PracticeMetadataService(mock_repo)

    result = await service.get_practice_metadata("user123", 10)

    mock_repo.get_practice_metadata.assert_awaited_once_with("user123", 10)
    assert isinstance(result, PracticeMetadata)
    assert result.id_practice == 10
    assert result.video_done is True


@pytest.mark.asyncio
async def test_finish_practice_returns_metadata():
    mock_repo = AsyncMock()
    mock_repo.finish_practice.return_value = PracticeMetadata(
        id_practice=11,
        video_in_local="local/video2.mp4",
        report="All good",
        video_done=True,
        audio_done=True
    )
    service = PracticeMetadataService(mock_repo)

    result = await service.finish_practice("user123", 11)

    mock_repo.finish_practice.assert_awaited_once_with("user123", 11)
    assert isinstance(result, PracticeMetadata)
    assert result.audio_done is True


@pytest.mark.asyncio
async def test_get_practice_metadata_raises_exception():
    mock_repo = AsyncMock()
    mock_repo.get_practice_metadata.side_effect = Exception("Metadata fetch failed")
    service = PracticeMetadataService(mock_repo)

    with pytest.raises(Exception, match="Metadata fetch failed"):
        await service.get_practice_metadata("user123", 99)
