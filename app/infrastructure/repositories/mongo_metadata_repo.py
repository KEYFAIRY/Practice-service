import logging

from app.core.exceptions import PracticeNotFoundException, UserNotFoundException
from app.domain.entities.practice_metadata import PracticeMetadata
from app.domain.repositories.metadata_repo import IMetaDataRepository
from app.infrastructure.database.mongo_connection import mongo_connection

logger = logging.getLogger(__name__)


class MongoMetadataRepository(IMetaDataRepository):
    """Concrete implementation of MetadataRepository using Motor (async MongoDB driver)."""

    async def get_practice_metadata(self, uid: str, practice_id: int) -> PracticeMetadata:
        try:
            db = mongo_connection.connect()

            # Get user document by uid
            user_doc = await db["users"].find_one({"uid": uid})
            if not user_doc:
                logger.warning(f"User with uid={uid} not found")
                raise UserNotFoundException(user_id=uid)

            # Get practice metadata by practice_id
            for pr in user_doc.get("practices", []):
                if pr.get("id_practice") == practice_id:
                    logger.info(f"Found practice metadata for uid={uid}, practice_id={practice_id}")
                    return PracticeMetadata(
                        id_practice=practice_id,
                        video_in_local=pr.get("video_in_local"),
                        report=pr.get("report"),
                        video_done=pr.get("video_done", False),
                        audio_done=pr.get("audio_done", False)
                    )

            logger.warning(f"No practice found with id={practice_id} for uid={uid}")
            raise PracticeNotFoundException(practice_id=practice_id)

        except (UserNotFoundException, PracticeNotFoundException):
            raise
        except Exception as e:
            logger.error(
                f"Error fetching practice metadata for uid={uid}, practice_id={practice_id}: {e}",
                exc_info=True
            )
            raise
    
    async def finish_practice(self, uid: str, practice_id: int) -> PracticeMetadata:
        try:
            db = mongo_connection.connect()

            # Get user document by uid
            user_doc = await db["users"].find_one({"uid": uid})
            if not user_doc:
                logger.warning(f"User with uid={uid} not found")
                raise UserNotFoundException(user_id=uid)

            # Update only video_in_local field
            for pr in user_doc.get("practices", []):
                if pr.get("id_practice") == practice_id:
                    await db["users"].update_one(
                        {"uid": uid, "practices.id_practice": practice_id},
                        {"$set": {"practices.$.video_in_local": ""}}
                    )

                    logger.info(f"Cleared video_in_local for uid={uid}, practice_id={practice_id}")
                    return PracticeMetadata(
                        id_practice=practice_id,
                        video_in_local="",  # siempre vacío
                        report=pr.get("report"),
                        video_done=pr.get("video_done", False),
                        audio_done=pr.get("audio_done", False)
                    )

            logger.warning(f"No practice found with id={practice_id} for uid={uid}")
            raise PracticeNotFoundException(practice_id=practice_id)

        except (UserNotFoundException, PracticeNotFoundException):
            raise
        except Exception as e:
            logger.error(
                f"Error finishing practice for uid={uid}, practice_id={practice_id}: {e}",
                exc_info=True
            )
            raise