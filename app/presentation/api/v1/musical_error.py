import logging
from fastapi import APIRouter, Depends, status

from typing import List
from app.application.use_cases.get_musical_errors_use_case import GetMusicalErrorsUseCase
from app.presentation.api.v1.dependencies import get_musical_errors_use_case_dependency
from app.presentation.schemas.common_schema import StandardResponse
from app.presentation.schemas.musical_error_schema import MusicalErrorItem, MusicalErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/musical-errors", tags=["Musical Errors"])


@router.get(
    "/{practice_id}",
    response_model=StandardResponse[MusicalErrorResponse],
    status_code=status.HTTP_200_OK,
    summary="Get musical errors for a practice",
    description="Retrieve all musical errors detected for a specific practice ID"
)
async def get_musical_errors(
    practice_id: int,
    use_case: GetMusicalErrorsUseCase = Depends(get_musical_errors_use_case_dependency)
):
    """Endpoint that retrieves musical errors for a given practice."""

    logger.info(f"Retrieving musical errors for practice_id={practice_id}")

    errors_dto: List = await use_case.execute(practice_id=practice_id)

    items = [
        MusicalErrorItem(
            min_sec=e.min_sec,
            missed_note=e.missed_note,
        )
        for e in errors_dto
    ]

    response = MusicalErrorResponse(
        num_errors=len(items),
        errors=items
    )

    return StandardResponse.success(
        data=response,
        message=f"Retrieved {len(items)} musical errors for practice {practice_id}"
    )
