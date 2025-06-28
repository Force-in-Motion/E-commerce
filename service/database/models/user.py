from sqlalchemy.orm import Mapped
from service.database.models.base import Base



class User(Base):

    __tablename__ = 'User'

    name: Mapped[str]
    floor: Mapped[str]
    age: Mapped[int]
    email: Mapped