from app.service.base import BaseService
from app.repositories import TokenRepo


class TokenService(BaseService[TokenRepo]):

    repo = TokenRepo