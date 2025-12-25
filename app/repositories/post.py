from app.repositories import BaseRepo
from app.models import Post as Post_model


class PostRepo(BaseRepo[Post_model]):

    model = Post_model

