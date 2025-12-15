from app.repositories import ProfileRepo
from app.service import BaseService


class ProfileService(BaseService[ProfileRepo]):

    repo = ProfileRepo
