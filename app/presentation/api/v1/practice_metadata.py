import logging
from fastapi import APIRouter, Depends, status, Path

from app.application.use_cases.finish_practice_use_case import FinishPracticeUseCase
from app.presentation.api.v1.dependencies import get_finish_practice_use_case_dependency
from app.presentation.schemas.common_schema import StandardResponse
from app.presentation.schemas.practice_metadata_schema import PracticeMetadataResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/practice", tags=["Practices"])


@router.patch(
    "/{uid}/{practice_id}/finish",
    response_model=StandardResponse[PracticeMetadataResponse],
    status_code=status.HTTP_200_OK,
    summary="Finish a practice",
    description="Mark a practice as finished by clearing its local video and returning updated metadata"
)
async def finish_practice(
    uid: str = Path(..., description="User unique identifier"),
    practice_id: int = Path(..., description="Practice identifier"),
    use_case: FinishPracticeUseCase = Depends(get_finish_practice_use_case_dependency)
):
    """
    Endpoint that finishes a practice for a given user:
    - Clears the `video_in_local` field.
    - Returns updated practice metadata.
    """

    logger.info(f"Finishing practice {practice_id} for user {uid}")

    practice_metadata_dto = await use_case.execute(uid=uid, practice_id=practice_id)

    response = PracticeMetadataResponse(
        id_practice=practice_metadata_dto.id_practice,
        video_in_local=practice_metadata_dto.video_in_local,
        report=practice_metadata_dto.report,
        video_done=practice_metadata_dto.video_done,
        audio_done=practice_metadata_dto.audio_done,
    )

    return StandardResponse.success(
        data=response,
        message=f"Practice {practice_id} finished successfully for user {uid}"
    )
