import os
import logging
import aiofiles

from app.core.exceptions import PracticeServiceException, ReportNotFoundException
from app.domain.repositories.report_repo import IReportRepository

logger = logging.getLogger(__name__)

class LocalReportRepository(IReportRepository):
    """Concrete implementation of IReportRepository that retrieves PDFs from local file system."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.getenv("CONTAINER_REPORT_PATH", "/app/storage")
        os.makedirs(self.base_dir, exist_ok=True)

    async def get_pdf(self, uid: str, practice_id: int) -> bytes:
        file_path = os.path.join(self.base_dir, uid, "reports", f"report_{practice_id}.pdf")

        logger.debug(f"Looking for PDF at: {file_path}")

        if not os.path.exists(file_path):
            logger.error(f"PDF not found at path: {file_path}")
            raise ReportNotFoundException(practice_id=practice_id)

        try:
            async with aiofiles.open(file_path, "rb") as pdf_file:
                content = await pdf_file.read()
            logger.info(f"Successfully loaded PDF for uid={uid}, practice_id={practice_id}, path={file_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}", exc_info=True)
            raise PracticeServiceException(
                message=f"Error reading report {practice_id}",
                code=500,
                error_code="REPORT_READ_ERROR",
                details={"practice_id": practice_id, "error": str(e)}
            )