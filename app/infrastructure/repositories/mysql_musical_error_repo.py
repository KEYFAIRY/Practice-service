import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import DatabaseConnectionException, MusicalErrorNotFoundException
from app.domain.entities.musical_error import MusicalError
from app.domain.repositories.musical_errror_repo import IMusicalErrorRepository
from app.infrastructure.database.models.musical_error_model import MusicalErrorModel
from app.infrastructure.database.mysql_connection import mysql_connection

logger = logging.getLogger(__name__)

class MySQLMusicalErrorRepository(IMusicalErrorRepository):
    """Concrete implementation of IMusicalErrorRepository using MySQL."""

    async def get_musical_errors_by_practice_id(self, practice_id: int) -> List[MusicalError]:
        try:
            async with mysql_connection.get_async_session() as session:
                result = await session.execute(
                    select(MusicalErrorModel).where(MusicalErrorModel.id_practice == practice_id)
                )
                rows = result.scalars().all()

                if not rows:
                    logger.warning(f"No musical errors found for practice_id={practice_id}")
                    raise MusicalErrorNotFoundException(practice_id, f"No musical errors for practice {practice_id}")

                logger.debug(f"Fetched {len(rows)} musical errors for practice_id={practice_id}")
                return [self._model_to_entity(row) for row in rows]

        except IntegrityError as e:
            logger.error(f"MySQL integrity error for practice_id={practice_id}: {e}", exc_info=True)
            raise DatabaseConnectionException("Database integrity error")
        except SQLAlchemyError as e:
            logger.error(f"MySQL error fetching musical errors for practice_id={practice_id}: {e}", exc_info=True)
            raise DatabaseConnectionException(f"Error fetching musical errors: {str(e)}")

    def _model_to_entity(self, model: MusicalErrorModel) -> MusicalError:
        return MusicalError(
            id=model.id,
            min_sec=model.min_sec,
            missed_note=model.missed_note,
            id_practice=model.id_practice
        )
