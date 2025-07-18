from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import Post
from web.schemas import UserInput


async def get_all_posts(session: AsyncSession) -> list[Post]:
    pass
