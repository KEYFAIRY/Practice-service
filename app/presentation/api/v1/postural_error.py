import logging
from fastapi import APIRouter, Depends, status

from typing import List
from app.application.use_cases.get_postural_errors_use_case import GetPosturalErrorsUseCase
from app.presentation.api.v1.dependencies import get_postural_errors_use_case_dependency
from app.presentation.schemas.common_schema import StandardResponse
from app.presentation.schemas.postural_error_schema import (
    PosturalErrorItem,
    PosturalErrorResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/postural-errors", tags=["Postural Errors"])


@router.get(
    "/{practice_id}",
    response_model=StandardResponse[PosturalErrorResponse],
    status_code=status.HTTP_200_OK,
    summary="Get postural errors for a practice",
    description="Retrieve all postural errors detected for a specific practice ID"
)
async def get_postural_errors(
    practice_id: int,
    use_case: GetPosturalErrorsUseCase = Depends(get_postural_errors_use_case_dependency)
):
    """Endpoint that retrieves postural errors for a given practice."""

    logger.info(f"Retrieving postural errors for practice_id={practice_id}")

    errors_dto: List = await use_case.execute(practice_id=practice_id)

    items = [
        PosturalErrorItem(
            min_sec_init=e.min_sec_init,
            min_sec_end=e.min_sec_end,
            explication=e.explication,
        )
        for e in errors_dto
    ]

    response = PosturalErrorResponse(
        num_errors=len(items),
        errors=items
    )

    return StandardResponse.success(
        data=response,
        message=f"Retrieved {len(items)} postural errors for practice {practice_id}"
    )
