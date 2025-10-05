import logging
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from datetime import date

from app.application.use_cases.get_user_practices_use_case import GetUserPracticesUseCase
from app.presentation.api.v1.dependencies import get_user_practices_use_case_dependency
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
    last_id: Optional[int] = Query(None, description="ID of the last practice from previous page for pagination"),
    limit: Optional[int] = Query(None, description="Maximum number of practices to return"),
    use_case: GetUserPracticesUseCase = Depends(get_user_practices_use_case_dependency)
):
    """Endpoint that retrieves practices for a user within a given date range."""

    logger.info(f"Retrieving practices for user {uid} with last_id={last_id} and limit {limit}")

    practices_dto: List = await use_case.execute(uid=uid, last_id=last_id, limit=limit)

    # DTOs → PracticeItem
    items = [
        PracticeItem(
            practice_id=p.id,
            scale=p.scale,
            scale_type=p.scale_type,
            duration=p.duration,
            bpm=p.bpm,
            figure=p.figure,
            octaves=p.octaves,
            date=p.date,
            time=p.time,
            state=p.state,
            local_video_url=p.local_video_url,
            pdf_url=p.pdf_url,
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
