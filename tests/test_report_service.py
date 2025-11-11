import pytest
from unittest.mock import AsyncMock
from app.domain.services.report_service import ReportService


@pytest.mark.asyncio
async def test_get_report_returns_bytes():
    mock_repo = AsyncMock()
    mock_repo.get_pdf.return_value = b"%PDF-1.4"
    service = ReportService(mock_repo)

    result = await service.get_report("uid123", 10)

    mock_repo.get_pdf.assert_awaited_once_with("uid123", 10)
    assert isinstance(result, bytes)
    assert result.startswith(b"%PDF")


@pytest.mark.asyncio
async def test_get_report_raises_exception():
    mock_repo = AsyncMock()
    mock_repo.get_pdf.side_effect = Exception("PDF not found")
    service = ReportService(mock_repo)

    with pytest.raises(Exception, match="PDF not found"):
        await service.get_report("uid123", 10)
