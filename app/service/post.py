from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import PostRepo
from app.schemas.post import PostUpdate
from app.service import BaseService
from app.models import Post as PostModel


class PostService(BaseService[PostModel]):

    repo = PostRepo

