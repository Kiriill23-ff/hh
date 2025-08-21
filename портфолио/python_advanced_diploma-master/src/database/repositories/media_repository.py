from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Media
from src.handlers.exceptions import IntegrityViolationException
from src.schemas.tweet_schemas import NewMediaResponseSchema


async def add_media(link: str, session: AsyncSession) -> NewMediaResponseSchema:

    new_media = Media(link=link)
    session.add(new_media)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise IntegrityViolationException(str(exc))

    return NewMediaResponseSchema(media_id=new_media.id)
