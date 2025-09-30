import logging

from app.domain.services.report_service import ReportService


logger = logging.getLogger(__name__)

class GetReportUseCase:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    async def execute(self, uid: str, practice_id: int) -> bytes:
        """Retrieve the report for a specific practice."""
        logger.info(f"Fetching report for user {uid}, practice_id={practice_id}")
        report = await self.report_service.get_report(uid, practice_id)
        return report