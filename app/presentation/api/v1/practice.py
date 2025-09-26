import logging
from fastapi import APIRouter, Depends, status, Query
from typing import List
from datetime import date

from app.presentation.schemas.common_schema import StandardResponse
from app.presentation.schemas.practice_schema import PracticeItem, PracticeResponse


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/practice", tags=["Practices"])

@router.get(
    "/{uid}",
    response_model=StandardResponse[PracticeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get practices for a user",
    description="Retrieve a list of practices for a specific user in a given date range"
)
async def get_user_practices(
    uid: str,
    start_date: date = Query(..., description="Start date (inclusive)"),
    end_date: date = Query(..., description="End date (inclusive)"),
    use_case: GetUserPracticesUseCase = Depends(get_user_practices_use_case_dependency)
):
    """Endpoint that retrieves practices for a user within a given date range."""

    logger.info(f"Retrieving practices for user {uid} from {start_date} to {end_date}")

    practices_dto: List = await use_case.execute(uid=uid, start_date=start_date, end_date=end_date)

    # DTOs → PracticeItem
    items = [
        PracticeItem(
            practice_id=p.id,
            scale=p.scale_name,
            scale_type=p.scale_type,
            date=p.date,
            time=p.time,
            state=p.state
        )
        for p in practices_dto
    ]

    response = PracticeResponse(
        num_practices=len(items),
        practices=items
    )

    return StandardResponse.success(
        data=response,
        message=f"Retrieved {len(items)} practices for user {uid}"
    )
