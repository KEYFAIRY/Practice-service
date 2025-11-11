import pytest
from unittest.mock import AsyncMock
from app.domain.services.postural_error_service import PosturalErrorService
from app.domain.entities.postural_error import PosturalError


@pytest.mark.asyncio
async def test_get_postural_errors_by_practice_id_returns_list():
    mock_repo = AsyncMock()
    mock_repo.get_postural_errors_by_practice_id.return_value = [
        PosturalError(id=1, min_sec_init="00:15", min_sec_end="00:25", explication="Back not straight", id_practice=5)
    ]
    service = PosturalErrorService(mock_repo)

    result = await service.get_postural_errors_by_practice_id(5)

    mock_repo.get_postural_errors_by_practice_id.assert_awaited_once_with(5)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].explication == "Back not straight"


@pytest.mark.asyncio
async def test_get_postural_errors_by_practice_id_returns_empty_list():
    mock_repo = AsyncMock()
    mock_repo.get_postural_errors_by_practice_id.return_value = []
    service = PosturalErrorService(mock_repo)

    result = await service.get_postural_errors_by_practice_id(99)

    mock_repo.get_postural_errors_by_practice_id.assert_awaited_once_with(99)
    assert result == []


@pytest.mark.asyncio
async def test_get_postural_errors_by_practice_id_raises_exception():
    mock_repo = AsyncMock()
    mock_repo.get_postural_errors_by_practice_id.side_effect = Exception("DB failure")
    service = PosturalErrorService(mock_repo)

    with pytest.raises(Exception, match="DB failure"):
        await service.get_postural_errors_by_practice_id(1)
