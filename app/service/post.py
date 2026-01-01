from app.repositories import PostRepo
from app.service import BaseService
from app.models import Post as PostModel


class PostService(BaseService[PostModel]):

    repo = PostRepo

