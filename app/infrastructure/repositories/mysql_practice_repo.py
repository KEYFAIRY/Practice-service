import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.core.exceptions import DatabaseConnectionException, PracticeNotFoundException
from app.domain.entities.practice import Practice
from app.domain.repositories.practice_repo import IPracticeRepository
from app.infrastructure.database.models.practice_model import PracticeModel
from app.infrastructure.database.mysql_connection import mysql_connection
from app.shared.constants import PRACTICES_PAGE_LIMIT

logger = logging.getLogger(__name__)


class MySQLPracticeRepository(IPracticeRepository):
    """Concrete implementation of IPracticeRepository for Practice using MySQL."""

    async def get_practices_for_user(
        self,
        uid: str,
        last_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Practice]:
        
        query_limit = limit if limit is not None else PRACTICES_PAGE_LIMIT
                
        logger.info(f"Repository: uid={uid}, last_id={last_id}, limit={limit}, effective_limit={query_limit}")

        async with mysql_connection.get_async_session() as session:
            try:
                stmt = (
                    select(PracticeModel)
                    .options(joinedload(PracticeModel.scale))
                    .where(PracticeModel.id_student == uid)
                    .order_by(PracticeModel.practice_datetime.desc())
                    .limit(query_limit)
                )

                if last_id:
                    subq = (
                        select(PracticeModel.practice_datetime)
                        .where(PracticeModel.id == last_id)
                        .scalar_subquery()
                    )
                    stmt = stmt.where(PracticeModel.practice_datetime < subq)

                result = await session.execute(stmt)
                models = result.scalars().all()

                logger.info(f"Fetched {len(models)} practices for uid={uid}")
                return [self._model_to_entity(m) for m in models]

            except SQLAlchemyError as e:
                logger.error(f"MySQL error fetching practices for uid={uid}: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error fetching practices: {str(e)}")
            
    async def get_practice_by_id(
        self,
        uid: str,
        practice_id: int
    ) -> Practice:
                        
        logger.info(f"Repository: uid={uid}, practice_id={practice_id}")

        async with mysql_connection.get_async_session() as session:
            try:
                stmt = (
                    select(PracticeModel)
                    .options(joinedload(PracticeModel.scale))
                    .where(
                        PracticeModel.id == practice_id,
                        PracticeModel.id_student == uid
                    )
                )

                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    logger.warning(f"Practice {practice_id} not found for user {uid}")
                    raise PracticeNotFoundException(f"Practice {practice_id} not found")

                logger.info(f"Successfully fetched practice {practice_id} for uid={uid}")
                return self._model_to_entity(model)

            except SQLAlchemyError as e:
                logger.error(f"MySQL error fetching practice {practice_id} for uid={uid}: {e}", exc_info=True)
                raise DatabaseConnectionException(f"Error fetching practice {practice_id}: {str(e)}")

    def _model_to_entity(self, model: PracticeModel) -> Practice:
        dt = model.practice_datetime
        return Practice(
            id=model.id,
            scale=model.scale.name if model.scale else "",
            scale_type=model.scale.scale_type if model.scale else "",
            duration=model.duration,
            bpm=model.bpm,
            figure=model.figure,
            octaves=model.octaves,
            num_postural_errors=model.num_postural_errors,
            num_musical_errors=model.num_musical_errors,
            date=dt.strftime("%Y-%m-%d"),
            time=dt.strftime("%H:%M:%S"),
            state="",           # lo completa el use case
            local_video_url="", # lo completa el use case
            pdf_url="",         # lo completa el use case
        )
