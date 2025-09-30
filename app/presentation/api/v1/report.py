from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from app.application.use_cases.get_report_use_case import GetReportUseCase
import io

from app.presentation.api.v1.dependencies import get_report_use_case_dependency

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get(
    "/{uid}/{practice_id}",
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
    summary="Download practice report",
    description="Download the PDF report for a specific practice"
)
async def download_report(
    uid: str,
    practice_id: int,
    use_case: GetReportUseCase = Depends(get_report_use_case_dependency),
):
    pdf_content = await use_case.execute(uid, practice_id)

    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{practice_id}.pdf"}
    )
