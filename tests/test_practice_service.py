import pytest
from unittest.mock import AsyncMock
from app.domain.services.practice_service import PracticeService
from app.domain.entities.practice import Practice


@pytest.mark.asyncio
async def test_get_practices_for_user_returns_list():
    mock_repo = AsyncMock()
    mock_repo.get_practices_for_user.return_value = [
        Practice(
            id=1,
            scale="C Major",
            scale_type="Major",
            duration=120,
            bpm=100,
            figure=4.0,
            octaves=2,
            num_postural_errors=1,
            num_musical_errors=2,
            date="2025-11-01",
            time="10:00",
            state="completed",
            local_video_url="video1.mp4",
            pdf_url="report1.pdf"
        )
    ]
    service = PracticeService(mock_repo)

    result = await service.get_practices_for_user("uid123")

    mock_repo.get_practices_for_user.assert_awaited_once_with("uid123", None, None)
    assert isinstance(result, list)
    assert result[0].scale == "C Major"


@pytest.mark.asyncio
async def test_get_practice_by_id_returns_object():
    mock_repo = AsyncMock()
    mock_repo.get_practice_by_id.return_value = Practice(
        id=1,
        scale="G Minor",
        scale_type="Minor",
        duration=90,
        bpm=120,
        figure=2.0,
        octaves=1,
        num_postural_errors=0,
        num_musical_errors=1,
        date="2025-11-02",
        time="09:30",
        state="in_progress",
        local_video_url="video2.mp4",
        pdf_url="report2.pdf"
    )
    service = PracticeService(mock_repo)

    result = await service.get_practice_by_id("uid123", 1)

    mock_repo.get_practice_by_id.assert_awaited_once_with("uid123", 1)
    assert isinstance(result, Practice)
    assert result.scale == "G Minor"


@pytest.mark.asyncio
async def test_get_practice_by_id_raises_exception():
    mock_repo = AsyncMock()
    mock_repo.get_practice_by_id.side_effect = Exception("DB fetch failed")
    service = PracticeService(mock_repo)

    with pytest.raises(Exception, match="DB fetch failed"):
        await service.get_practice_by_id("uid123", 999)
