import logging
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
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

    practices_dto: List = await use_case.get_all(uid=uid, last_id=last_id, limit=limit)

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
            num_postural_errors=p.num_postural_errors,
            num_musical_errors=p.num_musical_errors,
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


@router.get(
    "/{uid}/{practice_id}",
    response_model=StandardResponse[PracticeItem],
    status_code=status.HTTP_200_OK,
    summary="Get specific practice",
    description="Retrieve a specific practice by ID for a user with current state"
)
async def get_practice_by_id(
    uid: str = Path(..., description="User unique identifier"),
    practice_id: int = Path(..., description="Practice identifier"),
    use_case: GetUserPracticesUseCase = Depends(get_user_practices_use_case_dependency)
):
    """Endpoint that retrieves a specific practice by ID with current state from database."""
    
    logger.info(f"Retrieving practice {practice_id} for user {uid}")
    
    # Obtener la práctica específica usando el use case existente
    practice = await use_case.get_one(uid=uid, practice_id=practice_id)
        
    # Convertir DTO a PracticeItem
    item = PracticeItem(
        practice_id=practice.id,
        scale=practice.scale,
        scale_type=practice.scale_type,
        duration=practice.duration,
        bpm=practice.bpm,
        figure=practice.figure,
        octaves=practice.octaves,
        num_postural_errors=practice.num_postural_errors,
        num_musical_errors=practice.num_musical_errors,
        date=practice.date,
        time=practice.time,
        state=practice.state,
        local_video_url=practice.local_video_url,
        pdf_url=practice.pdf_url,
    )
        
    logger.info(f"Successfully retrieved practice {practice_id} with state '{practice.state}' for user {uid}")
        
    return StandardResponse.success(
        data=item,
        message=f"Practice {practice_id} retrieved successfully"
    )