from datetime import date
import logging
from typing import List, Optional

from app.application.dto.practice_dto import PracticeDTO
from app.domain.services.practice_metadata_service import PracticeMetadataService
from app.domain.services.practice_service import PracticeService
from app.shared.enums import PracticeState

logger = logging.getLogger(__name__)

class GetUserPracticesUseCase:
    """Use case for retrieving user practices within a date range."""
    
    def __init__(self, practice_service: PracticeService, practice_metadata_service: PracticeMetadataService):
        self.practice_service = practice_service
        self.practice_metadata_service = practice_metadata_service

    async def execute(self, uid: str, last_id: Optional[int] = None) -> List[PracticeDTO]:
        """Retrieve practices for a user within the specified date range."""
        
        logger.info(f"Fetching practices for user {uid} with last_id={last_id}")
        practices = await self.practice_service.get_practices_for_user(uid, last_id=last_id)
        
        # 2. Get practices info from MongoDB
        logger.info(f"Fetching metadata for {len(practices)} practices")
        for p in practices:
            metadata = await self.practice_metadata_service.get_practice_metadata(uid, p.id)
            p.local_video_url = metadata.video_in_local
            p.pdf_url = metadata.report
            
            # FINISHED: Report ready and video deleted from local
            if metadata.report != "" and metadata.video_in_local == "":
                p.state = PracticeState.FINISHED
            # COMPLETED: Report ready and video still in local
            elif metadata.report != "" and metadata.video_in_local != "":
                p.state = PracticeState.COMPLETED
            # ANALYZED: Audio/video analysis done, report pending
            if metadata.video_done and metadata.audio_done and metadata.report == "":
                p.state = PracticeState.ANALYZED
            # IN_PROGRESS: Audio or video analysis in progress
            elif not (metadata.video_done and metadata.audio_done):
                p.state = PracticeState.IN_PROGRESS
            
        
        logger.info(f"Retrieved {len(practices)} practices for user {uid}")
        
        # 3. Convert to DTOs and return
        return [PracticeDTO(id=p.id,
                            scale=p.scale,
                            scale_type=p.scale_type,
                            date=p.date,
                            time=p.time,
                            state=p.state,
                            local_video_url=p.local_video_url,
                            pdf_url=p.pdf_url
                            ) for p in practices]