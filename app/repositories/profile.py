from app.repositories import BaseRepo
from app.models import Profile as Profile_model


class ProfileRepo(BaseRepo[Profile_model]):

    model = Profile_model
