
from app.repositories import BaseRepo
from app.models import RefreshToken as Refresh_model



class TokenRepo(BaseRepo[Refresh_model]):

    model = Refresh_model