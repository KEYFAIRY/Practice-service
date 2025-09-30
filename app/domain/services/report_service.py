import logging

from app.domain.repositories.report_repo import IReportRepository


logger = logging.getLogger(__name__)

class ReportService:

    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def get_report(self, uid: str, practice_id: int) -> bytes:
        logger.info(f"Service getting report for user {uid}, practice_id={practice_id}")
        return await self.report_repository.get_pdf(uid, practice_id)