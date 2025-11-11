import pytest
from unittest.mock import AsyncMock
from app.domain.services.musical_error_service import MusicalErrorService
from app.domain.entities.musical_error import MusicalError


@pytest.mark.asyncio
async def test_get_musical_errors_by_practice_returns_list(mocker):
    # Arrange
    mock_repo = mocker.AsyncMock()
    mock_repo.get_musical_errors_by_practice_id.return_value = [
        MusicalError(id=1, min_sec="00:30", note_played="C#", note_correct="D", id_practice=101),
        MusicalError(id=2, min_sec="01:15", note_played="E", note_correct="F", id_practice=101),
    ]
    service = MusicalErrorService(mock_repo)

    # Act
    result = await service.get_musical_errors_by_practice(101)

    # Assert
    assert len(result) == 2
    assert isinstance(result[0], MusicalError)
    assert result[0].note_correct == "D"

@pytest.mark.asyncio
async def test_get_musical_errors_by_practice_returns_empty_list():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_musical_errors_by_practice_id.return_value = []
    service = MusicalErrorService(mock_repo)

    # Act
    result = await service.get_musical_errors_by_practice(practice_id=999)

    # Assert
    mock_repo.get_musical_errors_by_practice_id.assert_awaited_once_with(999)
    assert result == []


@pytest.mark.asyncio
async def test_get_musical_errors_by_practice_handles_exception():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_musical_errors_by_practice_id.side_effect = Exception("DB error")
    service = MusicalErrorService(mock_repo)

    # Act / Assert
    with pytest.raises(Exception) as exc:
        await service.get_musical_errors_by_practice(practice_id=5)

    assert "DB error" in str(exc.value)
    mock_repo.get_musical_errors_by_practice_id.assert_awaited_once_with(5)
