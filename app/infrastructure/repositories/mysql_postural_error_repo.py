import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.domain.entities.postural_error import PosturalError
from app.domain.repositories.postural_error_repo import IPosturalErrorRepository
from app.infrastructure.database.models.postural_error_model import PosturalErrorModel
from app.infrastructure.database.mysql_connection import mysql_connection
from app.core.exceptions import DatabaseConnectionException, PosturalErrorNotFoundException

logger = logging.getLogger(__name__)

class MySQLPosturalErrorRepository(IPosturalErrorRepository):
    """Concrete implementation of IPosturalErrorRepository using MySQL."""

    async def get_postural_errors_by_practice_id(self, practice_id: int) -> List[PosturalError]:
        try:
            async with mysql_connection.get_async_session() as session:
                result = await session.execute(
                    select(PosturalErrorModel).where(PosturalErrorModel.id_practice == practice_id)
                )
                rows = result.scalars().all()

                if not rows:
                    logger.warning(f"No postural errors found for practice_id={practice_id}")
                    raise PosturalErrorNotFoundException(practice_id, f"No postural errors for practice {practice_id}")

                logger.debug(f"Fetched {len(rows)} postural errors for practice_id={practice_id}")
                return [self._model_to_entity(row) for row in rows]

        except IntegrityError as e:
            logger.error(f"MySQL integrity error for practice_id={practice_id}: {e}", exc_info=True)
            raise DatabaseConnectionException("Database integrity error")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error fetching postural errors for practice_id={practice_id}: {e}", exc_info=True)
            raise DatabaseConnectionException(f"Error fetching postural errors: {str(e)}")

    def _model_to_entity(self, model: PosturalErrorModel) -> PosturalError:
        return PosturalError(
            id=model.id,
            min_sec_init=model.min_sec_init,
            min_sec_end=model.min_sec_end,
            explication=model.explication,
            id_practice=model.id_practice
        )
